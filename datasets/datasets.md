# Harmonized Research Datasets & Data Dictionary (`datasets/`)

This directory contains deterministic, analysis-ready empirical datasets derived exclusively from `rawdata/` via `src/data_preparation.py`. All indicators are standardized across currencies (Nominal USD & OECD/World Bank PPP International Dollars), institutional accounting boundaries (Tiers 0, 1, and 2), student enrollment models (Raw Headcount vs. On-Campus Full-Time Equivalent [FTE]), degree levels (Master's vs. Bachelor's), and tuition residency regimes (Non-Native / International vs. Native / Domestic / In-State).

---

## 1. Catalog of Datasets

| File | Description | Granularity | Key Primary Source Provenance |
| :--- | :--- | :--- | :--- |
| [`university_master_comparison_2024.csv`](./university_master_comparison_2024.csv) | Primary institutional cross-section for all 9 universities across 3-tier budgets, student/faculty supervision, multi-system rankings, research efficiency, and Master's and Bachelor's career metrics | 9 institutions (3 US, 3 EU, 3 ASIA) | Audited Financial Statements FY24, Common Data Sets / Factbooks, QS 2025, THE 2025, ARWU 2024, US News 2025, GEURS 2024/2025, CWTS Leiden 2024, World Bank WDI |
| [`external_ecosystem_harmonized_2024.csv`](./external_ecosystem_harmonized_2024.csv) | Granular breakdown of 25 co-located external research institutes across all 9 university ecosystems in local currency, Nominal USD, and PPP International Dollars | 25 research institutes & centers | Max Planck Society, Helmholtz Munich, ESO, MLZ, LRZ, ETH Domain (PSI, Empa, Eawag, WSL), Broad, Whitehead, Carnegie/Huntington, Emory/ORNL, Crick, BNRist, ETRI, IBS, A*STAR |
| [`masters_10y_cashflow_trajectories.csv`](./masters_10y_cashflow_trajectories.csv) | Annual financial cash-flow and net wealth trajectories ($t = -4 \dots +10$ years) across Master's and Bachelor's cohorts comparing sticker vs. funded paths | 229 annual cohort records across 9 universities | Official graduate and undergraduate tuition schedules, living expense guidelines, MOE GES, and StepStone / BFS / Payscale career progression surveys |
| [`degrees_10y_cashflow_trajectories.csv`](./degrees_10y_cashflow_trajectories.csv) | Unified annual cash-flow trajectories for all 4 student cohorts (Master & Bachelor x Native & Non-Native) | 229 annual cohort records across 9 universities | Combined graduate & undergraduate financial registries |
| [`historical_panel_harmonized.csv`](./historical_panel_harmonized.csv) | 15-year longitudinal panel (2010, 2015, 2020, 2024) of student enrollment expansion vs. real core academic budget per FTE indexed to $2010 = 100$ | 36 institutional year points | Historical university annual reports and Destatis / IPEDS longitudinal registries |
| [`literature_empirical_benchmarks.csv`](./literature_empirical_benchmarks.csv) | Full cryptographic catalog of literature benchmarks with exact page/table coordinates and verbatim quotes | 103 verified primary benchmark parameters | Primary research reports, financial statements, and World Bank / OECD statistical series |

---

## 2. Variable Definitions & Mathematical Normalization Formulas

### A. 3-Tier Budget Normalization
1. **Tier 0 (Gross Consolidated Operating Expenditure)**:
   - **Nominal USD**: $\text{Gross}_{\text{LCU}} \times \text{FX}_{\text{LCU}\to\text{USD}}$
   - **PPP International Dollars**: $\text{Gross}_{\text{LCU}} / \text{PPP}_{\text{LCU}}$ (World Bank 2023 WDI `PA.NUS.PPP`)
   - **Per Headcount (PPP)**: $\text{Gross}_{\text{PPP}} \times 10^6 / N_{\text{headcount}}$
   - **Per On-Campus FTE (PPP)**: $\text{Gross}_{\text{PPP}} \times 10^6 / N_{\text{FTE}}$
2. **Tier 1 (Core Academic ex-Hospitals & Defense FFRDCs)**:
   - $\text{Core}_{\text{LCU}} = \text{Gross}_{\text{LCU}} - \text{Hospital}_{\text{LCU}} - \text{Defense FFRDC}_{\text{LCU}}$
   - Strips non-academic patient care clinical turnover (e.g. TUM *Klinikum rechts der Isar* €794.7M) and closed military/space FFRDCs (MIT *Lincoln Lab* \$1,367.2M, Caltech *JPL* \$2,611.6M, Georgia Tech *GTRI* \$919.0M).
   - **Per On-Campus FTE (PPP)**: $\text{Core}_{\text{PPP}} \times 10^6 / N_{\text{FTE}}$
