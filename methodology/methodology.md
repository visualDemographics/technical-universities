# Methodology & Econometric Framework (`methodology/methodology.md`)

## Standard Operating Procedure for Cross-Continental University Benchmarking

This monograph documents the theoretical architecture, accounting boundary standardizations, denominator alignments, econometric models, and causal waterfall decompositions applied across the **9 leading technical universities** (**MIT, Caltech, Georgia Tech | Imperial College London, ETH Zurich, TUM | Tsinghua University, KAIST, NTU Singapore**).

---

## 1. Institutional Selection Rationale & The $3 \times 3$ Comparative Cohort

To conduct a descriptive and structural benchmarking of elite technical universities across North America, Europe, and Asia, institutional selection must balance **geographic symmetry** with **archetype diversity**:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 $3 \times 3$ REGIONAL MATRIX                            │
│  REGION        ELITE PRIVATE / BOUTIQUE      FEDERAL / PUBLIC CORE      MASS INNOVATION FLAGSHIP│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  UNITED STATES MIT (Private Endowment)       Caltech (Pure Boutique)    Georgia Tech (Public)   │
│  EUROPE        Imperial (UK Anglo-Saxon)     ETH Zurich (Swiss Federal) TUM (German Excellence) │
│  ASIA          NTU Singapore (City-State)    KAIST (National Institute) Tsinghua (China C9)    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **United States**:
   - **MIT**: The global archetype of the private research endowment ($>\$24\text{B}$ endowment, $\$5.07\text{B}$ gross revenue), integrating major on-campus basic science with national defense research.
   - **Caltech**: The ultra-compact boutique institute ($\sim 2{,}400$ total students, 3:1 student-to-faculty ratio) managing NASA's Jet Propulsion Laboratory (JPL).
   - **Georgia Tech**: The premier public STEM flagship ($\sim 53\text{k}$ total enrollees), offering an exact structural counterpart to European mass-enrollment institutions and pioneering mass-scale online graduate education (OMSCS).
2. **Europe**:
   - **ETH Zurich**: The continental European gold standard of public federal funding ($\sim 70\%$ direct federal core funding, $\sim 26\text{k}$ students), balancing world-class basic research with high accessibility and low tuition.
   - **Imperial College London**: The high-tuition, research-intensive UK model ($\sim 23\text{k}$ students) operating in a post-Brexit Anglo-Saxon framework with a major clinical medical school and biomedical partnerships.
   - **TUM (Technical University of Munich)**: Germany's top-ranked Excellence University ($>52\text{k}$ students), operating under a tuition-free public mandate (supplemented by non-EU fees in 2024/25) embedded within a massive external research cluster in Garching and Munich.
3. **Asia**:
   - **Tsinghua University**: China's flagship national engineering institution ($>63\text{k}$ students, $\sim 38.6\text{B RMB}$ budget), representing state-directed strategic research and massive domestic STEM talent concentration.
   - **KAIST**: South Korea's specialized national research institute ($\sim 12.3\text{k}$ students), established to drive high-tech industrial development with tuition-free fellowship models embedded in Daedeok Innopolis.
   - **NTU Singapore**: The globally dynamic Asian hub university ($\sim 33.5\text{k}$ core students), characterized by rapid ascent in global rankings, strong English-medium international recruitment, and co-location with Singapore's A\*STAR institutes.

---

## 2. The 3-Tier Accounting Boundary Framework (Pillar 1)

Headline institutional budgets differ fundamentally in statutory reporting boundaries. Failing to harmonize these boundaries results in severe **apples-to-oranges distortions**:

$$\text{Rate}_{u} = \frac{\text{Numerator}_{u}}{\text{Denominator}_{u}}$$

To ensure that the numerator matches the exact scope of student-facing activity, we define three explicit accounting tiers:

### Tier 0: Gross Consolidated Operating Expenditure
- **Definition**: Total headline operating expenditure as reported in statutory consolidated financial statements.
- **Limitation**: Grossly overstates resources at institutions managing non-academic clinical hospitals (**TUM's Klinikum rechts der Isar**: €794.7M) or closed federal defense/aerospace facilities (**Caltech's JPL**: \$2,611.6M; **MIT's Lincoln Laboratory**: \$1,367.2M; **Georgia Tech's GTRI**: \$919.0M).

