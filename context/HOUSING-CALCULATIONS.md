# Calculation index — Vancouver WA housing

Every derived number in this project: what it is, how it was computed, what went into it, which
script produces it, and where it appears. For auditing.

**Two kinds of number, checked differently:**

- **Transcribed literals** — copied from a source. Check against the cited document.
- **Derived values** — computed from literals. Check the arithmetic.

All scripts are pure stdlib and take no arguments. Re-run any of them to reproduce the values in
the "Value" column verbatim.

```bash
python3 data/vancouver-wa/capacity_model.py        # Part I
python3 data/vancouver-wa/subsidy_model.py         # Part II
python3 data/filtering/filtering_model.py          # Part III
python3 data/social-housing/alternatives_model.py  # Part IV
python3 data/international/comparators_model.py    # Parts V–VI
python3 data/vancouver-wa/fetch_council.py         # refresh the council record
python3 data/make_audit_shared.py                  # regenerate audit-shared.html
```

---

## Part 0 — the city's own record

Transcribed from Vancouver's council materials. These are **literals**: check them against the
document, not the arithmetic. No script produces them — they were read from the PDFs, which are
cached under `data/vancouver-wa/`.

| # | Value | Source | Page | Doc | Artifact |
|---|---|---|---|---|---|
| 0.1 | **8 projects / 630+ units** stalled, 0–60% AMI | AHF workshop deck, 10 Aug 2026 | p.5 | §0 | Part I callout |
| 0.2 | **$20.4M** committed but unspent | AHF workshop deck | p.5 | §0 | Part I callout |
| 0.3 | **$0** Housing Trust Fund awards 2025 | 2025 Housing Report | p.3 | §0 | tile, Part I |
| 0.4 | ConPlan rental units added **0 / 0 / 0** (goal 100) | 2027 HUD Priorities deck, 17 Aug 2026 | slide 4 (PDF p.5) | §0 | Part I table |
| 0.5 | goal of 100 = **0.5%** of sub-80% need (derived: 100 ÷ 18,700) | 0.4 ÷ 2.2 | — | §0 | Part I callout |
| 0.6 | AHF restructure **80→40** units/yr; caps **$75k→$150k**, **$100k→$200k** | AHF workshop deck | p.9 | §0 | Part I table |
| 0.7 | **$3M** revolving pre-development loan pool, from program income | AHF workshop deck | p.11 | §0 | Part I table |
| 0.8 | City of Vancouver as an **eligible AHF recipient** | AHF workshop deck | p.12 | §0 | Part I |
| 0.9 | Site P: **99-yr ground lease**, all units **≤80% AMI**, rent discounted 40 yrs | Heights Site P DDA, 17 Aug 2026 | §3.2 | §0 | Part I |
| 0.10 | **18 housing prototypes** behind the capacity figure | Appendix O | p.2 | §3 | Part II callout |
| 0.11 | "sizable gap financing" required | Appendix D (ECOnorthwest HNA) | p.59 | §0 | Part I |

**The one to scrutinise:** 0.1 and 0.2. Both are a director's spoken framing captured in a slide
deck, not a project-level schedule. The project list that would confirm the unit count and the
expiry dates has not been published; the 24 August and 14 September agendas were still empty
shells when this was compiled.

---

## Part I — capacity vs production
`data/vancouver-wa/capacity_model.py`