3. **Tier 2 (Ecosystem-Augmented Student-Facing Budget)**:
   - $\text{Augmented}_{\text{LCU}} = \text{Core}_{\text{LCU}} + \sum_{k} (B_{k,\text{LCU}} \times w_k)$
   - Where $B_{k}$ is the operating budget of co-located external institute $k$ (e.g., Garching Max Planck Institutes, Helmholtz Munich, ESO, FRM II, LRZ for TUM; PSI, Empa, Eawag, WSL for ETH; Broad/Whitehead for MIT; ETRI/IBS for KAIST; A*STAR for NTU) and $w_k$ is the audited academic integration weight ($0.10 \le w_k \le 0.60$) with explicit $\pm 50\%$ model calibration bounds.
   - **Conservative Tier 2 Lower Bound (Legally Independent Only)**:
     $$\text{Augmented}_{\text{Indep, LCU}} = \text{Core}_{\text{LCU}} + \sum_{k \in \mathcal{E}_{\text{indep}}} (B_{k,\text{LCU}} \times w_k)$$
     Isolates autonomous external institutes with legally segregated balance sheets (Max Planck, Helmholtz, PSI, Empa, Broad, Crick, ETRI, A*STAR), excluding on-campus hosted entities (FRM II, BNRist, SKLs, KAIST IBS, NTU RCEs) to test robustness against internal financial consolidation.

### B. Student Denominator Standardization & Sensitivity
- **On-Campus FTE**: Full-time equivalent degree-seeking students active on the physical campus.
- **Online Distance Cohort Isolation & Operational Cost Deduction**: Georgia Tech's $\sim 20{,}850$ online distance Master's students (OMSCS, OMSA, OMSCyber) are isolated from its $\sim 30{,}800$ on-campus FTE cohort. Furthermore, deducting the ~$78.0M annual operating delivery cost of the online program from Georgia Tech's Core Academic budget yields the clean on-campus figure:
  $$\text{Tier 1}_{\text{Clean}} = \frac{\$1{,}799.8\text{M} - \$78.0\text{M}}{30{,}800\text{ FTE}} = \$55{,}903\text{ PPP / FTE}$$
- **Clinical Medical Student Denominator Sensitivity**:
  - **TUM**: 1,666 clinical students (*Staatsexamen Medizin 2. Studienabschnitt*) deducted from 51,200 FTE denominator $\to$ \$31,623 PPP / FTE (+3.4%).
  - **Imperial**: 4,665 medical FTEs deducted from 22,400 FTE denominator $\to$ \$113,265 PPP / FTE (+26.3%).

### C. Multi-Dimensional Research Efficiency
- **Annualized Top-10% Cited Output per \$10M PPP Spend**:
  $$\text{Efficiency}_{\text{Top10, Annual}} = \frac{(\text{Total Publications}_{2019-2022} / 4.0) \times (\text{PP}_{\text{top 10\%}} / 100)}{\text{Tier 1 Core Academic Budget}_{\text{PPP}} / 10^7}$$
  Measures field-normalized annual breakthrough scientific output yield per unit of real purchasing power investment. The 4-year cumulative yield is also retained as `top10_pubs_per_10m_ppp_spend`.

### D. Multi-System Global Ranking Framework
Evaluates institutions across 7 authoritative ranking systems without rank-truncation artifacts:
1. **QS World University Rankings 2025** (Overall Score & Rank)
2. **Times Higher Education (THE) World University Rankings 2025** (Overall Score & Rank)
3. **Academic Ranking of World Universities (ARWU Shanghai) 2024** (Overall Score & Rank)
4. **U.S. News & World Report Best Global Universities 2024-2025** (Global Rank & Score)
5. **THE / QS Engineering & Technology Subject Rankings 2024/2025**
6. **Global Employability University Ranking and Survey (GEURS 2024/2025)**
7. **CWTS Leiden Ranking 2024 Scientific Impact** (PP_top10% & Scientific Volume)

### E. 4-Cohort Lifecycle & 20-Year Career Simulation
Simulates post-graduation financial lifecycles across a full $2 \times 2$ factorial structure:
1. **Cohort 1: Master's Non-Native (International)**
2. **Cohort 2: Master's Native (Domestic / In-State)**
3. **Cohort 3: Bachelor's Non-Native (International)**
4. **Cohort 4: Bachelor's Native (Domestic / In-State)**

- **Undergraduate Duration**: 3.0 years for European Bologna Bachelor programs (Imperial BEng, ETH Zurich BSc, TUM BSc); 4.0 years for US and Asian programs (MIT, Caltech, Georgia Tech, Tsinghua, KAIST, NTU Honours).
- **Study-Phase Outflow Conservation**:
  $$\sum_{t=1}^{\lceil T \rceil} \text{Outflow}_t \equiv \text{Total Net Degree Cost}$$
  Runtime assertions ensure 100.0% accounting conservation across integer and non-integer degree durations.
- **20-Year Post-Tax Cumulative Wealth & Real Discounting**:
  $$\text{Wealth}(t) = -\text{Net Degree Cost} + \sum_{\tau=1}^{t} \left(\text{Salary}(\tau) \times (1 - \text{Tax Rate}) - \text{CareerLiving}_{\text{city}}(\tau)\right)$$
  $$\text{Wealth}_{\text{disc}}(t) = -\text{Net Degree Cost} + \sum_{\tau=1}^{t} \frac{\Delta \text{Wealth}(\tau)}{(1 + 0.03)^{\tau}}$$
