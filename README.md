# city-council — Vancouver WA and Clark County WA agenda watch

Ongoing monitoring rather than a one-off analysis: retrieve agendas as they are published, read
the attachments, and produce a short pre-meeting brief flagging what is relevant, where public
comment is open, and where public money or land is moving.

This folder differs from the other projects here — there is no single analysis document and no
terminal artifact. The deliverable is a recurring brief in `briefs/`.

## Status

| Piece | State |
|---|---|
| Vancouver WA agenda access | working — CivicClerk OData API |
| Clark County WA agenda access | working — Drupal listing scrape |
| `data/agenda_watch.py` | working, ~15s per run, both sources |
| `data/clark-county/fetch_clark_county.py` | working, Clark County only, more verbose output |
| `BRIEF-PROMPT.md` | written — the lens and output structure |
| Scheduling | **not set up** — see "Running it" below |
| Briefs written | none yet |

## Layout

```
README.md                                 this file
BRIEF-PROMPT.md                           how a digest becomes a brief
data/
  agenda_watch.py                         both bodies -> briefs/raw/<date>-digest.md
  .agenda-watch-state.json                seen-agenda fingerprints (auto)
  clark-county/
    fetch_clark_county.py                 Clark County listing walker
    clark-rules-of-procedure-2026-07-27.pdf/.txt   cached primary source
briefs/
  raw/<date>-digest.md                    raw gather, no interpretation
  <meeting-date>-<body>.md                the brief
```

## Running it

```bash
python3 data/agenda_watch.py            # new/changed agendas only
python3 data/agenda_watch.py --all      # everything in the window
python3 data/agenda_watch.py --days 30  # widen the lookahead
python3 data/agenda_watch.py --fetch 1083   # download a Vancouver packet
```

Then follow `BRIEF-PROMPT.md` against the digest it writes.

**When to run.** The two bodies publish on different days, so a two-run week catches both:

- **Wednesday** — Clark County's next Tuesday agenda is due by 5pm (Rules §VII.A), and Vancouver's
  Monday agenda posts about a week out.
- **Friday** — Clark County Council Time additions are posted by Friday noon (Rules §VII.P).

Nothing schedules this yet. Cloud routines (`/schedule`) cannot reach this directory, so
unattended running needs either the repo pushed to git so a cloud agent can clone it, or a local
cron entry.

## Meeting days

| Body | Day | What happens | Public comment |
|---|---|---|---|
| Vancouver City Council | Monday | Workshops, consent, hearings | per meeting, see digest |
| Vancouver Planning Commission | 2nd/4th Tuesday | Zoning and comp-plan implementation | yes |
| Clark County Council — regular | Tuesday, ~1st & 3rd | Consent, ordinances, hearings, votes | 3 min, **any county business** |
| Clark County Council Time | Wednesday, weekly | Informal discussion | 3 min, **agenda items only** |
| Clark County Work Sessions | Wednesday, 9am–noon | Briefings | **none** |
| Clark County Board of Health | Wednesday | | yes |

## Gotchas

- **A Vancouver `agendaId` is assigned long before the agenda exists.** A future meeting can show
  a non-zero `agendaId` whose `Meetings/{id}` returns zero items. Item count is the test.
- **Council skips weeks.** There was no Vancouver meeting on 31 Aug 2026. Confirm the meeting
  exists before concluding an agenda is late.
- **Clark County's Sunday-dated rows are not meetings** — they are the Weekly Calendar PDF for the
  week ahead, posted the preceding Thursday. It is the earliest published notice of what is coming.
- **Clark County filenames are not consistently formatted** (`8.19.26-ct-agenda.pdf` next to
  `08262026-ct-agenda.pdf`). Scrape the href; never construct one from a date.
- **Vancouver's `fiscalImpactSummary` is empty on the public API.** A blank field is not evidence
  of no fiscal impact — the numbers are in the attachments.
- **The CivicClerk API is slow**, roughly 5–10 seconds per request and one request per meeting.
  Keep windows tight.
- **`codepublishing.com` is behind Cloudflare** and resisted a reasonable effort, so Clark County
  Code 2.04 (which the Rules of Procedure cite for the statutory meeting day) is **unverified**.
  The Rules themselves are cached here and are decisive on practice.
- Vancouver WA is not Vancouver BC; Clark County WA is not Clark County NV.

## Sources

1. Clark County Council, *Rules of Procedure*, adopted markup dated 27 July 2026 — cached at
   `data/clark-county/clark-rules-of-procedure-2026-07-27.pdf`. §IV.A meeting days, §VII.A agenda
   posting deadline, §VII.L public comment, §VII.P Council Time additions, §VIII work sessions.
2. Clark County WA, Council Meetings listing —
   `https://clark.wa.gov/councilors/clark-county-council-meetings`
3. City of Vancouver WA, CivicClerk portal — `https://vancouverwa.portal.civicclerk.com`
   (API: `https://vancouverwa.api.civicclerk.com/v1`)
4. RCW 42.30.080 — special meetings, 24 hours' notice.
