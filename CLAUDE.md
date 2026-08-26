# city-council — working conventions

Agenda monitoring for **Vancouver WA** and **Clark County WA**. Retrieve agendas as they are
published, read the attachments, and write a short pre-meeting brief.

Extracted from a larger public-policy research repo; the conventions below are the parts that
apply here. The standing rule from that repo holds: **be specific about what is firm and what is
not.** A number quoted without its provenance is worse than no number.

## The task

1. `python3 data/agenda_watch.py` — writes `briefs/raw/<date>-digest.md`.
2. Follow **`BRIEF-PROMPT.md`**, which is the full instruction set: the lens, the three things to
   look for, the output structure, and the accuracy rules. Read it before writing anything.
3. Write the brief to `briefs/<meeting-date>-<body>.md` and commit it.

`README.md` carries the status table, meeting days, and the gotchas.

## Scripts

- **Pure stdlib Python 3.** No pandas, no requests.
- Fetchers may use the network at run time; that is what they are for. Anything that computes
  should take its inputs as module-level literals with a citation comment.
- **Print a readable report**, not a data structure.
- **Record retired findings in comments.** When an approach is abandoned, leave a note saying so
  and why — a future reader needs to know the earlier version was wrong.

## Sourcing

- **Primary sources beat summaries, always.** An agenda title is written to be uncontroversial;
  the staff report is where the substance is. If you flag an item without opening its attachments,
  say so in the brief.
- **Cache every primary source you rely on** (`curl -sL -A "<browser UA>"`, then
  `pdftotext -layout`), so the work reproduces if a document moves.
- **Name what you could not verify**, every time — unread attachments, unpublished agendas, dead
  links.

## If a finding is challenged

Treat it as a research task, not a debate. Go and check. If the challenge is right, say so
directly, fix the root cause rather than the sentence, and add a note naming the earlier version
as wrong so anyone holding an old copy knows.

## Gotchas

See `README.md` for the full list. The ones that bite hardest:

- **Vancouver WA is not Vancouver BC. Clark County WA is not Clark County NV.** Every search
  silently returns the wrong one. Always qualify.
- **A Vancouver `agendaId` exists long before the agenda does** — item count is the test, not the
  id.
- **Clark County's Sunday-dated rows are not meetings**, they are the Weekly Calendar for the week
  ahead.
- **Vancouver's `fiscalImpactSummary` is empty on the public API** — a blank field is not evidence
  of no fiscal impact.
