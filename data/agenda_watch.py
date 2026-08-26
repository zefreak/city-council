#!/usr/bin/env python3
"""
Agenda watcher for Vancouver WA and Clark County WA.

Gathers newly-published agendas from both bodies and writes a DIGEST — a
structured dump of every upcoming meeting, its agenda tree, its attachments and
its public-comment status. The digest is input for a human-or-model reading
pass; this script deliberately does no summarising and applies no political
judgement. See BRIEF-PROMPT.md for what happens to the digest afterwards.

Two very different sources (see ../../CLAUDE.md §8):

    Vancouver WA    CivicClerk OData API, vancouverwa.api.civicclerk.com/v1
                    Council meets MONDAY. Agendas post ~1 week out.
    Clark County    plain Drupal view at clark.wa.gov
                    Regular Council meets TUESDAY (~1st and 3rd); agenda posts
                    by 5pm the preceding WEDNESDAY. Council Time and Work
                    Sessions meet WEDNESDAY.

So a Wednesday run catches Clark County's next Tuesday agenda, and a Friday run
catches Council Time additions (posted by Friday noon) — hence the two-run week.

State
-----
Meetings already digested are recorded in .agenda-watch-state.json, keyed by
source + meeting id + a fingerprint of the agenda contents. An agenda that is
REVISED after first publication therefore resurfaces, which matters: items get
added to Vancouver consent agendas late.

Usage:
    python3 agenda_watch.py                 # new/changed agendas only
    python3 agenda_watch.py --all           # everything in the window
    python3 agenda_watch.py --days 30       # widen the lookahead
    python3 agenda_watch.py --fetch 1083    # download a Vancouver agenda's PDFs

Pure stdlib. Network at run time by design — this is a fetcher, not a model.
"""

import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
RAW = os.path.join(PROJECT, "briefs", "raw")
STATE = os.path.join(HERE, ".agenda-watch-state.json")

VAN_API = "https://vancouverwa.api.civicclerk.com/v1"
CLARK = "https://clark.wa.gov"
CLARK_LIST = f"{CLARK}/councilors/clark-county-council-meetings"
UA = "Mozilla/5.0 (X11; Linux x86_64) research-archival-fetch"

LOOKAHEAD_DAYS = 14
LOOKBACK_DAYS = 3          # so a run just after a meeting still captures it
CLARK_PAGES = 1            # page 0 covers ~5 weeks; the listing is newest-first

# Sections whose items pass WITHOUT debate unless a member pulls them. Worth
# calling out separately: this is where substantive things get buried.
QUIET_SECTIONS = ("consent",)


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.geturl()


def jget(url):
    return json.loads(get(url)[0])


def text(fragment):
    t = re.sub(r"<(br|/p|/li|/div|/tr)[^>]*>", "\n", fragment, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"[ \t\xa0]+", " ", t).strip()


# ---------------------------------------------------------------- Vancouver

def van_events(days_ahead, days_back=LOOKBACK_DAYS):
    today = dt.date.today()
    since = (today - dt.timedelta(days=days_back)).isoformat() + "T00:00:00Z"
    until = (today + dt.timedelta(days=days_ahead + 1)).isoformat() + "T00:00:00Z"
    q = urllib.parse.urlencode({
        "$filter": f"startDateTime ge {since} and startDateTime le {until}",
        "$orderby": "startDateTime asc",
        "$top": 200,
    }, quote_via=urllib.parse.quote)
    url, out = f"{VAN_API}/Events?{q}", []
    while url:                       # pages at 15 regardless of $top
        page = jget(url)
        out.extend(page.get("value") or [])
        url = page.get("@odata.nextLink")
    return out


def van_walk(items, section=None, depth=0):
    """Yield (section, depth, item). `section` is the nearest ancestor that
    looks like a heading — that is how Consent Agenda / Public Hearings is
    recovered, since agendaObjItemCategoryTypeDesc is empty on the public API."""
    for it in items or []:
        name = (it.get("agendaObjectItemName") or "").strip()
        kids = it.get("childItems")
        here = name if (kids and not it.get("attachmentsList")) else section
        # A heading yields itself flagged, so the renderer can print it as a
        # section header instead of repeating it as an ordinary line.
        yield section, depth, it, here is not section
        yield from van_walk(kids, here, depth + 1)