| # | Value | Formula | Inputs & source | Line | Doc | Artifact |
|---|---|---|---|---|---|---|
| 1.1 | **1,733 /yr** required | `TARGET_UNITS / YEARS` | 38,129 ÷ 22. Target: Our Vancouver 2045 Ch.4 (transcribed). Years: 2045−2023 | 36–37 | §1 | tiles, Part I |
| 1.2 | Permit series 2010–25 | parsed from cached BPS files | Census BPS place files, cols 18/21/24/27 summed | 55–79 | §2 table | Part I chart |
| 1.3 | **1,103 / 1,366 / 1,524 / 1,112** /yr | arithmetic mean of 1.2 over each window | BPS totals | 82–84 | §2 | Part I table |
| 1.4 | **2,403** best year (2021), **771** in 2025 | max / lookup of 1.2 | BPS | 133–135 | §2 | Part I |
| 1.5 | 64% / 79% / 88% / 44% of need | 1.3 ÷ 1.1 | — | 145 | §2 | Part I table |
| 1.6 | **+27% / +14% / +125%** uplift | `1.1 / 1.3 − 1` | — | 196–203 | §2 | Part I |
| 1.7 | **32.3 / 28.9 / 18.4** years to absorb | `ZONED_CAPACITY / rate` | 44,112 (Ch.4 Table 5, transcribed) | 186–189 | §3 | Part I table |
| 1.8 | **2,005 /yr** binding threshold | `ZONED_CAPACITY / YEARS` | 44,112 ÷ 22 | 191 | §3 | Part I |
| 1.9 | **1,794 /yr**, **104%** of need | `(90,780 − 81,809) / 5`, then ÷ 1.1 | WA OFM Apr-1 units, Table 7 (transcribed) | 155–163 | §4 | Part I callout |
| 1.10 | 2045 totals 29,292 / 32,291 / 17,984 | actual 2023–25 + rate × remaining yrs | BPS + 1.3 | 88–92 | §2 | — |

**Watch:** 1.10's "required rate" row gives 36,265 not 38,129 — because 2023–25 actuals (3,335)
are already below 3 × 1,733. That 1,864-unit hole is real, not a rounding error.

---

## Part II — the income-band gap
`data/vancouver-wa/subsidy_model.py`

| # | Value | Formula | Inputs & source | Line | Doc | Artifact |
|---|---|---|---|---|---|---|
| 2.1 | **38,128** total need | `sum(NEED)` | FEIS Ch.3 p.72, seven bands (transcribed). Comp plan Ch.4 Table 3 gave 38,129 | 21–39 | §5 | hero chart |
| 2.2 | **18,700** ≤80% AMI, **49%** | sum of bottom 4 bands ÷ 2.1 | FEIS Ch.3 p.72 | 115–125 | §5 | hero, tiles |
| 2.3 | **12,912** ≤50% AMI, **34%** | 2,651+4,371+5,890 ÷ 2.1 | FEIS Ch.3 p.72 | 126–128 | §5 | — |
| 2.4 | **516 / 94** unfunded per yr | `per_year − delivered_per_year` | Ch.4 Table 6 (transcribed) | 142 | §6 | Part II table |
| 2.5 | **$206.3M / $30.7M** | 2.4 × $400,000 / $325,000 | Ch.4 Table 6 | 143 | §6 | Part II table |
| 2.6 | **$236.9M /yr** | sum of 2.5 | — | 144 | §6, everywhere | tiles |
| 2.7 | **$5.21B** | 2.6 × 22 | — | 153 | §6 | Part II |
| 2.8 | **$1,155 /resident/yr** | 2.6 ÷ 205,100 | WA OFM Apr-2025 pop | 154 | §6 | Part II |
| 2.9 | **$2,727 /unit/yr** | 2.6 ÷ 86,878 | 2023 unit baseline | 155 | §6 | — |
| 2.10 | **$36.5B** assessed value | `(77,388,214 + 10,532,691) / 2.41 × 1000` | 2025 adopted budget lines + published city levy rate | 88–90 | §8 | Part II table |
| 2.11 | **$43.4M /yr** headroom | `(3.60 − 2.41) × 2.10 / 1000` | RCW 84.52.043 | 178–179 | §8 | Part II table |
| 2.12 | **$6.50 /$1,000** needed | `2.6 / 2.10 × 1000` | — | 180 | §8 | Part II table |
| 2.13 | **4.2%** AHF share, **23.7×** multiple | 10M ÷ 2.6; 2.6 ÷ 10M | AHF Admin Plan | 170–175 | §7 | tiles |
| 2.14 | **3.1× / 4.0×** shelter & PSH expansion | 1,374 ÷ 437; (885+2,651) ÷ 885 | FEIS Ch.3 p.72 + Clark County HIC 2026 | 214–222 | §9 | Part II table |

**Derivation to check first:** 2.10. It is the only figure here I derived rather than read.
Cross-check in §8: the City publishes AHF at $122/yr on a median home; at the Dec-2025 median of
$489,995 that implies $0.249/$1,000 against $0.289 derived — a gap consistent with assessment lag.