### Tier 1: Core Academic Budget (ex-Hospitals & Defense FFRDCs)
- **Definition**: Isolates core university instructional and departmental research expenditures:
  $$\text{Core Academic Budget}_{u} = \text{Gross Expenditure}_{u} - \text{Clinical Hospitals}_{u} - \text{Defense/Aerospace FFRDCs}_{u}$$
- **Impact**:
  - Caltech: Drops from $\$3,525.8\text{M}$ to $\$914.2\text{M}$ ($-74.1\%$).
  - MIT: Drops from $\$4,586.2\text{M}$ to $\$3,219.0\text{M}$ ($-29.8\%$).
  - Georgia Tech: Drops from $\$2,718.8\text{M}$ to $\$1,799.8\text{M}$ ($-33.8\%$).
  - TUM: Drops from $\text{€}1,892.9\text{M}$ to $\text{€}1,098.2\text{M}$ ($-42.0\%$).

### Tier 2: Ecosystem-Augmented Student-Facing Budget (The "Garching Rule")
- **Definition**: In continental Europe and parts of Asia, basic research institutes are legally independent from university balance sheets (e.g., Max Planck Society, Helmholtz Association, ETH Domain, IBS, A\*STAR), yet their directors hold joint professorships (*Doppelberufungen*) and directly supervise Bachelor, Master, and Doctoral students:
  $$\text{Augmented Budget}_{u} = \text{Core Academic Budget}_{u} + \sum_{k \in \mathcal{E}_u} \left( \text{Budget}_{k} \times w_k \right)$$
- **Model Calibration & Sensitivity: Academic Integration Weights ($w_k$)**:
  *(Methodological note: While partner institute operating budgets are drawn directly from official audited annual reports, the academic attribution weights $w_k \in [0.25, 0.60]$ constitute a structural model calibration based on joint faculty chairs [Doppelberufungen] and graduate thesis supervision. In compliance with the Responsible Research Protocol, these parameters are classified as `Strukturelle_Modellkalibrierung` and accompanied by explicit $\pm 50\%$ sensitivity intervals in `datasets/university_master_comparison_2024.csv` and visual error bars in Panels A & C.)*
  - **TUM Garching & Munich Cluster** (€971.6M/yr total): MPI for Plasma Physics (IPP, $w = 0.50$), MPI for Extraterrestrial Physics (MPE, $w = 0.50$), MPI of Quantum Optics (MPQ, $w = 0.50$), MPI for Astrophysics (MPA, $w = 0.50$), MPI of Biochemistry ($w = 0.40$), Helmholtz Munich ($w = 0.40$), ESO Headquarters ($w = 0.30$), FRM II / MLZ research reactor ($w = 0.60$), Leibniz Supercomputing Centre (LRZ, $w = 0.50$). Adds **€419.4M** in attributable academic research capacity.
  - **ETH Domain** (CHF 775M/yr total): PSI ($w = 0.45$), Empa ($w = 0.40$), Eawag ($w = 0.40$), WSL ($w = 0.35$). Adds **CHF 326.8M** in attributable research capacity.
  - **MIT Kendall Square**: Broad Institute ($w = 0.35$), Whitehead Institute ($w = 0.40$). Adds **\$356.9M**.
  - **KAIST Daedeok Innopolis**: ETRI ($w = 0.35$), IBS Campus Centers ($w = 0.40$). Adds **KRW 362.5B**.
  - **NTU Jurong Innovation District**: A\*STAR SIMTech/ARTC ($w = 0.35$), RCEs SCELSE/EOS ($w = 0.40$). Adds **S\$178.0M**.

