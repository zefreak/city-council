#!/usr/bin/env python3
"""
Fetch Clark County WA council meeting agendas, packets and attachments.

Clark County is NOT CivicClerk. It is a plain Drupal 10 site, and the meeting
listing is an ordinary rendered view — no API, no SPA, no JS needed:

    listing  https://clark.wa.gov/councilors/clark-county-council-meetings
    archive  https://clark.wa.gov/councilors/meetings-agendas-and-archives?year=YYYY

Compare Vancouver WA, which needs the OData API on a separate host — see
../../../housing/data/vancouver-wa/fetch_council.py. The two counties/cities
share a building and share nothing else.

Structure of the listing
------------------------
A Drupal view (`council_meetings`) rendered as a table, paged at ~15 date-groups
per page via `?page=N`, N counting BACKWARDS in time from 0 (most recent).
As of Aug 2026 the pager ran to ?page=102, i.e. back to roughly 2009.

Each `<tr>` is one SESSION, with cells addressed by their `headers` attribute:

    view-field-date-table-column          8/26/2026  — or EMPTY, see below
    view-field-agenda-text-table-column   "1:00pm" + <a>Agenda</a>, <a>Minutes</a>
    view-body-table-column                blurb, the agenda outline, attachments
    view-field-media-text-table-column    short session label, e.g. "BOH Meeting"

Traps
-----
  * The date cell is filled only on the FIRST session of a day; later sessions
    that day have an EMPTY date cell. Carry the last seen date forward or you
    will attribute Council Time to the wrong week.
  * Sunday-dated rows are not meetings. They are the "Weekly Calendar" PDF for
    the week ahead, posted the preceding Thursday. Useful — that is the earliest
    published notice of what is coming — but do not count them as sessions.
  * Attachment links come in TWO forms and you must handle both:
        /sites/default/files/media/document/YYYY-MM/name.pdf   direct
        /media/document/234766                                 media entity,
        302-redirects to the direct URL. urllib follows it; take the final URL
        for the filename, because the entity id tells you nothing.
  * Filenames are NOT consistently formatted. Real examples from one month:
        8.19.26-ct-agenda.pdf        08262026-ct-agenda.pdf
    Never construct a URL from a date. Always scrape the href.
  * "ct" = Council Time, "ws" = Work Session, "boh" = Board of Health.

Meeting days — do not conflate them
-----------------------------------
Rules of Procedure (cached here as clark-rules-of-procedure-2026-07-27-DRAFT.pdf
— a DRAFT going to hearing 1 Sept 2026; last adopted version is 4 Feb 2025):

  TUESDAY   §IV.A  the REGULAR Council meeting: consent agenda, ordinances,
                   public hearings, the actual votes. Roughly 1st and 3rd
                   Tuesday. Agenda posts by 5 pm the PRECEDING WEDNESDAY.
  WEDNESDAY §VII.P Council Time, weekly, informal discussion; items may be
                   added and posted by Friday noon.
            §VIII  Work Sessions, "typically scheduled between 9 a.m. and
                   noon on Wednesday". No public comment.
                   Board of Health also sits Wednesday.

Filter on Wednesday alone and you will miss every consent agenda. Observed
Jun-Aug 2026 across the listing: 11 Wed, 5 Tue, 10 Sun (weekly-calendar rows),
1 Mon (a special meeting — RCW 42.30.080, 24 hours' notice, so these appear
with little warning).

Usage (no arguments; edit the constants below):
    python3 fetch_clark_county.py           # list meetings + matching documents
    python3 fetch_clark_county.py --get URL # download one document

Pure stdlib. Network at run time by design — this is a fetcher, not a model.
"""

import html
import os
import re
import sys
import urllib.parse
import urllib.request

SITE = "https://clark.wa.gov"
LISTING = f"{SITE}/councilors/clark-county-council-meetings"
UA = "Mozilla/5.0 (X11; Linux x86_64) research-archival-fetch"
OUT = os.path.dirname(os.path.abspath(__file__))

# Words that mark a session or document as worth pulling.
KEYWORDS = ("housing", "afford", "homeless", "shelter", "comprehensive plan",
            "zoning", "land use", "growth management", "density", "co-living",
            "coliving", "compact lot", "manufactured", "impact fee", "adu",
            "mental health sales tax", "subdivision")

MAX_PAGES = 4          # ~15 date-groups per page; 4 pages is roughly 6 months
DOC_RE = re.compile(r'href="(/(?:sites/default/files/)?media/document/[^"]+)"')


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.geturl()


def text(fragment):
    """HTML fragment -> collapsed plain text."""
    t = re.sub(r"<(br|/p|/li|/div)[^>]*>", "\n", fragment, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"[ \t\xa0]+", " ", t).strip()


def cells(row):
    out = {}
    for h, c in re.findall(r'<td[^>]*headers="([^"]+)"[^>]*>(.*?)</td>',
                           row, re.S):
        key = h.split("-table-column")[0]
        key = key.replace("view-field-", "").replace("view-", "")
        out[key.replace("-", "_")] = c
    return out


def sessions(max_pages=MAX_PAGES):
    """Yield dicts, one per session row, date carried forward across the
    empty date cells that follow the first session of each day."""
    seen_date = None
    for page in range(max_pages):
        body, _ = get(f"{LISTING}?page={page}")
        body = body.decode("utf-8", "replace")
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
            c = cells(row)
            if not c:
                continue
            d = text(c.get("date", ""))
            if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", d):
                seen_date = d
            agenda, blurb = c.get("agenda_text", ""), c.get("body", "")
            label = text(c.get("media_text", ""))
            head = text(agenda)
            if "weekly calendar" in head.lower():
                yield {"date": seen_date, "kind": "weekly-calendar",
                       "label": head, "docs": docs(agenda), "outline": ""}
                continue
            if not (head or blurb):
                continue
            yield {"date": seen_date, "kind": "session",
                   "label": label or head.split("\n")[0],
                   "time": head.split("\n")[0],
                   "docs": docs(agenda) + docs(blurb),
                   "outline": text(blurb)}


def docs(fragment):
    """(link text, absolute url) for every document link in a fragment."""
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', fragment, re.S):
        href, name = m.group(1), text(m.group(2))
        if "/media/document/" not in href and not href.endswith(".pdf"):
            continue
        out.append((name or "(untitled)", urllib.parse.urljoin(SITE, href)))
    return out


def download(url, name=None):
    blob, final = get(url)          # resolves the /media/document/N redirect
    name = name or os.path.basename(urllib.parse.urlparse(final).path)
    path = os.path.join(OUT, f"clark-{name}")
    with open(path, "wb") as f:
        f.write(blob)
    print(f"  saved {path} ({len(blob):,} bytes)")
    return path


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--get":
        download(sys.argv[2])
        return

    print(f"Clark County WA council — {MAX_PAGES} listing pages\n" + "=" * 78)
    last = None
    for s in sessions():
        if s["date"] != last:
            print(f"\n{s['date']}")
            last = s["date"]
        if s["kind"] == "weekly-calendar":
            for n, u in s["docs"]:
                print(f"    CALENDAR  {n}\n              {u}")
            continue
        label = re.sub(r"\s*\n\s*", " / ", s["label"])
        print(f"    {label[:74]}")
        hit = any(k in s["outline"].lower() or k in s["label"].lower()
                  for k in KEYWORDS)
        for n, u in s["docs"]:
            mark = "*" if hit or any(k in n.lower() for k in KEYWORDS) else " "
            print(f"      {mark} {n[:56]:<56} {u}")


if __name__ == "__main__":
    main()