---

## Part III — filtering
`data/filtering/filtering_model.py`

| # | Value | Formula | Inputs & source | Line | Doc | Artifact |
|---|---|---|---|---|---|---|
| 3.1 | 179 MSA rates | regex parse of the paper PDF text | Liu et al. 2022 appendix Table A1 | 43–66 | §11 | Part III chart |
| 3.2 | **−0.0046** national mean | mean of 3.1 | Liu A1 | 77 | §11 | table footer |
| 3.3 | **+0.0035**, s.e. 0.0004, rank **166/179** | lookup + sort of 3.1 | Liu A1, "Portland, OR" | 72–79 | §11 | Part III |
| 3.4 | **+0.0003** relative-to-median, rank 156 | parse of Table A5 | Liu A5 | 73, 84 | §11 | — |
| 3.5 | **42.2%** Vancouver share of county stock | `86,878 / 206,013` | Vancouver Ch.4 baseline ÷ Clark Issue Paper 5 Table 3 | 115 | §12 | Part III |
| 3.6 | Units crossing below 80% AMI | uniform-within-band ageing, `x·exp(rate·22)` | Clark 2023 supply by band (Issue Paper 5 T3), scaled by 3.5 | 137–155 | §12 | Part III table |
| 3.7 | 33,464 / 7,315 / 6,090 / **0** | 3.6 at each candidate rate | Rosenthal 2014; Liu | 158–163 | §12 | — |
| 3.8 | **+0.0081** Portland owner penalty | `3.3 − 3.2` | — | 232 | §33 | Part III |
| 3.9 | **−0.0169** implied Portland rental | `ROSENTHAL_RENTAL + 3.8` | Rosenthal −0.025 | 236 | §33 | Part III |
| 3.10 | **17,066 / 12,939 / 5,294 / 0** tenure split | `3.6(owner)×0.49 + 3.6(renter)×0.51` | tenure split — FEIS Ch.3 p.72, Census 2023a | 210–222 | §33 | Part III table |
| 3.11 | 91% / 69% / **28%** / 0% of need | 3.10 ÷ 2.2 | — | 244–248 | §33 | Part III table |

**The one to scrutinise:** 3.10. Band shares are assumed identical across tenures — rental stock
is actually concentrated lower, so the renter column is probably overstated. Stated in the
docstring and in §33. Row 3.11's 28% (with 1%/yr real median income growth netted out) is the
most defensible single figure; the 0% in the last row is the retired v1 result, kept visible.

---

## Part IV — closing the gap
`data/social-housing/alternatives_model.py`

| # | Value | Formula | Inputs & source | Line | Doc | Artifact |
|---|---|---|---|---|---|---|
| 4.1 | **$7.6M /yr** HTF per-capita share | `302.5M × 205,100 / 8,115,100` | 2025–27 capital budget; OFM | 122 | §13 | Part IV chart |
| 4.2 | **$12.6M /yr** Seattle scaled | `50M × 205,100 / 816,600` | Prop 1A yield; OFM | 123 | §13 | Part IV chart |
| 4.3 | **$73.6M** stacked, **31.1%** | 10M + 4.1 + 43.4M + 4.2 | — | 130–131 | §13 | Part IV |
| 4.4 | **$9.4B /yr** statewide | `2.8 × 8,115,100` | — | 144–145 | §14 | Part IV callout |
| 4.5 | **31×** vs HTF | 4.4 ÷ 302.5M | — | 150 | §14 | Part IV callout |
| 4.6 | **90** affordable units/yr per $100M | `1,800 / 20` | Montgomery County HPF (projection) | 70 | §15 | Part IV table |
| 4.7 | **$104M / $573M** capital implied | `units_needed / 4.6 × 100M` | 2.4 | 164–165 | §15 | Part IV table |
| 4.8 | **16.4%–26.1%** cost reduction | `1 − (1−fee)(1−loss)` | **Now sourced.** Fee 9.1–13.0% of TDC: WSHFC 2025 Policies §2.6 / WAC 262-01-130(8)(f). Loss 8–15%: Novogradac equity pricing, 92¢ post-TCJA → 85¢ June 2025 | 176–200 | §16 | Part IV |
| 4.9 | Gap **$175.1M–$198.2M**, saving **$38.8M–$61.8M** | GAP × (1−4.8) | — | 177–200 | §16 | Part IV |
| 4.10 | **367** chronically homeless | `178+127+50+12` | Clark County PIT 2026 Parts 1–2 | 90 | §17 | Part IV |
| 4.11 | **$27.3M / $52.2M / $107.7M** all-in | `n×361,221/22 + n×25,000` | WSHFC Clark median TDC; Whatcom PSH op | 206–212 | §17 | Part IV chart |
| 4.12 | **$19.4M / $37.2M / $76.8M** at $13k op | same, `PSH_OPERATING_LOW` | published low end | 212 | §17 | Part IV figcaption |
| 4.13 | **9,851–10,515** severely burdened renters, **8×** PIT | `86,878 × occ × 0.49 × 0.26` | ACS 2023 B25091 via Ch.4. Occupancy run at 89% and 95%; **conclusion is 8× either way** | 219–224 | §18 | Part IV callout |