- **Foregone Earnings & Empirical Age-Graded No-College Excess Wealth Baseline**:
  During study years, foregone earnings equal country-specific age-20 median net salary (`youth_median_gross_salary_lcu`) for Bachelor's cohorts and Bachelor Year-1 net salary for Master's cohorts. During post-graduation career years ($\tau = 1 \dots 20$, ages 22–45), annual excess wealth subtracts the empirical age-graded (`20–24`, `25–29`, `30–34`, `35–39`, `40–45`) net salary of a non-college worker in that country (`nocollege_salary_*_lcu`), where shared city living expenses cancel out identically:
  $$\text{ExcessWealth}_{\text{opp}}(t) = -\left(\text{Net Degree Cost} + T_{\text{deg}} \cdot \text{Salary}_{\text{foregone, net}}\right) + \sum_{\tau=1}^{t} \left(\text{Salary}_{\text{grad, net}}(\tau) - \text{Salary}_{\text{no-college, net}}(\text{age}_\tau)\right)$$
- **Disciplinary Sensitivity Bands**: Models uncertainty intervals between mechanical engineering and CS/AI compensation paths.

### F. Admissions Selectivity & Screening Indicators
Captures the divergence between upfront admissions gatekeeping and in-program comprehensive exam screening:
1. `undergrad_applicants_total` & `undergrad_admitted_total`: Official first-time undergraduate applications and admissions from Common Data Sets (CDS Section C1), UCAS end-of-cycle summaries, and institutional factbooks.
2. `undergrad_acceptance_rate_pct`: Overall undergraduate acceptance rate ($\text{Admitted} / \text{Applicants} \times 100$).
3. `undergrad_acceptance_rate_domestic_pct` & `undergrad_acceptance_rate_intl_pct`: In-state/domestic statutory entitlement vs. international competition rates.
4. `first_year_screening_attrition_pct`: Actual first-year undergraduate cohort attrition / non-continuation rate after Year 1 (ETH Zurich *Basisprüfung* 1st-year exit 20.0% [out of 31% total multi-year attrition / 69% BFS Bachelor completion, as 1st-attempt non-passers may repeat once]; TUM *Grundlagen- und Orientierungsprüfung* [GOP] 1st-year exit 15.0% [out of 20.0% total 8-semester EFV exmatriculation rate]), harmonized with 1-year non-continuation rates across US, UK, and Asian peers (1.0%–4.5%).

---

## 3. Data Dictionary of Newly Added Harmonized Indicators

### `datasets/university_master_comparison_2024.csv`
- `clinical_medical_students_headcount`: Exact headcount of clinical human medicine students (TUM: 1,666; Imperial: 2,734 UG MBBS / 4,665 total medical FTE).
- `online_operating_expenditure_est_lcu`: Estimated operating cost of online distance programs in local currency (Georgia Tech: \$78.0M for 20,850 online students).
- `tier1_per_fte_usd_ppp_clean_online`: Core academic budget per on-campus FTE after deducting online delivery expenditure (Georgia Tech: \$55,903 PPP/FTE).
- `tier1_per_fte_usd_ppp_ex_med`: Core academic budget per on-campus FTE after deducting clinical medical students (TUM: \$31,623 PPP/FTE; Imperial: \$113,265 PPP/FTE).
- `tier2_augmented_usd_ppp_indep_m`: Ecosystem-augmented budget in million PPP Int'l \$ including only legally independent external institutes.
- `tier2_per_fte_usd_ppp_indep`: Tier 2 per on-campus FTE using only legally independent external partners (conservative lower bound).
- `year1_median_salary_ppp` & `bachelors_year1_median_salary_ppp`: Early-career median graduate salary valued in local purchasing power (World Bank PPP).
- `total_sticker_cost_ppp`, `bachelors_total_sticker_cost_ppp`, `net_out_of_pocket_cost_ppp`, `bachelors_net_out_of_pocket_cost_ppp`: Degree investment amounts converted to World Bank PPP International Dollars.

### `datasets/external_ecosystem_harmonized_2024.csv`
- `is_legally_independent`: Boolean indicator (`True` for autonomous research entities with distinct legal personality and balance sheets; `False` for hosted on-campus centers).
- `hosted_status`: String classification (`Legally_Independent_External_Partner` vs `On_Campus_Hosted_Center_Potential_Internal_Consolidation`).

### `datasets/masters_10y_cashflow_trajectories.csv` & `datasets/degrees_10y_cashflow_trajectories.csv`
- `cumulative_wealth_discounted_usd` & `cumulative_wealth_discounted_lcu`: Cumulative post-tax net wealth discounted at a 3% real annual discount rate.
- `cumulative_wealth_opp_cost_usd` & `cumulative_wealth_local_opp_cost_usd`: Cumulative 20-year post-tax excess wealth over the empirical age-graded (`20–45` yr) no-college counterfactual baseline, net of study-phase out-of-pocket degree costs and foregone earnings.
