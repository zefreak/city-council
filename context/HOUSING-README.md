# Vancouver WA — housing analysis

Companion to `../roads/`. Same city (Vancouver, **Washington** — always qualify searches with
"WA" or "Clark County"), same method: every source figure transcribed inline as a literal with
a citation, pure-stdlib Python, no network calls at run time, fully portable.

**The question.** How much housing can Vancouver realistically expect to build under the
comprehensive plan adopted 1 June 2026, and how much has to come from social housing, public
development or other non-market schemes to fulfil a Housing First policy that moves people off
the street into permanent housing?

## Status

| Topic | Status | Where |
|---|---|---|
| Zoned capacity vs actual production | **Done** | `HOUSING-vancouver-wa.md` Part I (§1–4) |
| Income-band gap and the subsidy arithmetic | **Done** | Part II (§5–9) |
| Filtering — does the stock get cheaper as it ages? | **Done** — owner channel closed, rental unmeasured | Part III (§10–12) |
| Source review — every claim re-checked | **Done** | Part VII (§32–34) |
| Check against the city's own council proceedings | **Done** — corrects the framing | Part VIII (§32a–32e) |
| Alternative delivery: social housing, public development, Housing First | **Done** | Part IV (§13–18) |
| Seeding a portfolio without a tech-sector tax | **Done** — corrects a Part IV omission | §18b |
| International comparators: Vienna, Helsinki, Singapore, Tokyo, Sweden | **Done** | Part V (§19–24) |
| Designing the tax code from scratch | **Done** | Part VI (§25–27) |
| Appendix P / Final EIS capacity method | **Not started** | Part VIII §29 |
| Middle-housing-specific production | **Not started** | Part VIII §29 |
| Intra-metro (ZIP-level) filtering | **Not started** — biggest open uncertainty | Part VIII §29 |
| Countywide / unincorporated Clark | **Not started** | Part VIII §29 |
| Residence- vs employment-based payroll levy base | **Not started** | Part VIII §29 |

## Read this first if you are close to this work

**Part VIII** checks the analysis against Vancouver's own council proceedings, after a fair
criticism that it was built from documents rather than from the city's process. The record both
confirms and corrects it. The city's housing director, August 2026: *"The affordable housing
pipeline is one of our biggest frustrations. We have **eight existing projects with over 630
units** that cannot move forward"* — stalled on state gap financing, with some city commitments
expiring as soon as May. That is this document's Part II from the inside, and 630 stalled units
against the 610/yr calculated here as unfunded is close enough to state plainly.

**The council record is now machine-readable.** The CivicClerk portal is an SPA, but it talks to
an OData API on a *different host* — `vancouverwa.api.civicclerk.com/v1`, not the portal domain.
`data/vancouver-wa/fetch_council.py` lists meetings, filters agenda items by keyword and downloads
attachments. Part VIII is now written from the **city's own workshop decks**, not from the
reporting, which turned out accurate on every checkable figure and understated two.