| 4.14 | **~$16.9M/yr** committed revenue = **7.2%** of gap | $10M AHF + ~$7.0M HB 1590 sales tax | HB 1590 tax adopted Nov 2020; yield proxied by the city's identically sized TBD 0.1% sales tax, $6.95M in 2024 | 300–320 | §18b | Part IV½ |
| 4.15 | Bonding **$261M / $130M** | annuity PV at 5% over 30 yrs | 4.14 | 322–330 | §18b | Part IV½ table |
| 4.16 | **847 / 630** homes from $261M | 4.15 ÷ per-unit cost | WSHFC FY2025: acq/rehab $307,625, new build $413,776 | 330–334 | §18b | Part IV½ table |
| 4.17 | Acquisition **26% cheaper**; land **9%** of TDC | $307,625 vs $413,776; cost-category share | WSHFC FY2025 cost data | 336–344 | §18b | Part IV½ table |

**Both former assumptions here are now sourced.** 4.8's two inputs come from the WSHFC policy
and Novogradac equity pricing; 4.13's occupancy is run as a 89%–95% sensitivity and the finding
holds at both ends. Occupancy is the last input in this model without a clean primary source.

---

## Parts V–VI — comparators and from-scratch
`data/international/comparators_model.py`

| # | Value | Formula | Inputs & source | Line | Doc | Artifact |
|---|---|---|---|---|---|---|
| 5.1 | **2.12×** Vienna leverage | `530M / 250M` | two *different* secondary sources | 61 | §20 | Part V table |
| 5.2 | **$301 /resident/yr** Vienna | `530M × 1.08 / 1.9M` | EUR/USD 1.08 assumed | 62 | §20 | Part V table |
| 5.3 | **3.8×** Vancouver vs Vienna | 2.8 ÷ 5.2 | — | 386 | §20 | Part V |
| 5.4 | **$4.34 /resident/yr** Finland HF | `270M × 1.08 / 12 / 5.6M` | ARA/Y-Foundation programme capital | 89–90 | §21 | Part V table |
| 5.5 | **$255 /resident/yr** Vancouver HF | `52.2M / 205,100` | 4.11 | 94 | §21 | Part V table |
| 5.6 | **59×** | 5.5 ÷ 5.4 | — | 411 | §21 | Part V table |
| 5.7 | **$337B** WA covered wages | `3,544,556 × 95,160` | WA ESD 2024 | 165 | §25 | Part VI figcaption |
| 5.8 | **$12.65B** Clark wages | `180,400 × 70,111` | WA ESD Clark County profile | 185 | §25 | Part VI figcaption |
| 5.9 | **$70.1M / $126.5M / $3,373M** at 1% | 1% of jobs-in-Vancouver / Clark / WA wages | 5.7, 5.8, 100,000 jobs (Ch.4 T1) | 455–460 | §25 | Part VI chart |
| 5.10 | **30% / 53% / 36%** of gap | 5.9 ÷ 2.6 (or ÷ 4.4 for statewide) | — | 460 | §25 | Part VI table |
| 5.11 | **240,925** employed residents → **$169M** | measured × 70,111 × 1% | **No longer assumed.** WA ESD Clark County profile: labour force 252,007, employed 240,925 | 184–186, 469 | §25 | Part VI chart |
| 5.12 | Grant stock plateau **24,400** | `610 × min(year, 40)` | 2.4; AHF 40-yr covenant | 210–212 | §27 | Part VI chart |
| 5.13 | Endowment **41,822 / 67,686 / 119,414** | 610 × leverage ramped 1.0→2.12 over 30 yrs | 5.1 | 215–224 | §27 | Part VI chart |
| 5.14 | Sweden net **600,000**, **20%** of stock | `1,000,000 − 400,000`, ÷ 3,000,000 | Gowan & Cooper | 357 | §24 | Part V table |
| 5.15 | **25.9M** US-equivalent | `129.3M × 600,000 / 3,000,000` | US stock 2007 | 362 | §24 | Part V table |