### Double-Counting Resolution & Conservative Tier 2 Lower Bounds
To address the risk of double-counting entities that are physically hosted on university property and whose funding might partially pass through the university general ledger, we classify all 25 partner research institutes into two distinct legal categories:
1. **Legally Independent External Partners (`is_legally_independent = True`)**: Autonomous public/non-profit research institutions with entirely segregated balance sheets, independent governance, and dedicated statutory appropriations:
   - Max Planck Institutes (IPP, MPE, MPQ, MPA, Biochemistry) and Helmholtz Munich
   - European Southern Observatory (ESO) and Leibniz Supercomputing Centre (LRZ)
   - ETH Domain institutes (PSI, Empa, Eawag, WSL)
   - Broad Institute and Whitehead Institute (Cambridge, MA)
   - Francis Crick Institute (London)
   - Electronics and Telecommunications Research Institute (ETRI, Korea)
   - A\*STAR Research Institutes (SIMTech, ARTC, Singapore)
2. **On-Campus Hosted Centers with Potential Internal Consolidation (`is_legally_independent = False`)**:
   - **TUM Research Neutron Source Heinz Maier-Leibnitz (FRM II)** (€72.0M gross): Operated by TUM as a corporate entity with €43.2M ($w = 0.60$) attributable research.
   - **Tsinghua BNRist & State Key Laboratories** (6.5B RMB and 8.0B RMB gross): Key national research labs physically integrated within university departments.
   - **KAIST Institute for Basic Science (IBS) Campus Centers** (KRW 250.0B gross): Dedicated national basic science centers hosted within KAIST departments.
   - **NTU Research Centres of Excellence (SCELSE & EOS)** (SGD 200.0M gross): MOE-funded national centers embedded on campus.

By computing a **Conservative Tier 2 Lower Bound** that includes *only* legally independent external entities:
$$\text{Tier 2}_{\text{Conservative, Indep}} = \text{Tier 1}_{\text{Core}} + \sum_{k \in \mathcal{E}_{\text{indep}}} \left( B_k \times w_k \right)$$
we establish a rigorous sensitivity bound (visualized as lower error whiskers in Panel C) that remains completely unaffected even if internal consolidation were present.

---

## 3. Student Denominator Standardization & The Online Cohort Split

A university's per-student intensity depends critically on the denominator definition:
1. **On-Campus Full-Time Equivalent (FTE) Standard**: Degree-seeking students physically enrolled on campus and utilizing departmental teaching infrastructure.
2. **The Georgia Tech Online Master's Phenomenon**:
   - In Fall 2024, Georgia Tech enrolled **53,350 total students**, of whom **20,850** were enrolled in low-cost online distance Master's programs (OMSCS, OMSA, OMSCyber).
   - Dividing Georgia Tech's campus budget by total headcount yields $\$33.7\text{k}/\text{student}$, understating actual on-campus expenditure.
   - Standardizing by **30,800 on-campus FTEs** establishes the true campus resource intensity: **$\$58.4\text{k}/\text{FTE}$** (Tier 1) and **$\$63.0\text{k}/\text{FTE}$** (Tier 2).
3. **Georgia Tech Online Delivery Cost Cleaning**:
   - Online Master's students pay ~$3,740 per academic year, operating at a cost-recovery rate.
   - Isolating this delivery cost ($\sim \$78.0\text{M}$ for 20,850 online students) from Georgia Tech's Core Academic budget ($1,799.8M) isolates pure on-campus teaching expenditure:
     $$\text{Core}_{\text{On-Campus}} = \$1{,}799.8\text{M} - \$78.0\text{M} = \$1{,}721.8\text{M}$$
     $$\text{Tier 1}_{\text{Clean}} = \frac{\$1{,}721.8\text{M}}{30{,}800\text{ FTE}} = \$55{,}903\text{ / FTE}$$
   - This prevents cross-subsidization distortion while preserving exact per-FTE accounting.
