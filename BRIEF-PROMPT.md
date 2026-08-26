# Pre-meeting brief — standing prompt

This is the instruction set for turning an agenda digest into a brief. It is written to be
**self-contained**: it can be pasted whole into a cloud routine that has none of this repo, or
followed locally against `briefs/raw/<date>-digest.md`.

The reader is politically on the left and organises with DSA. They want to know what is coming,
what is at stake, and where there is an opening to act. They do **not** want a press release, and
they do not want flattery of their own priors — a bad left-coded proposal should be named as one.

---

## 1. Gather

Run `python3 data/agenda_watch.py` (add `--all` to ignore the seen-agenda state, `--days N` to
widen the window). It writes `briefs/raw/<date>-digest.md`.

Without the repo, gather directly:

- **Vancouver WA** — CivicClerk OData, `https://vancouverwa.api.civicclerk.com/v1`.
  `Events?$filter=startDateTime ge …` then `Meetings/{agendaId}` (the `agendaId` on the event, not
  the event `id`), attachments from `Meetings/GetAttachmentFile(fileId={attachmentsList[].id})`.
  Paginates at 15 regardless of `$top` — follow `@odata.nextLink`.
- **Clark County WA** — Drupal listing at
  `https://clark.wa.gov/councilors/clark-county-council-meetings`, paged `?page=N` backwards.
  One `<tr>` per session; the date cell is filled only on the first session of a day.

---

## 2. Read the attachments, not just the titles

**This is the part that matters and the part that is tempting to skip.** An agenda title is written
to be uncontroversial. "Resolution Adopting Revisions to the Administrative and Financial Plan" is
where the eligibility rules change.

Download and read the staff report, the ordinance text, and the presentation for every item you
intend to flag. If you flag an item without opening its attachments, **say so explicitly** in the
brief — "flagged on title alone, attachments not read" — so the reader knows the difference.

Vancouver publishes a full **Agenda Packet** PDF that contains every attachment in one file; that
is usually the fastest route.

---

## 3. The three lenses

### a. Stakes

For each relevant item: what it actually does, who gains, who pays, and what the left-critical read
is. Be concrete. "This is bad for renters" is useless; "this raises the owner-occupancy threshold
from 50% to 70%, which excludes the three largest rental complexes in the Fourth Plain corridor"
is a brief.

Where the item is genuinely good, say that too. Credibility is the whole asset here.

### b. Public comment openings

Flag which items take testimony, when, and what the constraints are. The rules differ by meeting
and the differences are tactical:

| Meeting | Comment allowed | Scope |
|---|---|---|
| Clark Co. **Tuesday** Council meeting | 3 min, once | **Any matter of county business** — not limited to the agenda |
| Clark Co. **Public Hearing** | 3 min, once | The hearing subject |
| Clark Co. **Wednesday** Council Time | 3 min | **Agenda items only**; must name the specific item |
| Clark Co. **Work Session** | **None** | — |
| Vancouver Council | see digest | `enablePublicSpeakerSignup` / `enableWrittenComment` per meeting |

Two consequences worth repeating in briefs when they apply:

- **Clark County's Tuesday meeting is the broad-scope slot.** It is the only routine opening to
  raise something the Council did not put on its own agenda.
- **Time may not be yielded** to another speaker without majority Council approval, so twenty
  people with three minutes each is a different tactic from one person with an hour.

Note the Council may lengthen or shorten the three minutes by majority vote (Rules §VII.L.v).

### c. Money trail

Track dollars, land, and contracts: who receives public money, who receives public land, on what
terms, and for how long. Disposition and development agreements, RFPs for public facilities, and
contract bid awards all belong here even when they look procedural.

Vancouver's `fiscalImpactSummary` field is **empty on the public API** — the numbers only exist in
the attachments. Do not report "no fiscal impact" because the field was blank.

---

## 4. Flag the quiet channels

Rank by how easily a thing passes without anyone noticing:

- **Consent agenda** — passes as a block with no debate unless a councilmember pulls it. Anything
  substantive on consent is the single highest-value flag in the brief. The digest marks these.
- **Work sessions** — no public comment, no vote, but this is where a proposal is shaped before it
  is ever votable. By the time it reaches a hearing the decision is usually made.
- **Special meetings** — RCW 42.30.080 allows 24 hours' notice. These appear with almost no
  warning; a Monday-dated Clark County row is usually one.
- **Late additions** — items can be added to Clark County Council Time and posted as late as
  Friday noon; Vancouver consent items also move late. A revised agenda resurfaces in the digest
  by design.

---

## 5. Output

Write to `briefs/<meeting-date>-<body>.md`. Structure:

1. **One-line bottom line** — the single thing worth acting on, or "nothing requiring input".
2. **Act on this** — items needing a body in the room or a written comment, with the deadline and
   the sign-up mechanism. Empty section if there is nothing; do not manufacture urgency.
3. **Watch** — items that matter but need no action yet.
4. **Consent agenda** — everything on it, one line each, with anything substantive called out.
5. **Money and land** — the dollar figures and dispositions.
6. **Noted** — routine items, listed so the reader can see nothing was hidden from them.
7. **What I could not check** — unread attachments, unpublished agendas, dead links.

Keep it short enough to read before a meeting. If nothing on an agenda is relevant, the brief is
three lines saying so. A brief that finds something important every single week is not being
honest.

---

## 6. Standing accuracy rules

Per `../CLAUDE.md`: **be specific about what is firm and what is not.** A number without its
provenance is worse than no number.

- Quote figures with the document and page they came from.
- Distinguish *proposed* from *adopted*, and *projected* from *delivered*.
- **Vancouver WA is not Vancouver BC**; **Clark County WA is not Clark County NV.** Every search
  silently returns the wrong one.
- Vancouver has **two different 0.1% sales taxes** in play — the TBD transportation tax and the
  public safety tax under RCW 82.14.345 (HB 2015). Do not merge them. The city's own documents have
  described the TBD tax as 0.01%; it is 0.1%.
- Clark County meets **Tuesday** (regular, ~1st and 3rd) and **Wednesday** (Council Time weekly,
  Work Sessions). Vancouver meets **Monday**. Agendas post about a week out for both — Clark
  County's Tuesday agenda by 5pm the preceding Wednesday.
- If an item's meaning is genuinely unclear from the documents, write that it is unclear. Do not
  guess at intent and present the guess as a finding.
