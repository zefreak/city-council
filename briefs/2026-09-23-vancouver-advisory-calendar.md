# Vancouver advisory bodies — Wednesday 23 September 2026

> **Overtaken, 23 September 2026 (evening run).** The Parks & Recreation Advisory Commission agenda
> and a 40-page packet were published after this brief was written, and the packet is substantive.
> It shows a countywide Metropolitan Park District expansion being prepared for a possible fall 2027
> ballot. See `briefs/2026-09-23-vancouver-parks-advisory-commission.md`. The "no agenda published
> at all" statement below was true on 22 September and is no longer. The Civil Service Commission's
> packet was still unpublished at 19:05 on the day of the meeting.

Two Vancouver meetings this Wednesday, neither with substantive published material. Recorded so the
reader can see nothing was hidden, not because either warrants attention.

---

## Bottom line

Nothing requiring input. Two thin agendas, one of them a closed-door-in-effect retreat with no agenda
published at all.

---

## Noted

### Civil Service Commission — 8:00am

Agenda published (doc `Agenda 9.23.2026`, fileId 3039); **agenda packet not published**, so no staff
reports or attachments exist for any item. Six items, all structural:

- Call to Order and Roll Call
- Approval of Minutes
- **Community Forum**
- Commission and Staff Reports
- **New Business**
- Adjournment

"New Business" with no packet is the item that could be anything. There is a **Community Forum** slot
despite the API reporting `enablePublicSpeakerSignup: False` and `enableWrittenComment: False` — the
standing gotcha again: those flags report the portal widget, not the body's rules.

The Civil Service Commission governs hiring, promotion and discipline rules for classified City
employees, including police and fire. That makes it more consequential than its agenda looks, and
worth watching when a packet does appear. The 21 September Fire District 5 supplemental ordinance
specified that its seven new positions "shall be made consistent with applicable civil service rules
and personnel regulations", so that work lands here.

### Parks & Recreation Advisory Commission — September Special Meeting & Retreat, 4:00pm

**No agenda published.** A *special meeting* under RCW 42.30.080 needs only 24 hours' notice, and a
*retreat* is the format that produces direction without a vote or a comment slot. This project has
seen the same pattern twice this month — Clark County's 14 September facilitated policy-priorities
retreat, and now this.

There is no way to say what is on it. What makes it worth a line: the City Manager's recommended
2027-28 budget, previewed two days before this meeting, funds a **Parks Comprehensive Plan Update**,
a **Deputy Director for Parks**, **Bagley Park redevelopment**, **Marine Park boat launch dredging**,
park equipment replacement at Bella Vista and Franklin Neighborhood, an **ADA transition plan for
parks projects**, and a **cost recovery study for Parks**. Clark County is simultaneously preparing
its own Parks & Natural Areas Comprehensive Plan and a 2027 parks fee update. A parks advisory
retreat held in that week is not a blank event, whatever the notice says.

"Cost recovery study" is the phrase to watch in both jurisdictions. It is how park fees get raised.

### Planning Commission, Tuesday 22 September, 4:30pm — cancelled

Event name carries "- Cancelled"; `agendaId` is 0. No notice document exists — the City publishes
cancellations only in the event title, in either spelling. Next scheduled sitting 13 October (2nd and
4th Tuesdays).

---

## What I could not check

- **The Civil Service Commission's New Business item.** No packet published; `agendaPacketIsPublish`
  is false. Per the standing gotcha, a packet appearing later will *not* resurface this meeting in
  the digest, because the fingerprint hashes item names only. It has to be re-queried by hand.
- **Everything about the Parks & Recreation Advisory Commission retreat.** No agenda, no packet, no
  materials.
- **The reason the Planning Commission meeting was cancelled.** Never published.
