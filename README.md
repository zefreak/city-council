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
| `data/run_watch.sh` | written — local cron runner, gather + brief + notify |
| Scheduling | local cron, twice weekly — see "Running it" |
| Email notifications | **needs msmtp set up once** — see below |
| Cloud routine | disabled — sandbox egress blocks both councils |
| Briefs written | 3 — Vancouver 24 Aug, Clark County 26 Aug, Planning Commission 8 Sep |

## Layout

```
README.md                                 this file
BRIEF-PROMPT.md                           how a digest becomes a brief
data/
  agenda_watch.py                         both bodies -> briefs/raw/<date>-digest.md
  run_watch.sh                            cron runner: gather + claude -p + notify
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

**Network access.** The run needs outbound HTTPS to `vancouverwa.api.civicclerk.com` and
`clark.wa.gov`. In a sandboxed or proxied environment both must be on the egress allowlist — the
27 August 2026 run failed entirely because they were not, with the proxy answering 403 to CONNECT
for both (see `briefs/raw/2026-08-27-digest.md`). The failure surfaces as
`URLError: Tunnel connection failed: 403 Forbidden` out of `van_meetings()`, which looks like a
site outage and is not one. A policy denial is to be reported, not worked around.

**When to run.** The two bodies publish on different days, so a two-run week catches both:

- **Wednesday** — Clark County's next Tuesday agenda is due by 5pm (Rules §VII.A), and Vancouver's
  Monday agenda posts about a week out.
- **Friday** — Clark County Council Time additions are posted by Friday noon (Rules §VII.P).

### Automated, twice a week

`data/run_watch.sh` runs the whole job locally: gather, read attachments, write briefs, publish the
artifact, commit, push, then notify by desktop popup and email. Add to `crontab -e`:

```cron
PATH=/home/scottr/sf/bin:/usr/local/bin:/usr/bin:/bin
0 19 * * 3,5 /home/scottr/research/city-council/data/run_watch.sh >/dev/null 2>&1
```

Wednesday and Friday at 7pm local. The `PATH` line matters — cron's default does not include
`~/sf/bin`, where `claude` lives.

Test it without waiting for cron:

```bash
data/run_watch.sh          # full run
tail -f briefs/raw/run-*.log
```

Exit codes: `0` work done or nothing to do, `1` setup problem, `2` the gather failed.

### Email setup — required once

`mail` and `mailx` are installed but have **no MTA behind them**, so they silently fail to deliver.
`msmtp` is what actually sends. Until it is configured the script still runs and still notifies on
the desktop, but it logs `EMAIL NOT SENT` and raises a critical desktop notice rather than failing
quietly — a missed brief must never look like a quiet week.

```bash
sudo pacman -S --needed msmtp
```

Then create `~/.msmtprc` (Gmail needs an **app password**, not the account password — generate one
at https://myaccount.google.com/apppasswords with 2FA enabled):

```
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

account        gmail
host           smtp.gmail.com
port           587
from           zefreak@gmail.com
user           zefreak@gmail.com
password       <app-password>

account default : gmail
```

`chmod 600 ~/.msmtprc` — msmtp refuses to use a world-readable file containing a password. Test
with `printf 'Subject: test

body
' | msmtp zefreak@gmail.com`.

### Why local rather than a cloud routine

This ran first as a Claude Code cloud routine (`trig_01RT8WqXFyTLpGRsE8gHBGmp`, now disabled). The
cloud sandbox sits behind an egress proxy that allowlists package registries and API hosts;
`clark.wa.gov` and `vancouverwa.api.civicclerk.com` are not on it and answered 403 to CONNECT, so
the gather could not run at all. Adding domains requires the Enterprise admin console. The failed
run is recorded at `briefs/raw/2026-08-27-digest.md`. Re-enabling the routine is one API call if
that ever changes.



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
- **Meeting-level files use `GetMeetingFile`, item attachments use `GetAttachmentFile`.** The two
  endpoints share a fileId namespace, so the wrong one returns *an unrelated document* with HTTP
  200 and no error — fileId 2994 on `GetAttachmentFile` returns a Cultural Access deck from
  October 2025 instead of the September 2026 Planning Commission agenda. Use the `url` field the
  API supplies in `publishedFiles`. It returns JSON `{"blobUri": ...}`, not a PDF; fetch the
  blobUri as a second step.
- **`agendaIsPublish` and `agendaPacketIsPublish` are different things.** An agenda can be
  published while the packet is not — which means the agenda titles are readable but every staff
  report is still unavailable. Check the packet flag before concluding an item has no documents,
  and re-run closer to the meeting.
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
