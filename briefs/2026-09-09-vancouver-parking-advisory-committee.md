# Vancouver Parking Advisory Committee — Wednesday 9 September 2026, 8:00am

City Hall, Aspen Room, 415 W. 6th St, Vancouver WA · virtual link and call-in on the agenda.
Members: Jocelyn Cross, Ryan Morin, Jason Cromer, Jonathan Wheeler, Garret Ginter.
Agenda cached at `data/vancouver/2026-09-09-pac/pac-agenda-2026-09-09.pdf`
(CivicClerk agendaId 1203, fileId 3008).

## Bottom line

**Public comment here is open on any issue and the sign-up deadline is 5pm Tuesday 8 September** —
the same evening as the Planning Commission's HB 1491 hearing, which turns on parking minimums near
transit. Two agenda items, both about enforcement and code, and **no packet is published**, so
neither can be assessed from a document.

## Act on this

### Public comment — pre-register by 5pm the day before

Three routes, all with the same deadline, all through Callie Taylor:

| Route | How | Deadline |
|---|---|---|
| Written | Email name, address, contact and comments to callie.taylor@cityvancouver.us | **5pm Tue 8 Sep** |
| Remotely | Pre-register by phone 360-487-8650 or the same email | **5pm Tue 8 Sep** |
| In person | Pre-register as above, or fill out a form before Community Communications starts | At the meeting |

Three minutes. The agenda's Community Communications note says "**the public is invited to speak
regarding any issue**" — this is not restricted to agenda items, which makes an 8:00am advisory
committee a live route for anything parking-adjacent.

Note the email domain: `@cityvancouver.us`, without the "of". That is what the agenda prints, three
times. The Planning Commission's address is `@cityofvancouver.us`. If a comment bounces, that is
why.

## Watch

### Item 5 — Parking Scofflaw Program

Presented by Tyler Lund, Parking Project Coordinator, and Austin Douglas, Lead Parking Officer.
**Flagged from the agenda line alone — there is no attachment and no packet, so what the programme
is, is not on the public record.** "Scofflaw" programmes elsewhere typically mean escalating
enforcement against vehicles with accumulated unpaid citations: boot, tow, impound.

If that is what this is, it is worth attention for a specific reason rather than a general one.
Towing and impound convert an unpaid parking fine into loss of the vehicle and then into
storage fees that exceed the original debt — a mechanism that falls on people who cannot pay the
first ticket, and that in Vancouver intersects directly with vehicle residency. **What to ask for:
whether there is an ability-to-pay determination, a payment-plan route that halts escalation, and
an exemption or protocol for vehicles someone is living in.** That is a concrete question with a
yes/no answer, and asking it before a programme is designed is worth more than objecting after.

The presence of the Lead Parking Officer alongside the Project Coordinator suggests enforcement
rather than policy design, but that is an inference from a staffing line, not a finding.

### Item 4 — Parking Code Review & Update

Gabriel Montez, Parking District Manager. A presentation is listed as an attachment but the packet
is unpublished, so it is unavailable. **Flagged on the agenda line alone.**

The timing is the reason to care. The day before, on 8 September, the Planning Commission holds its
public hearing on Title 20 changes for HB 1491 compliance — a law whose mandated offsets include
**eliminating off-street parking requirements** for residential and mixed-use projects within a
quarter mile of all 51 Vine BRT stations. A parking code review running one day behind that hearing
either implements it, works around it, or does not touch it. Which of the three is not knowable
from the agenda. See `briefs/2026-09-08-vancouver-planning-commission.md`.

## Money and land

Nothing published. Vancouver's `fiscalImpactSummary` field is empty on the public API as a matter
of course, and with no packet there are no attachments to read. **A blank field is not evidence of
no fiscal impact** — a scofflaw programme has revenue and cost sides, and neither is available.

## Noted

Call to order and roll call · public comment · approval of the 12 August 2026 minutes (attachment
listed, not published) · adjournment. The API reports `enablePublicSpeakerSignup` and
`enableWrittenComment` both **false** for this meeting, which contradicts the agenda's own
instructions — those flags govern the City's online sign-up widget, not the committee's practice,
and the agenda's email and phone routes are the operative ones.

The meeting file is named "September 8, 2026 PAC Agenda" in the API while the agenda itself, the
calendar entry and the item list all say **9 September**. Treat 9 September as the date.

## What I could not check

- **The entire packet.** `agendaPacketIsPublish` is **false** as of 2 September (queried directly
  against `Meetings/1203`; the digest's change-detection does not resurface a meeting when the
  packet flag flips, so this has to be re-checked by hand). Both substantive items are flagged from
  their agenda lines.
- **What the Parking Scofflaw Program actually proposes** — no document exists publicly.
- **The 12 August 2026 minutes**, which would show what this committee has already discussed.
- **Whether the Parking Code Review touches HB 1491's parking-minimum elimination.** Not knowable
  until the presentation posts.
- Whether the committee has any decision authority here or is purely advisory to Parking Services.
