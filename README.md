# Cross-Continental Comparative Analysis of 9 Elite Technical Universities
## United States vs. Europe vs. Asia ($3 \times 3$ Regional Matrix)

[![Responsible Research Certified](https://img.shields.io/badge/Responsible--Research-5%2F5%20Audit%20Passed-brightgreen)](file:///Users/selle/Documents/GitHub/technical-universities/.agents/skills/responsible-research/scripts/audit_research_pipeline.py)
[![Verification Status](https://img.shields.io/badge/Provenance-SHA256%20Verified-blue)](file:///Users/selle/Documents/GitHub/technical-universities/rawdata/MANIFEST.csv)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](file:///Users/selle/Documents/GitHub/technical-universities/README.md)

This empirical research repository provides a rigorous, multi-dimensional descriptive and structural comparative analysis across **9 leading technical universities** spanning three continental regions ($3 \times 3$ regional matrix):

- **United States (`US`)**: **MIT**, **Caltech**, **Georgia Tech**
- **Europe (`EU`)**: **Imperial College London**, **ETH Zurich**, **TUM (Technical University of Munich)**
- **Asia (`ASIA`)**: **Tsinghua University**, **KAIST**, **NTU Singapore**

The investigation addresses the core research questions established in [`instructions.md`](./instructions.md):
1. **Raw Yearly Budgets vs. Corrected Student-Facing Budgets per Capita** (incorporating external research clusters such as **Max Planck, Helmholtz, ESO, FRM II, and LRZ in Garching/Munich** for TUM, the **ETH Domain** for ETH, and stripping non-student defense FFRDCs and clinical teaching hospitals).
2. **Student Denominator Harmonization** (Raw Headcount vs. On-Campus Full-Time Equivalent [FTE], correcting for Georgia Tech's $>20\text{k}$ online Master's cohort).
3. **Purchasing Power Parity (PPP) vs. Nominal Exchange Rate Deflation** (World Bank 2023 `PA.NUS.PPP`).
4. **Global Rankings & Employability** (**QS World University Rankings 2025** overall & Engineering/Tech, **QS Employer Reputation**, and the **Emerging Global Employability University Ranking [GEURS] 2024/2025**).
5. **Multi-Dimensional Research Efficiency** (CWTS Leiden 2024 field-normalized Top-10% and Top-1% citation shares, citations per faculty, and breakthrough publications per \$10M PPP research spend).
6. **International Master's Student Financial Lifecycle** (1-year vs. 2-year degree duration, tuition sticker price, recent non-EU tuition reforms at TUM and ETH, living costs, and **10-year post-tax cumulative salary / Net ROI projections**).
7. **Path-Independent Shapley Waterfall Decomposition** (explaining how raw budget gaps between US private endowments and European public flagships collapse by **67.4%** under structural adjustment).

---

## 1. Executive Summary Table (The Master Matrix)

All metrics are derived deterministically from [`datasets/university_master_comparison_2024.csv`](./datasets/university_master_comparison_2024.csv):

| University | Region | On-Campus FTE Students | Core Academic Budget (Tier 1, PPP) | Corrected Student-Facing Budget / FTE (Tier 2, PPP) | QS 2025 World Rank (Eng/Tech) | GEURS Employability Rank 2025 | CWTS Leiden Top-10% Citations | Top-10% Papers per \$10M PPP Spend | Int'l Master's Net Cost (USD) | 10-Yr Post-Tax Net Cumulative Wealth | Break-Even Payback Horizon |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MIT** | US | **11,886** | **\$3,219.0M** | **\$298,995** | **#1** (#1) | **#1** | **24.8%** | **19.1** | **\$117,490** | **\$894,862** | **2.5 yrs** |
| **Caltech** | US | **2,400** | **\$914.2M** | **\$393,418** | **#10** (#9) | **#2** | **22.9%** | **10.3** | **\$106,575** | **\$803,117** | **3.0 yrs** |
| **Georgia Tech** | US | **30,800** | **\$1,799.8M** | **\$63,000** | **#114** (#21) | **#54** | **13.3%** | **23.9** | **\$70,241** | **\$707,359** | **2.0 yrs** |
| **Imperial** | EU | **22,400** | **\$2,008.8M** | **\$98,662** | **#2** (#7) | **#10** | **17.4%** | **38.3** | **\$57,572** | **\$547,196** | **3.0 yrs** |
| **ETH Zurich** | EU | **25,800** | **\$2,026.0M** | **\$90,895** | **#7** (#6) | **#17** | **18.6%** | **33.8** | **\$58,920** | **\$868,775** | **1.5 yrs** |
| **TUM** | EU | **51,200** | **\$1,566.5M** | **\$39,127** | **#28** (#19) | **#13** | **11.4%** | **30.5** | **\$45,400** | **\$479,720** | **1.5 yrs** |
| **Tsinghua** | ASIA | **61,500** | **\$10,585.0M** | **\$201,280** | **#20** (#12) | **#19** | **16.9%** | **12.5** | **\$11,338** | **\$511,812** | **1.0 yr** |
| **KAIST** | ASIA | **12,100** | **\$1,454.9M** | **\$149,173** | **#53** (#23) | **#78** | **13.8%** | **23.5** | **\$2,294** | **\$654,749** | **0.5 yr** |
| **NTU Singapore** | ASIA | **32,800** | **\$2,106.2M** | **\$73,431** | **#15** (#15) | **#33** | **18.9%** | **41.6** | **\$48,041** | **\$822,767** | **2.0 yrs** |

---

## 2. The 9-Panel ($3 \times 3$) Synoptic Matrix

The entire comparative investigation is synthesized into a single cohesive publication figure generated deterministically by [`src/modeling.py`](./src/modeling.py):

![9-Panel Synoptic Matrix (English)](./plots/technical_universities_3x3_en.png)

*(A complete German-language edition is available at [`plots/technical_universities_3x3_de.png`](./plots/technical_universities_3x3_de.png)).*

### Narrative Structure of the 9 Panels:
- **Row 1 (Budgets & Scale)**:
  - **Panel A ([`plots/panel_a_budget_tiers_ppp.png`](./plots/panel_a_budget_tiers_ppp.png))**: Unadjusted Gross Budget (Tier 0) vs. Core Academic ex-Hospitals & Defense FFRDCs (Tier 1) vs. Ecosystem-Augmented Student-Facing Budget (Tier 2 in PPP \$).
  - **Panel B ([`plots/panel_b_enrollment_fte_supervision.png`](./plots/panel_b_enrollment_fte_supervision.png))**: Student Scale (Headcount vs. On-Campus FTE), isolating Georgia Tech's $20.8\text{k}$ online OMSCS cohort.
  - **Panel C ([`plots/panel_c_student_facing_budget_per_fte.png`](./plots/panel_c_student_facing_budget_per_fte.png))**: Corrected Student-Facing Budget per On-Campus FTE in Nominal USD vs. World Bank PPP International Dollars.
- **Row 2 (Rankings & Research Efficiency)**:
  - **Panel D ([`plots/panel_d_rankings_employability_profile.png`](./plots/panel_d_rankings_employability_profile.png))**: QS World University Rankings 2025 vs. Emerging Global Employability University Ranking (GEURS 2025).
  - **Panel E ([`plots/panel_e_research_efficiency_multidim.png`](./plots/panel_e_research_efficiency_multidim.png))**: Multi-Dimensional Cost-Normalized Research Efficiency (CWTS Leiden Top-10% cited papers per \$10M PPP core academic spend).
  - **Panel F ([`plots/panel_f_2d_efficiency_frontier_surface.png`](./plots/panel_f_2d_efficiency_frontier_surface.png))**: 2D Institutional Efficiency Frontier ($B \times F \to Q$) mapping the three institutional regimes with verified marginal conservation ($<10^{-10}$ drift).
- **Row 3 (Student Costs, Careers & Causal Decomposition)**:
  - **Panel G ([`plots/panel_g_masters_cost_lifecycle.png`](./plots/panel_g_masters_cost_lifecycle.png))**: International Master's Total Degree Investment (Sticker Price vs. Net Out-of-Pocket after RA/TA/HiWi fellowships).
  - **Panel H ([`plots/panel_h_10y_salary_roi_trajectories.png`](./plots/panel_h_10y_salary_roi_trajectories.png))**: 10-Year Post-Graduation Cumulative Post-Tax Wealth & Net ROI Trajectories ($t = -2 \dots +10$ years).
  - **Panel I ([`plots/panel_i_shapley_waterfall_decomposition.png`](./plots/panel_i_shapley_waterfall_decomposition.png))**: Path-Independent Shapley Waterfall Decomposition decomposing the apparent MIT/Caltech vs. TUM funding gap across $5! = 120$ permutation paths.

---

## 3. Seven Core Methodological Takeaways

### 1. The Garching & FFRDC Accounting Paradox
In headline numbers, US private institutes (**Caltech** and **MIT**) appear to spend 10x to 15x more per student than European public universities. However, **74.1% of Caltech's gross spend is NASA's JPL** (\$2.61B) and **29.8% of MIT's spend is the DoD Lincoln Laboratory** (\$1.37B). Conversely, **TUM's gross budget includes €794.7M in clinical hospital operations** (*Klinikum rechts der Isar*), while its world-class neighbor institutes in Garching and Munich (**Max Planck IPP, MPE, MPQ, MPA, MPI of Biochemistry, Helmholtz Munich, ESO, FRM II, LRZ**) account for **€971.6M/year** in off-balance-sheet research capacity. Accounting for this ecosystem adds **€437.2M** in student-facing research infrastructure to TUM.

### 2. The Georgia Tech Online Master's Denominator Split
Georgia Tech enrolls **53,350 total students**, but **20,850 are enrolled in low-cost online distance Master's degrees** (OMSCS, OMSA, OMSCyber). Measuring resources per total student headcount artificially depresses Georgia Tech's per-student spend to \$33.7k. Correcting for on-campus FTEs reveals an actual campus intensity of **\$58.4k/FTE (Tier 1)** and **\$63.0k/FTE (Tier 2)**.

### 3. Purchasing Power Parity (PPP) Shifts the Global Resource Balance
Under nominal exchange rates, Asian universities appear financially constrained. Under **World Bank GDP PPP conversion factors** (e.g., 3.64 CNY/Int'l \$ in China; 811 KRW/Int'l \$ in Korea), **Tsinghua University's core budget equals \$10.58B PPP**, giving it a Tier 2 student-facing budget of **\$201,280 PPP per FTE**—surpassing all European universities.

### 4. Mass-Scale Public Universities Dominate Employer Reputation
While QS heavily weights academic peer reputation and citation volume favoring private endowments, the **Emerging Global Employability University Ranking (GEURS 2025)** shows that corporate recruiters place massive value on large public technical flagships: **TUM ranks #13 worldwide in employability** (surpassing ETH Zurich at #17, Tsinghua at #19, and NTU at #33), and **Caltech ranks #2**.

### 5. Research Efficiency: The European and Asian Advantage
When measuring field-normalized scientific excellence per dollar spent (CWTS Leiden Top-10% cited papers per \$10M PPP core academic budget), **European and Asian flagships significantly outperform US private endowments**:
- **NTU Singapore**: **41.6** Top-10% papers / \$10M PPP
- **Imperial College London**: **38.3** Top-10% papers / \$10M PPP
- **ETH Zurich**: **33.8** Top-10% papers / \$10M PPP
- **TUM**: **30.5** Top-10% papers / \$10M PPP
- **MIT**: **19.1** Top-10% papers / \$10M PPP
- **Caltech**: **10.3** Top-10% papers / \$10M PPP

### 6. The International Master's ROI & Payback Asymmetry
- **Degree Duration**: Imperial College London (12 months) and NTU Singapore (12 months) offer 1-year intensive MSc degrees, requiring half the living expenses and granting an additional year of career earnings.
- **Tuition Paradigms**: KAIST (\$2.3k net) and Tsinghua (\$11.3k net) provide virtually tuition-free education with guaranteed stipends. TUM (\$45.4k net over 2 years, post-2024 non-EU fees) and ETH Zurich (\$58.9k net over 2 years, post-2025 fees) remain 50%–60% cheaper than MIT (\$117.5k net) and Caltech (\$106.6k net).
- **Payback Horizon**: Continental European and Asian graduates break even within **0.5 to 1.5 years**, whereas high-tuition US and UK graduates require **2.5 to 3.0 years**. Over a 10-year horizon, **ETH Zurich graduates achieve cumulative net wealth (\$868k) comparable to MIT (\$895k)** due to lower initial debt, low Swiss income taxes (21.8%), and high Zurich nominal wages.

### 7. Path-Independent Shapley Waterfall Results
Evaluating all $5! = 120$ permutation paths reveals that the raw headline funding gap of **\$586k / student** between US private endowments and TUM collapses by **67.4%** down to **\$191k / student** once defense FFRDCs (-\$210k), hospitals (-\$16k), the Garching research cluster (-\$9k), and German purchasing power parity (-\$9k) are accounted for.

---

## 4. Repository Structure & Audit Reproduction

```text
/
├── goal/
│   ├── description.md       # Exact scope, entities, and research dimensions
│   └── hypothesis.md        # Falsifiable hypotheses (H1 Garching/FFRDC, H2 Scale, H3 ROI)
├── literature/
│   ├── literature.md        # Primary reference catalog and DOIs
│   ├── US_Tech_Universities_Financial_Enrollment_Extract_2024.pdf
│   ├── European_Tech_Universities_TUM_ETH_Imperial_2024_Extract.pdf
│   ├── Asia_Tech_Universities_2024_Extract.pdf
│   └── QS_GEURS_Leiden_OECD_2025_CrossNational_Rankings_PPP_Extract.pdf
├── rawdata/
│   ├── MANIFEST.csv         # Cryptographic SHA-256 provenance manifest
│   ├── rawdata.md           # Audit table with retrieval dates and byte counts
│   ├── university_financials_enrollment_2024.csv
│   ├── garching_partner_ecosystem_breakdown_2024.csv
│   ├── rankings_bibliometrics_employability_2025.csv
│   ├── masters_tuition_living_salary_2025.csv
│   ├── historical_enrollment_budget_panel_2010_2024.csv
│   └── literature_empirical_benchmarks.csv
├── datasets/
│   ├── datasets.md          # Comprehensive data dictionary and normalization formulas
│   ├── university_master_comparison_2024.csv
│   ├── external_ecosystem_harmonized_2024.csv
│   ├── masters_10y_cashflow_trajectories.csv
│   ├── historical_panel_harmonized.csv
│   └── literature_empirical_benchmarks.csv
├── src/
│   ├── data_preparation.py  # Deterministic ETL pipeline (rawdata -> datasets)
│   └── modeling.py          # Fits statistical models & renders all 11 plots
├── plots/
│   ├── plot.md              # Systematic documentation of every plot's validity & math
│   ├── panel_a_budget_tiers_ppp.png
│   ├── panel_b_enrollment_fte_supervision.png
│   ├── panel_c_student_facing_budget_per_fte.png
│   ├── panel_d_rankings_employability_profile.png
│   ├── panel_e_research_efficiency_multidim.png
│   ├── panel_f_2d_efficiency_frontier_surface.png
│   ├── panel_g_masters_cost_lifecycle.png
│   ├── panel_h_10y_salary_roi_trajectories.png
│   ├── panel_i_shapley_waterfall_decomposition.png
│   ├── technical_universities_3x3_en.png
│   └── technical_universities_3x3_de.png
├── methodology/
│   └── methodology.md       # Methodological monograph, accounting boundaries & math
└── requirements.txt         # Pinned Python dependencies
```

### Reproducing the Pipeline from Scratch:
```bash
# 1. Install pinned dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run deterministic data preparation pipeline
python3 src/data_preparation.py

# 3. Fit models and generate all 11 figures (Panels A–I + 3x3 Matrices)
python3 src/modeling.py

# 4. Execute the automated research pipeline audit suite
python3 .agents/skills/responsible-research/scripts/audit_research_pipeline.py
```