**The sharpest fact in the project, from the city's 2025 Housing Report (March 2026):**
*"Despite a strong pipeline of shovel ready projects, **no Vancouver projects received Housing
Trust Fund awards in 2025**."* Part IV priced Vancouver's per-capita share of a record state HTF
at $7.6M/yr and treated it as a floor. **The actual award was zero** — HTF is a competitive
statewide contest, not a share. The same report confirms Part I from the inside (*"fewer than half
of the targeted housing units were completed in 2025"*) and reaches §18b's conclusion first, in
print: achieving the goals *"will likely require... an expanded role for **publicly led and
non-market rate housing development**."*

**Appendix P is found, and it confirms Part II line for line.** Every comp plan appendix lives on
the engagement site's project-documents page (`beheardvancouver.civilspace.io`), *not* the city's
comp plan page, which links only the appendix list — which is why it eluded earlier searches.
Appendix P supplies the derivation the analysis never had: HAPT need of **43,198 units 2020–2045,
less 5,069 built 2020–23 = 38,129**, on Allocation Method A. Every income band matches. Two extras:
existing emergency capacity is **406 beds against 1,405 needed**, and the plan forecasts just
**1,280 ADUs through 2045** from 53,269 eligible lots — under 3% of capacity, so it is *not*
banking on middle-housing uptake.

**The Draft EIS closes the last open flag.** A 14-month agenda sweep found it (12.4MB, Aug 2025).
Capacity **is** feasibility-adjusted — Alternative 1 ≈ 45,100 units *"based on market feasibility
and redevelopment potential"*, the adopted 44,112 sitting just below. And ECONorthwest, the city's
consultant, states Part II's finding directly: lower income bands *"are likely unable to be served
without additional subsidies"* and regulated affordable housing *"typically requires sizable gap
financing."* The DEIS also states **1,733 units/yr** — settling the 1,733-vs-2,500 question: 1,733
is the plan requirement, 2,500 is the separate operational target in the Housing Report.

**From the AHF deck (10 Aug 2026):** $67.6M awarded has been **leveraged with $588.3M** from other
sources — an **8.7× multiple** — supporting 2,034 units including **1,425 at or under 50% AMI**.
Total development cost has gone **$200k → $400k per unit since 2016**, which independently confirms
Part II's central input. Staff verdict: *"Production goals established with levy renewal in 2023
not realistic."* Proposed per-unit limits roughly **double**; a **$3M revolving predevelopment loan
pool funded from program income** is being created; and the plan adds **"City of Vancouver as an
eligible recipient"** — the public-developer move, in one line. Council acts 8/24; **State Housing
Trust Fund applications are due 9/21**.

**On HB 1491, staff's objection is sharper than the headline:** it is *"partially funded
inclusionary zoning"* — 50 years of required affordability against at most 20 years of offset,
where the other incentives are already available citywide. Vancouver has **51 BRT stations on two
Vine routes**, so a law written for Sound Transit light rail lands unusually hard here.

What the record corrects: **the near-term binding constraint is state gap financing, not local
instrument design**; the city's own production target is **2,500/yr** ("the pace needs to double")
against the 1,733/yr used here; the Affordable Housing Fund is **being restructured right now**
(staff propose halving directly supported units from 80 to 40/yr and adding a $3M pre-development
loan pool); and **HB 1491 (2025)** — 50-year affordability near transit — is a new downside risk
that officials call "good intentions but bad policy". None of this is news to city staff. The
analysis is a quantification of a problem the city is already working, not a discovery.

## Source review (latest pass)

Every source was re-checked for counter-evidence. Three claims changed shape, two got firmer,
one was wrong. Full claim-by-claim table in `HOUSING-vancouver-wa.md` Part VII and in the artifact.

| Claim | Standing |
|---|---|
| 1,733/yr required vs ~1,366 delivered | **Firm** — BPS is a full count, Vancouver reports all 12 months, OFM corroborates |
| 44,112 zoned capacity | **Verified** — the Draft EIS shows it is feasibility-adjusted (Alt 1 ≈ 45,100 *"based on market feasibility and redevelopment potential"*) |
| 18,701 units below 80% AMI, no zone reaches it | **Firm** — the city's own tables |
| $236.9M/yr gap | **Firm as arithmetic** — the plan's Table 6 |
| MFTE delivers 195/yr | **Softest number in the plan** — 20% set-aside at ≤80% AMI; JLARC doubts additionality |
| Property tax can't raise it | **Firm** — statutory |
| **Filtering delivers zero** | **Was wrong — now a range of 27–88%** (both studies are owner-occupied only) |
| Portland filters up on owner stock | **Firmer** — independently replicated by AEI, a hostile witness |
| $104M closes the shallow band | **Weakened** — Montgomery County's yield is a projection with one completion |
| Housing First $27–52M/yr | **Conservative** — quoted at the top of a $13k–$25k operating range |
| Vienna $301/resident | **Directionally firm, precisely soft** — leverage ratio inferred from two sources |
| **Finland −68%** | **True to 2022, since reversed** — +11% in 2024, +20% in 2025 |
| 1% payroll levy = $126.5M | **Firm on an employment base** — corrected up from $124.2M ($70,111 avg wage) |

**What the review did not shake:** the plan needs 7,023 units at 0–30% AMI; no zoning produces
them, no filtering scenario reaches them, no revolving fund refinances them, and the city's
entire legal taxing capacity covers 18% of the bill.

## Headline findings

**The unit target is achievable. The affordability composition is not.** Our Vancouver
2026–2045 requires **1,733 units/yr** for 22 years. Vancouver has averaged 1,366/yr over eleven
years, and OFM's unit series says it actually hit **104% of the required rate over 2020–2025
under the old zoning**. A +14% to +27% uplift from a genuine upzoning is plausible. The real
risk to the total is the 2025 collapse to **771 permits — 44% of need, a 49% fall from the 2021
peak** — which is a cost-of-capital problem the plan has no instrument against.

**Capacity was never the binding constraint.** The new map zones for 44,112 units against a
38,129 target — a "surplus" the plan cites as evidence of sufficiency. At the eleven-year
production mean it would take **32 years** to absorb that capacity. Capacity only binds above
2,005 units/yr, a rate Vancouver has never reached in a single year.

**49% of the target has to be below-market, and no zone in the city reaches it.** 18,701 units
at or below 80% AMI. The plan's own Table 4 records the lowest income level served at market
rate in every zoning designation: outside 205 acres of manufactured home park, it is 80% AMI or
above, everywhere.

**The plan prices its own gap at $236.9M/yr and funds 4.2% of it.** Chapter 4 Table 6: 935
below-market units needed annually, 325 delivered by tax credits and MFTE, 610 unfunded, at
$400,000 and $325,000 per unit. That is **$5.21 billion over the plan period**, $1,155 per
Vancouver resident per year, against an Affordable Housing Fund levy of $10M/yr.

**The property tax cannot raise it, as a matter of statute.** RCW 84.52.043 caps the city
regular levy at $3.60/$1,000; Vancouver is at $2.41. Maxing out every remaining dollar of levy
capacity yields **$43.4M/yr — 18% of the need**. The rate required for the full subsidy is
$6.50/$1,000 on top of the current levy, 2.5× the statutory ceiling.

**Filtering: the owner channel is closed, the rental channel is unmeasured.** Rosenthal
(2014) is the number everyone quotes: rental stock filters down 2.5%/yr. Liu, McManus &
Yannopoulos (2022) re-estimate it MSA by MSA: the national average is only **0.42%/yr**, and
~20% of MSAs filter *upward*. Portland–Vancouver–Hillsboro is **+0.35%/yr — 166th of 179 MSAs,
+15.1% over 40 years**. A 40-year-old home here houses a household with *more* real income than
the one that moved in new. At the *national average* rate Vancouver's stock would deliver 6,090
sub-80%-AMI units by 2045. **But both Liu et al. and AEI measure owner-occupied stock only** —
Liu says so on p.11 — and about half of Vancouver's stock is rented. Splitting by tenure gives a
range of **27–88% of the sub-80% need**, not zero. What survives: the owner channel is closed
(replicated by AEI on 2.4M sale pairs, R²=65%); filtering adds no units, only reallocates them;
and **no scenario reaches the 0–30% band**.

**Statewide, the implied subsidy is 31× what Washington has ever appropriated.** Vancouver's
gap is $1,155/resident/yr. Applied statewide that is **$9.4B/yr**. The 2025–27 capital budget's
"record-setting" Housing Trust Fund appropriation is $302M/yr — $37/resident.

**One band is genuinely solvable, one is not.** A Montgomery-County-style revolving public
development fund delivers ~90 affordable units/yr per $100M of revolving capital.
**$104M closes Vancouver's entire 50–80% AMI shortfall** — a single bond issue, no recurring
tax. But a revolving fund has to revolve, and rents at 30% AMI refinance nothing. **The
0–30% AMI band (7,023 units) has no local solution at all.**

**Vienna spends a quarter as much per resident as Vancouver's gap — and houses half its
population.** €530M/yr across 1.9M people is **$301/resident/yr**, against Vancouver's
**$1,155/resident/yr** shortfall. Vienna is not more generous; its spending is *marginal* where
Vancouver's would be *catch-up*, and Vienna **lent** the money and still owns the asset. A €1.4B
revolving loan book turns a €250M levy into €530M of spending — **2.12× leverage**.

**Finland's Housing First costs $4.34/resident/yr and cut long-term homelessness 68%.**
Vancouver's equivalent is $255/resident/yr — 59× more. The mismatch *is* the finding: Finland
buys placements into stock that already exists. **Finland's number is what Housing First costs
after you have solved Part II, not a shortcut around it.**

**Filtering is a policy output, not a law of nature.** Japan taxes and finances buildings as
depreciating consumer durables, written down over 22–30 years and demolished. That is *why* its
stock filters down. Portland–Vancouver's tax code, mortgage market and planning system all treat
a building as appreciating — which is why the measured rate is +0.35%/yr.

**Sweden points both ways, and the cautionary half is about durability, not drift.** The Million
Homes Programme (1965–74) built 1M homes against a 3M stock — a net +20%, equivalent to ~25.9M US
homes in a decade — and a *Planning Perspectives* review found the stock better built than its
Berlin, Madrid, Rome, Paris or UK peers. The dismantling came under Bildt in 1991–93 (housing
ministry abolished, interest subsidies ended, completions troughing at **12,000 units in 1995**);
the municipal share fell **25% → 17% between 1990 and 2010 — before the 2011 Act was even
passed**. That Act was triggered by a property-owners' **state-aid complaint to the European
Commission**, and the Tenants' Union negotiated it to preserve universality at the cost of
cost-rent. **The binding constraint was EU competition law, which has no US counterpart** — so a
Washington social housing developer could be universal *and* subsidised. What survives as a
warning is the **ratchet**: the 1991 voucher reform was *expanded* by the Social Democrats in
1994, and the 2010 care voucher survived 2014–22 intact. **The design lesson is the statutory
asset lock** — Vienna's limited-profit associations have one, Sweden's municipal companies did
not.

**A 1% payroll levy is the only instrument of the right size.** Vienna-style, applied to Clark
County's $12.42B of covered wages, it raises **$124M/yr — 52% of the gap**, 12× the AHF levy and
2.9× all remaining city property tax capacity. Statewide: $3.37B/yr. Two honest objections:
cross-river commuters would escape an employment-based levy, and a flat payroll tax is
regressive in the second-most-regressive state tax system in the country.

**The barriers are tax barriers, not housing barriers.** *Culliton v. Chase* (1933) held income
is "property", barring a graduated income tax; I-747 (2001) caps levy growth at 1%; RCW
84.52.043 caps city levies at $3.60/$1,000; the B&O taxes gross receipts, not profits.
Vancouver's housing element fails on arithmetic settled by voters and judges who were not
thinking about housing at all.

**One European constraint does not transfer, and it helps.** EU competition law treats
subsidising a landlord who serves the general population as potential illegal state aid — that is
what forced Sweden's universality-or-subsidy choice. There is no US analogue.

**Grant vs endowment — and this one needs no new revenue.** The same $236.9M/yr granted against
40-year covenants plateaus at **24,400 units** forever; lent into a permanently-held public
asset it reaches **67,686 by year 60 (2.8×)** and 119,414 by year 100. The load-bearing caveat is
the same as the revolving-fund one: cost-rent financing bottoms out around 50–60% AMI. The
second caveat isn't financial — **an endowment with no statutory asset lock has a sell-by date**.

**Vancouver already levies a housing sales tax I initially missed, and already has a public
developer.** Under HB 1590 a city can levy a **0.1% affordable-housing sales tax councilmanically**;
Vancouver adopted it in November 2020. Proxied by the city's identically sized TBD 0.1% sales tax
(**$6.95M in 2024**), committed housing revenue is **~$16.9M/yr — 7.2% of the gap, not 4.2%**. The
**Vancouver Housing Authority** already holds 175 public housing units and 3,410 vouchers and can
bond. **RCW 39.33.015** lets the city hand over surplus land at no cost — it sold part of the City
Hall lot for **$1** in 2025. Bonding the committed streams at 5%/30yr raises **$261M**, enough for
**847 acquired homes or 630 new builds**. Acquisition runs **$307,625/unit against $413,776 for new
construction — 26% cheaper** — and land is 9% of a new build's cost. The ceiling is honest though:
$261M is about one year of the gap. It seeds a portfolio; it does not close Part II.

**Housing First is the cheap half.** Housing everyone counted in the January 2026 Clark County
PIT (1,260 people, down 18%) in permanent supportive housing costs **~$52M/yr all-in**; just
the 659 unsheltered, **~$27M/yr**. Both are inside the city's unused levy capacity. What is not
affordable is the **~10,500 severely cost-burdened Vancouver renter households — eight times
the entire county PIT count** — that the street population is drawn from. A Housing First
policy without a funded 0–30% AMI pipeline refills the shelters as fast as it empties them.

## Layout

```
README.md                          this file — orientation and status
artifact-housing-vancouver.html    published artifact source (self-contained)
HOUSING-vancouver-wa.md            the analysis; Part V is the continuation roadmap
CALCULATIONS.md                    audit index: every derived number -> script, line, source
audit.html                         interactive check-off list (open from disk)
data/vancouver-wa/
  comp-plan-2026-2045.pdf/.txt     Our Vancouver 2026-2045, adopted 1 Jun 2026, 313pp
  capacity_model.py                Part I — capacity vs production
  subsidy_model.py                 Part II — income bands, subsidy gap, levy capacity
  ahf-admin-financial-plan.*       Affordable Housing Fund plan, adopted 16 Dec 2024
  sepa-comp-plan-update.*          2024 SEPA determination / EIS scoping
data/census-bps/
  bps_we20{10..25}a.txt            Census Building Permits Survey, West Region place files
data/commerce-wa/
  clark-issue-paper-5-*.pdf/.txt   Clark County allocation + HAPT income bands (Tables 3-5)
  wshfc-cost-data-fy2025.pdf/.txt  WSHFC cost data report to the Legislature, FY2024-25
  state-of-state-housing-2025.*    UW WCRER State of the State's Housing 2025
data/filtering/
  filtering_model.py               Part III — stock-ageing model, tenure split
  liu-aea-paper.pdf/.txt           Liu, McManus & Yannopoulos (2022), incl. appendix A1/A5
  liu-aea-2021-slides.pdf/.txt     AEA session slides
  gatech-filtering-white-paper.*   secondary synthesis, Georgia Tech Urban Research 2026
  aei-filtering-2024.*             Peter & Pinto, AEI — a competing (bullish) view
  cmhc-understanding-filtering.*   CMHC research report — Canadian comparison
data/homelessness/
  2026-PIT-Report-Form_*.pdf/.txt  Clark County WA-508 PIT, count date 29 Jan 2026
  2026-HIC-Final.pdf/.txt          Housing Inventory Chart, same date
  20{22..25}-*PIT*.pdf/.txt        prior years
data/social-housing/
  alternatives_model.py            Part IV — sizing the alternatives
data/international/
  comparators_model.py             Parts V & VI — comparators, payroll levy,
                                   grant-vs-endowment stock model
  ppp-social-housing-2022.pdf/.txt Gowan & Cooper, Social Housing in the
                                   United States (People's Policy Project)
```

## Reproducing

```bash
python3 data/vancouver-wa/capacity_model.py       # Part I
python3 data/vancouver-wa/subsidy_model.py        # Part II
python3 data/filtering/filtering_model.py         # Part III
python3 data/social-housing/alternatives_model.py # Part IV
python3 data/international/comparators_model.py   # Parts V & VI
```

All five are **pure stdlib Python 3**. No pandas, no network at run time. The only script that
reads a source file rather than inline literals is `filtering_model.py`, which parses Liu et
al.'s appendix tables straight out of the paper text so the MSA ranking is reproducible; and
`capacity_model.py`, which parses the cached Census BPS place files.

## Gotchas

- **Vancouver WA vs Vancouver BC** — searches silently return BC. Also **Clark County WA vs
  Clark County NV**: PIT-count searches return Las Vegas.
- **The comprehensive plan contradicts itself on unit counts.** Page 4 says 71,649 housing
  units; the housing element uses 86,878 for 2023; OFM counts 90,780 in April 2025. Use 86,878
  — every Chapter 4 calculation is built on it.
- **36,527 is the County allocation, 38,129 is the City's target.** Both correct, not the same
  number. Chapter 4 footnote 23 explains why.
- **Capacity is a stock; production is a flow.** The "5,983-unit surplus" says nothing about
  whether the units get built.
- **Do not add the AHF's 320 units/yr to the plan's 325 units/yr** — they are largely the same
  LIHTC units counted twice.
- **Liu et al.'s appendix Table A4 has the same shape as Table A1.** Any parser must bound A1
  at "Table A2" or it reads squared residuals as filtering rates. An earlier version of
  `filtering_model.py` did exactly that and reported a national filtering rate of +25%/yr.
- **Sign convention: negative = downward filtering** (more affordable). Easy to invert.
- **$400,000/unit is a subsidy, not a cost.** It exceeds Clark County median TDC ($361,221)
  because deep-affordability projects support no debt.
- **PSH is counted in beds in the inventory and units in the plan.** 885 vs 2,600 is not a
  clean ratio.
- **The $3.60/$1,000 city levy cap applies only to cities with a pre-LEOFF firefighters'
  pension fund**; the base cap is $3.375. Headroom at the base cap is $35.1M/yr, not $43.4M.
- **The Sweden section was rewritten after a challenge; the earlier version is wrong.** It
  claimed a structural result and dated the decline to 2011. Both wrong — the decline predates
  the Act, and the Act's trigger was an EU state-aid complaint. Don't quote an earlier copy.
- **Sweden points both ways** — Million Homes success, 1991–2010 dismantling. Quoting either half
  alone misrepresents it.
- **Stockholm's *ombildning* conversions are not quantified**; the 25% → 17% national figure is
  sourced but not decomposed.
- **The Vienna per-capita comparison is spend-against-*gap*, not spend-against-spend.** €530M is
  Vienna's whole housing outlay; $237M is Vancouver's *unfunded* shortfall on top of existing
  spending. Orders of magnitude are meaningful; it is not a like-for-like budget comparison.
- **The 59× Finland ratio is deliberately not like-for-like** — quoting it as "Finland is 59×
  more efficient" inverts the point.
- **Vienna's 2.12× leverage is inferred** by dividing a reported €530M spend by a reported €250M
  receipt, from two different secondary sources. Direction solid, second decimal not.
- **§25 prices an *employment*-based payroll levy** because that is what QCEW supports. Given
  Clark County's cross-river commuting, a residence-based levy would yield materially
  differently. Not estimated.
- **Census API now requires a key** — the ACS figures here come from the comprehensive plan's
  own citations rather than a live pull.
- **The Columbian and OPB block automated fetches** (403 / JS-rendered body). Headlines and
  search-result summaries only.