4. **Clinical Medical Student Denominator Sensitivity (TUM & Imperial)**:
   - Universities with clinical faculties face an asymmetry: non-academic hospital expenditures are excluded from Tier 1, but clinical students might remain in the denominator.
   - **TUM**: Of its 51,200 on-campus FTEs, exactly **1,666 students** are enrolled in the clinical phase of human medicine (*Staatsexamen Medizin 2. Studienabschnitt*, TUM in Zahlen 2023, p. 13), fully trained and budgeted within *Klinikum rechts der Isar*. Excluding them raises TUM's core STEM/management resources from **\$30,596 to \$31,623 PPP / FTE** (+3.4%).
   - **Imperial College London**: Imperial's Faculty of Medicine accounts for **4,665 FTEs** (including 2,734 undergraduate MBBS students; Imperial Statistics Guide 2024–25, p. 4). Excluding the medical cohort lifts core STEM/business resources from **\$89,679 to \$113,265 PPP / FTE** (+26.3%).
   - Both variations are explicitly incorporated into Panel C sensitivity bounds.

---

## 4. Currency Normalization: Nominal USD vs. Purchasing Power Parity (PPP)

Comparing nominal exchange rates introduces severe geographic bias. A professor's salary or a lab technician's contract in Beijing (CNY) or Munich (EUR) costs substantially less in nominal USD than in Cambridge, MA (USD) or Zurich (CHF):
- We convert all financial flows using **World Bank International Comparison Program (ICP 2023 / WDI Series `PA.NUS.PPP`)**:
  - Germany: **0.701054 EUR / Int'l \$** (Price Level Index = 75.9)
  - Switzerland: **0.999013 CHF / Int'l \$** (Price Level Index = 113.4)
  - United Kingdom: **0.660709 GBP / Int'l \$** (Price Level Index = 84.4)
  - China: **3.643738 CNY / Int'l \$** (Price Level Index = 50.6)
  - South Korea: **811.048042 KRW / Int'l \$** (Price Level Index = 59.5)
  - Singapore: **0.797634 SGD / Int'l \$** (Price Level Index = 59.7)
  - United States: **1.000000 USD / Int'l \$** (Price Level Index = 100.0)

Under PPP deflation, Tsinghua's core academic budget expands from $\$5.36\text{B}$ nominal to **$\$10.58\text{B}$ PPP Int'l \$**, making it the single largest research expenditure pool in the world.

---

## 5. Path-Independent Shapley Waterfall Decomposition

When decomposing the apparent per-student funding gap between US private institutions (MIT & Caltech average) and TUM, sequential adjustments are order-dependent. For $K = 5$ adjustment stages, we evaluate all $K! = 120$ permutation sequences $\pi \in \Pi$:

$$\phi_j = \frac{1}{K!} \sum_{\pi \in \Pi} \Delta_j(\pi)$$

The decomposition reveals that the raw headline gap of **\$889k / student** is reduced by **65.7%** down to **\$305k / student**:
1. **Stripping Defense FFRDCs (JPL & Lincoln Lab)**: $-\$602\text{k}$ Shapley attribution ($\phi$).
2. **Stripping Clinical Hospitals (Klinikum rechts der Isar)**: $+\$19\text{k}$ Shapley attribution ($\phi$), reflecting that patient care is non-instructional.
3. **Adding External Research Clusters**: $+\$11\text{k}$ net Shapley attribution ($\phi$).
4. **Applying OECD Purchasing Power Parity (PPP)**: $-\$11\text{k}$ Shapley attribution ($\phi$).
5. **Harmonizing On-Campus FTE Scale**: $-\$1.4\text{k}$ Shapley attribution ($\phi$).
6. **Remaining Adjusted Disparity (Tier 2 PPP)**: $\$305\text{k}$ reflecting MIT/Caltech's compact student body ($\sim 7\text{k}$ average) vs. TUM's mass enrollment ($51.2\text{k}$ on-campus FTE).

---

## 6. International & Domestic Degree Total Cost & 20-Year Career ROI Model