**5.1 is now primary-sourced and partly corrected.** The *Berichtsstandard Wohnbauförderung 2023* (p.6) confirms the 1% levy but shows it is **no longer hypothecated** (dedicated transfers ended in the late 2000s; the 2018 *Finanzausgleich* made it a general *Länder* tax) and that the €1.4bn of loan repayments is **Austria-wide, not Vienna's**. The €250M/€530M Vienna split, and therefore the 2.12× leverage, remain secondary-sourced.

**Other weak inputs:**
5.2 (a fixed
1.08 EUR/USD). All three are flagged in §29–30 and in the artifact's source review.

---

## Corrections found while compiling this index

- **Vienna's levy is not hypothecated.** Fetching the Austrian primary source while adding audit
  links showed that an earlier draft's "earmarked and not divertible" was wrong, and that the
  €1.4bn loan-repayment figure is national rather than Vienna's. Corrected in both models, both
  analysis documents and both artifacts. The revolving mechanism survives; the ring-fence does not.
- **$7.7M → $7.6M** (4.1) and **$73.7M → $73.6M** (4.3). These were computed before WA
  population was corrected from 8,060,500 to 8,115,100 and were not re-propagated to the
  analysis doc and artifact. Both now fixed; the percentages (3.2%, 31.1%) are unchanged.
- **Owner and renter shares were transposed** (3.10, 3.11). The filtering model had Vancouver at
  51% owner / 49% renter. The Final EIS, Ch.3 "Current Home Ownership" (PDF p.97, printed p.72),
  is explicit: *"Approximately 51% of Vancouver residents rent their homes, while the remaining
  49% own their homes"* — and notes the renter share is far above Clark County (33%) and
  Washington State (36%). Because the rental channel is the one that delivers low-income
  affordability, the error ran **optimistic**. Corrected, the filtering range moves from 27–88%
  to **28–91%** and the central estimate from 5,086 to **5,294** units. Fixed in the model, the
  artifact, the audit and this index. Anyone holding a copy dated 11 August or earlier has the
  transposed figures.
- **The Final EIS revised two income bands** (2.1, 2.2, 2.3, 2.14). Supportive housing
  2,600 → **2,651** and below-30% AMI 4,423 → **4,371**, with emergency shelter beds
  1,405 → **1,374**, "to better align with the final Clark County housing allocations". The
  sub-80% AMI total moves by a single unit, 18,701 → 18,700, so no conclusion changes. Note the
  other five bands were **not** revised — the FEIS says they still reflect the 2024 HNA run
  through Commerce's HAPT, so the seven bands are not all the same vintage.
- **The Final EIS is internally inconsistent on the total.** Its narrative still says "at least
  38,129 new housing units" while its own revised band list sums to **38,128**. The city revised
  the bands without restating the headline. Immaterial, but check the bands rather than the
  headline.
- **Three audit links pointed at files that were not in this project.** `audit.html` referenced
  the OECD and Hong Kong sources by paths that only resolved inside `public-housing/`. Own copies
  are now cached under `housing/data/oecd/` and `housing/data/asia/`, per the rule that each
  project folder must be portable on its own.
- **`audit-shared.html` had drifted from `audit.html`** and was missing rows. It is now generated
  from it by `data/make_audit_shared.py` rather than maintained by hand.
