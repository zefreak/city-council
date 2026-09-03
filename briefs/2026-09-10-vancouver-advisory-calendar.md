# Vancouver — the meetings with no agenda yet, 10–23 September 2026

Everything on the City's CivicClerk calendar past the 8 and 9 September meetings, checked directly
against `Meetings/{agendaId}` on 2 September 2026. Rather than nine three-line files, they are here
together.

## Bottom line

Nothing to act on yet, but one date is worth putting in a diary: the **Culture, Arts and Heritage
Commission meets 10 September**, which is where the minutes of its 25 August special meeting —
the one that retained a law firm on an uncapped hourly agreement — should be approved. An earlier
brief said no further CAHC meeting was on the calendar through 25 September. **That was wrong**:
the meeting was added, and it now carries an agendaId.

## The state of the calendar

| Meeting | Date | agendaId | Items | State |
|---|---|---|---|---|
| **Culture, Arts & Heritage Commission** | Thu 10 Sep, 4:30pm | 1204 | 0 | Agenda not published |
| **City Council** | Mon 14 Sep, 4:00pm | 1084 | 0 | Agenda not published — due ~8–9 Sep |
| Urban Forestry Commission | Wed 16 Sep, 6:00pm | 0 | — | No agenda; id not yet assigned |
| **Downtown Redevelopment Authority** | Thu 17 Sep, 11:00am | 1198 | 0 | Agenda not published |
| City Center Redevelopment Authority | Thu 17 Sep, 12:30pm | 0 | — | **Cancelled** ("Canceled" on the calendar) |
| City Council | Mon 21 Sep, 4:00pm | 1085 | 0 | Agenda not published |
| Planning Commission | Tue 22 Sep, 4:30pm | 0 | — | No agenda; id not yet assigned |
| Civil Service Commission | Wed 23 Sep, 8:00am | 0 | — | No agenda; id not yet assigned |
| **Parks & Recreation Advisory Commission** | Wed 23 Sep, 4:00pm | 1205 | 0 | **Special meeting & retreat**; agenda not published |
| Transportation and Mobility Commission | Tue 1 Sep, 4:30pm | 0 | — | **Cancelled** — has now passed |
| Lodging Tax Advisory Committee | Wed 9 Sep, 12:00pm | 0 | — | **Cancelled** |

A non-zero `agendaId` with zero items means an id has been reserved and nothing published. A
cancellation is recorded only by appending it to the event name — there is no flag and no notice
document, and both spellings ("Cancelled" and "Canceled") are in use.

## Watch

### Culture, Arts and Heritage Commission, 10 September — the follow-up on the law firm

The 25 August special meeting voted on retaining **Madrona Law Group** as general counsel at
$340/hour for the lead attorney, on an agreement with **no cap and no end date**. See
`briefs/2026-08-25-vancouver-culture-arts-heritage-commission.md`. Three things were unresolved
there and all three are answerable at this meeting: **whether the motion passed**, **whether the
agreement has been executed** (the packet copy had blank signature lines), and **whether the
engagement letter's description of the Commission as "a public development authority" is correct**
— the City's own website does not list it as one, and a PDA is a separate legal entity that can
hold money, contract and sue.

This Commission takes public comment on **any issue** at every meeting, three minutes, written
comment to parksrecculture@cityofvancouver.us by **5pm the day before** — so **5pm Wednesday
9 September** for this one. Four of its eleven seats were vacant as of 25 August, including the
Vice President.

### City Council, 14 September — the agenda is due this week

Vancouver Council agendas post about a week out, so the 14 September agenda should appear around
**8–9 September**, which the next scheduled run of this watch will catch. The two things to look
for: whether the **Title 20 / HB 1491 affordability ordinance** appears (the Planning Commission
presentation puts the Council hearing on **12 October**, so 14 September would be early), and what
lands on **consent**. Consent items pass as a block with no debate unless a councilmember pulls one.

### Downtown Redevelopment Authority, 17 September

Flagged for what the body is, not for anything on an agenda — there is no agenda. It is an actual
public development authority and it moves land. Worth checking when the agenda posts.

### Parks & Recreation Advisory Commission, 23 September — a special meeting and retreat

New on the calendar since the last brief. A **retreat** is the format in which advisory bodies set
priorities for the year with the least public attention on them, and this one carries a reserved
agendaId with nothing in it. Note the timing against Clark County's Parks and Nature CIP work
session requested for 14 October — different jurisdiction, different parks, but the same budget
season.

### Two more cancellations

The **Lodging Tax Advisory Committee** cancellation on 9 September makes it two in a row for that
body. RCW 67.28.1817 requires a municipality to submit proposed lodging-tax uses to its LTAC for
comment before acting, and award recommendations have to happen somewhere in the budget calendar.
The **City Center Redevelopment Authority** cancellation on 17 September is the same day as the
Downtown Redevelopment Authority meeting that is going ahead. **Both flagged from calendar entries
alone — no agenda was published for either, so I do not know what was scheduled to be on them.**

Counting from 25 August: Planning Commission (25 Aug), Transportation and Mobility Commission
(1 Sep), Lodging Tax Advisory Committee (9 Sep) and City Center Redevelopment Authority (17 Sep) —
**four Vancouver advisory meetings cancelled in under a month**, none with a published reason. It is
still more likely to be late-summer quorum trouble than anything else, and it is now enough of a
pattern to keep counting.

## Money and land

Nothing. No agendas, no attachments, no figures anywhere in this set.

## What I could not check

- **Everything substantive.** No agenda is published for any meeting listed here, so there are no
  staff reports and no attachments. Every line above is from the CivicClerk calendar entry and the
  API's `agendaId` and item-count fields.
- **Why any of the four meetings were cancelled.** No notice or reason is published for any of them.
- **Whether the Lodging Tax Advisory Committee has allocations pending**, and when it next sits —
  no rescheduled date appears through 28 September.
- **What the Parks & Recreation Advisory Commission retreat will cover.**
- Anything after 28 September; the calendar was queried 30 days ahead.