We model the complete financial lifecycle across all 4 cohorts (Master & Bachelor $\times$ International & Domestic/In-State):
1. **Tuition, Living Costs & Empirical Median Degree Durations**:
   - **Master's Cohorts**:
     - Imperial College London: 1.0-year MSc (£41k tuition + £22.7k living = **\$73.6k USD** net int'l / **\$49.1k USD** net domestic).
     - NTU Singapore: 1.0-year MSc (S\$52k tuition + S\$17.4k living = **\$48.0k USD** net int'l / **\$22.2k USD** net domestic).
     - ETH Zurich: 2.0-year MSc (CHF 8.76k tuition + CHF 52.8k living = **\$66.9k USD** net int'l / **\$45.3k USD** net domestic).
     - TUM: 2.0-year MSc (€20k tuition + €32.4k living = **\$49.1k USD** net int'l / **\$22.8k USD** net domestic).
     - MIT: 2.0-year SM (\$128.6k tuition + \$53.2k living = **\$181.8k USD** sticker, **\$117.5k USD** net).
     - KAIST: 2.0-year MS (100% tuition waiver + living stipend = **\$1.7k USD** net int'l / **\$1.1k USD** net domestic).
   - **Bachelor's Empirical Median Durations & Student Employment Offsets**:
     - While statutory Bologna *Regelstudienzeit* is 6 semesters (3.0 years), official statistical registries (*TUM in Zahlen 2023/24* p. 32 across Informatics, EE, and Mechanical Engineering; Destatis Fachserie 11; Swiss BFS LABB) show an empirical engineering median duration of **8.0 semesters (4.0 years)** at **TUM** and **ETH Zurich**, matching the 4.0-year median of US (**MIT, Caltech, Georgia Tech**) and Asian (**Tsinghua, KAIST, NTU**) programs. Only **Imperial College London (BEng)** operates a strictly cohort-locked **3.0-year** undergraduate progression.
     - Net degree costs incorporate verified institutional student employment and grant schedules (`€12.41–€14.00/hr` TUM HiWi / TV-Stud and `€538/mo` minijob ceiling; `CHF 30.70/hr` ETH *Hilfsassistierende*; Imperial Bursary & London Living Wage casual work; US IPEDS aided net prices & GRA/GTA waivers; Asian national scholarship remissions).
2. **Fixed Post-Matriculation Horizons & Age-Graded No-College Counterfactual**:
   - Trajectories are evaluated over a fixed post-matriculation window: **22 years for Master** (ages 22$\to$44, giving 1-yr MSc graduates 21 career years vs. 20 career years for 2-yr MS) and **24 years for Bachelor** (ages 18$\to$42, giving 3-yr Imperial BEng graduates 21 career years vs. 20 career years for 4-yr BSc), capturing the 1-year labor-market head start on the horizontal `year_since_matriculation` axis.
   - Piecewise linear interpolation from Year 1 starting salary to Year 10 mid-career salary (`yr = 1..10`) and from Year 10 to Year 20 senior salary (`yr = 10..20/21`), net of effective single-earner income tax and employee social security contributions.
   - **Study-Phase Foregone Earnings**: Country-specific median 20-year-old net salary (`youth_median_gross_salary_lcu`) for Bachelor cohorts and Bachelor Year-1 net salary for Master cohorts.
   - **Career-Phase Counterfactual Baseline**: Annual excess wealth subtracts the empirical age-graded (`20–24`, `25–29`, `30–34`, `35–39`, `40–45`) net salary of a non-college worker in that country (`nocollege_salary_*_lcu`), where shared single-adult city living expenses cancel out identically:
     $$\text{ExcessWealth}_{\text{opp}}(t) = -\left(\text{Net Degree Cost} + T_{\text{deg}} \cdot S_{\text{foregone, net}}\right) + \sum_{\tau=1}^{t} \left(S_{\text{grad, net}}(\tau) - S_{\text{no-college, net}}(\text{age}_\tau)\right)$$
3. **Discounted Real Cash Flows ($r = 3\%$) & Economic ROI Multiple**:
   - **Real Discounting**: Future savings flows are also tracked at a 3% real discount rate (`cumulative_wealth_discounted_usd`).
   - **Economic ROI Multiple**: Because total economic investment ($\text{Net Degree Cost} + \text{Foregone Earnings}$) is strictly positive for all 9 institutions even when tuition is waived, $\text{ROI}_u(t) = \text{ExcessWealth}_{\text{opp}}(t) / (\text{Net Cost}_u + \text{Foregone Earnings}_u)$ is well-defined and currency-invariant across all cohorts.