def van_meetings(days_ahead):
    out = []
    for e in van_events(days_ahead):
        aid = e.get("agendaId") or 0
        rec = {
            "source": "vancouver",
            "id": f"van-{e['id']}",
            "when": (e.get("startDateTime") or "")[:16],
            "body": e.get("eventName", ""),
            "published": False,
            "items": [], "files": [], "comment": {},
        }
        # An agendaId is assigned long before publication; item count is the test.
        if aid:
            try:
                a = jget(f"{VAN_API}/Meetings/{aid}")
            except Exception as exc:                       # noqa: BLE001
                rec["error"] = str(exc)
                out.append(rec)
                continue
            items = a.get("items") or []
            rec["published"] = bool(items)
            rec["comment"] = {
                "speaker_signup": a.get("enablePublicSpeakerSignup"),
                "written_comment": a.get("enableWrittenComment"),
                "signup_cutoff": a.get("signUpCutoffTime"),
                "comment_cutoff": a.get("commentCutOffTime"),
            }
            for f in a.get("publishedFiles") or []:
                rec["files"].append({
                    "name": f.get("name") or f.get("type"),
                    "url": f"{VAN_API}/Meetings/GetAttachmentFile"
                           f"(fileId={f.get('fileId')})"})
            for sect, depth, it, is_heading in van_walk(items):
                name = (it.get("agendaObjectItemName") or "").strip()
                if not name:
                    continue
                atts = [{"name": at.get("fileName") or "(unnamed)",
                         "size": at.get("fileSize", 0),
                         "url": f"{VAN_API}/Meetings/GetAttachmentFile"
                                f"(fileId={at['id']})"}
                        for at in (it.get("attachmentsList") or [])]
                rec["items"].append({"section": sect, "depth": depth,
                                     "name": name, "attachments": atts,
                                     "heading": is_heading})
        out.append(rec)
    return out


# ------------------------------------------------------------- Clark County

def clark_cells(row):
    out = {}
    for h, c in re.findall(r'<td[^>]*headers="([^"]+)"[^>]*>(.*?)</td>',
                           row, re.S):
        k = h.split("-table-column")[0]
        k = k.replace("view-field-", "").replace("view-", "")
        out[k.replace("-", "_")] = c
    return out


def clark_docs(fragment):
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', fragment, re.S):
        href, name = m.group(1), text(m.group(2))
        if "/media/document/" not in href and not href.endswith(".pdf"):
            continue
        out.append({"name": name or "(untitled)",
                    "url": urllib.parse.urljoin(CLARK, href)})
    return out


def clark_meetings(days_ahead, pages=CLARK_PAGES):
    """The Drupal listing is newest-first and mostly retrospective; the forward
    view is the Weekly Calendar row (Sunday-dated), posted the preceding
    Thursday. Both are returned."""
    lo = dt.date.today() - dt.timedelta(days=LOOKBACK_DAYS)
    hi = dt.date.today() + dt.timedelta(days=days_ahead)
    out, seen_date = [], None
    for page in range(pages):
        body = get(f"{CLARK_LIST}?page={page}")[0].decode("utf-8", "replace")
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
            c = clark_cells(row)
            if not c:
                continue
            d = text(c.get("date", ""))
            if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", d):
                m, dd, y = (int(x) for x in d.split("/"))
                seen_date = dt.date(y, m, dd)
            if not seen_date or not (lo <= seen_date <= hi):
                continue
            agenda, blurb = c.get("agenda_text", ""), c.get("body", "")
            head, label = text(agenda), text(c.get("media_text", ""))
            outline = text(blurb)
            if not (head or outline):
                continue
            weekly = "weekly calendar" in head.lower()
            out.append({
                "source": "clark",
                "id": f"clark-{seen_date}-{len(out)}",
                "when": seen_date.isoformat(),
                "weekday": seen_date.strftime("%A"),
                "body": ("Weekly Calendar" if weekly else
                         (label or head.split("\n")[0] or "session")),
                "kind": "weekly-calendar" if weekly else "session",
                "published": True,
                "outline": outline,
                "files": clark_docs(agenda) + clark_docs(blurb),
            })
    out.sort(key=lambda r: r["when"])
    return out


# ------------------------------------------------------------------- digest

def fingerprint(rec):
    """Changes when the agenda content changes, so revised agendas resurface."""
    if rec["source"] == "vancouver":
        blob = json.dumps([i["name"] for i in rec["items"]], sort_keys=True)
    else:
        blob = json.dumps([f["url"] for f in rec["files"]] + [rec["outline"]],
                          sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def render(recs):
    L = [f"# Agenda digest — {dt.date.today().isoformat()}", ""]
    L.append("Generated by `data/agenda_watch.py`. Raw gather, no interpretation.")
    L.append("Turn this into a brief using `BRIEF-PROMPT.md`.")
    L.append("")
    for r in recs:
        L.append("---")
        L.append("")
        when = r["when"]
        if r["source"] == "clark":
            when = f"{when} ({r['weekday']})"
        L.append(f"## {when} — {r['body']}")
        L.append(f"*source: {r['source']} · id: {r['id']}*")
        L.append("")
        if r.get("error"):
            L.append(f"> fetch error: {r['error']}")
            L.append("")
            continue
        if not r["published"]:
            L.append("> Agenda not published yet.")
            L.append("")
            continue
        if r["source"] == "vancouver":
            c = r["comment"]
            L.append(f"- Public speaker signup: **{c.get('speaker_signup')}** · "
                     f"written comment: **{c.get('written_comment')}**")
            if r["files"]:
                L.append("- Packet files:")
                for f in r["files"]:
                    L.append(f"  - [{f['name']}]({f['url']})")
            L.append("")
            section = object()
            for it in r["items"]:
                if it["section"] != section:
                    section = it["section"]
                    if section:
                        quiet = any(q in (section or "").lower()
                                    for q in QUIET_SECTIONS)
                        tag = ("  ← passes without debate unless pulled"
                               if quiet else "")
                        L.append("")
                        L.append(f"### {section}{tag}")
                if it["heading"]:
                    continue          # already rendered as the ### header
                pad = "  " * max(0, it["depth"] - 1)
                L.append(f"{pad}- {it['name']}")
                for a in it["attachments"]:
                    L.append(f"{pad}  - [{a['name']}]({a['url']}) "
                             f"({a['size']:,} bytes)")
            L.append("")
        else:
            if r["kind"] == "weekly-calendar":
                L.append("*Forward-looking calendar for the week ahead.*")
            if r["outline"]:
                L.append("```")
                L.append(r["outline"][:4000])
                L.append("```")
            for f in r["files"]:
                L.append(f"- [{f['name']}]({f['url']})")
            L.append("")
    return "\n".join(L) + "\n"


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--fetch":
        a = jget(f"{VAN_API}/Meetings/{args[1]}")
        for f in a.get("publishedFiles") or []:
            url = f"{VAN_API}/Meetings/GetAttachmentFile(fileId={f['fileId']})"
            blob = get(url, timeout=180)[0]
            path = os.path.join(RAW, f"van-{args[1]}-{f['fileId']}.pdf")
            with open(path, "wb") as fh:
                fh.write(blob)
            print(f"saved {path} ({len(blob):,} bytes)")
        return

    show_all = "--all" in args
    days = LOOKAHEAD_DAYS
    if "--days" in args:
        days = int(args[args.index("--days") + 1])

    recs = van_meetings(days) + clark_meetings(days)
    recs.sort(key=lambda r: r["when"])

    state = load_state()
    fresh = []
    for r in recs:
        if not r["published"]:
            fresh.append(r)
            continue
        fp = fingerprint(r)
        if show_all or state.get(r["id"]) != fp:
            fresh.append(r)
        state[r["id"]] = fp

    if not fresh:
        print("No new or changed agendas.")
        return

    out = os.path.join(RAW, f"{dt.date.today().isoformat()}-digest.md")
    with open(out, "w") as f:
        f.write(render(fresh))
    with open(STATE, "w") as f:
        json.dump(state, f, indent=1, sort_keys=True)
    published = sum(1 for r in fresh if r["published"])
    print(f"{len(fresh)} meetings ({published} with published agendas)")
    print(f"digest -> {out}")


if __name__ == "__main__":
    main()
