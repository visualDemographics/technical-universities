# Harmonized Research Datasets & Data Dictionary (`datasets/`)

This directory contains deterministic, analysis-ready empirical datasets derived exclusively from `rawdata/` via `src/data_preparation.py`. All indicators are standardized across currencies (Nominal USD & OECD/World Bank PPP International Dollars), institutional accounting boundaries (Tiers 0, 1, and 2), and student enrollment models (Raw Headcount vs. On-Campus Full-Time Equivalent [FTE]).

---

## 1. Catalog of Datasets

| File | Description | Granularity | Key Primary Source Provenance |
| :--- | :--- | :--- | :--- |
| [`university_master_comparison_2024.csv`](./university_master_comparison_2024.csv) | Primary institutional cross-section for all 9 universities across 3-tier budgets, student/faculty supervision, rankings, research efficiency, and Master's career metrics | 9 institutions (3 US, 3 EU, 3 ASIA) | Audited Financial Statements FY24, Common Data Sets / Factbooks, QS 2025, GEURS 2024/2025, CWTS Leiden 2024, World Bank WDI |
| [`external_ecosystem_harmonized_2024.csv`](./external_ecosystem_harmonized_2024.csv) | Granular breakdown of 25 co-located external research institutes across all 9 university ecosystems in local currency, Nominal USD, and PPP International Dollars | 25 research institutes & centers | Max Planck Society, Helmholtz Munich, ESO, MLZ, LRZ, ETH Domain (PSI, Empa, Eawag, WSL), Broad, Whitehead, Carnegie/Huntington, Emory/ORNL, Crick, BNRist, ETRI, IBS, A*STAR |
| [`masters_10y_cashflow_trajectories.csv`](./masters_10y_cashflow_trajectories.csv) | Annual financial cash-flow and net wealth trajectories ($t = -2 \dots +10$ years) for international STEM Master's students comparing sticker vs. funded paths | 106 annual cohort records across 9 universities | Official graduate tuition schedules, living expense guidelines, MOE GES, and StepStone / BFS / Payscale career progression surveys |
| [`historical_panel_harmonized.csv`](./historical_panel_harmonized.csv) | 15-year longitudinal panel (2010, 2015, 2020, 2024) of student enrollment expansion vs. real core academic budget per FTE indexed to $2010 = 100$ | 36 institutional year points | Historical university annual reports and Destatis / IPEDS longitudinal registries |
| [`literature_empirical_benchmarks.csv`](./literature_empirical_benchmarks.csv) | Full cryptographic catalog of literature benchmarks with exact page/table coordinates and verbatim quotes | 73 verified primary benchmark parameters | Primary research reports, financial statements, and World Bank / OECD statistical series |

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
   - Where $B_{k}$ is the operating budget of co-located external institute $k$ (e.g., Garching Max Planck Institutes, Helmholtz Munich, ESO, FRM II, LRZ for TUM; PSI, Empa, Eawag, WSL for ETH; Broad/Whitehead for MIT; ETRI/IBS for KAIST; A*STAR for NTU) and $w_k$ is the audited academic integration weight ($0.10 \le w_k \le 0.60$) based on joint faculty chairs (*Doppelberufungen*) and graduate thesis supervision.

### B. Student Denominator Standardization
- **On-Campus FTE**: Full-time equivalent degree-seeking students active on the physical campus.
- **Online Distance Cohort Isolation**: Georgia Tech's $\sim 20{,}850$ online distance Master's students (OMSCS, OMSA, OMSCyber) are isolated from its $\sim 30{,}800$ on-campus FTE cohort to prevent an artificial $\sim 40\%$ dilution of campus teaching expenditure.

### C. Multi-Dimensional Research Efficiency
- **Annualized Top-10% Cited Output per \$10M PPP Spend**:
  $$\text{Efficiency}_{\text{Top10, Annual}} = \frac{(\text{Total Publications}_{2019-2022} / 4.0) \times (\text{PP}_{\text{top 10\%}} / 100)}{\text{Tier 1 Core Academic Budget}_{\text{PPP}} / 10^7}$$
  Measures field-normalized annual breakthrough scientific output yield per unit of real purchasing power investment. The 4-year cumulative yield is also retained as `top10_pubs_per_10m_ppp_spend`.

### D. International Master's Student Lifecycle & 10-Year Career ROI (v1)
- **Total Sticker Degree Cost**: $\text{Tuition}_{\text{Total}} + \text{Living Cost}_{\text{Total}}$ (accounting for 1.0-year UK/SG degrees vs. 1.5–2.0-year US/EU/Asia degrees).
- **Net Degree Cost**: Sticker cost reduced by audited fellowship, graduate research/teaching assistantship (GRA/GTA), and student job (*HiWi*) offset rates.
- **10-Year Cumulative Post-Tax Net Pay (`cumulative_10y_net_earnings_usd`)**: Total cumulative take-home salary over 10 career years.
- **10-Year Post-Tax Cumulative Wealth / Net Savings (`cumulative_wealth_funded_usd`)**:
  $$\text{Wealth}(t) = -\text{Net Cost} + \sum_{\tau=1}^{t} \max\left(0, \text{Salary}(\tau) \times (1 - \text{Tax Rate}) - \text{Living}(\tau)\right)$$
- **Payback Horizon**: Smallest year $t^* \in [1, 10]$ where $\text{Wealth}(t^*) \ge 0$.

### E. Domestic / In-State Local Tuition Standardization (v2)
- **Total Degree Local Tuition (`total_degree_local_tuition_usd`)**: Total tuition evaluated under domestic/in-state fee schedules:
  - **TUM**: €0 tuition for German & EU domestic students.
  - **Georgia Tech**: \$14,064/yr in-state graduate tuition (vs. \$30,504 out-of-state/international).
  - **Imperial College London**: £16,500/yr UK Home fee (vs. £40,900 international).
  - **ETH Zurich**: CHF 730/sem domestic standard fee (vs. CHF 2,190 international from 2025).
  - **NTU Singapore**: SGD 22,050 total degree fee for Singapore Citizens (vs. SGD 57,024 international).
  - **Tsinghua University**: RMB 16,000 total degree fee for Chinese domestic academic Master's (vs. RMB 78,000 international).
  - **KAIST**: KRW 0 tuition under National Scholarship for Korean domestic students (vs. KRW 9.4M international).
  - **MIT & Caltech (US Private Endowments)**: Private US institutions offer no in-state residency discounts. Adhering strictly to the constraint of *no need-based cuts for family income*, their sticker tuition remains full price (\$64,310/yr and \$65,715/yr).
- **Local Total Degree Sticker Cost (`local_total_sticker_cost_usd`)**: $\text{Local Tuition}_{\text{USD}} + \text{Living Cost}_{\text{USD}}$.
- **Local Net Total Degree Cost (`local_net_total_degree_cost_usd` & `local_net_total_degree_cost_ppp`)**: $\text{Local Tuition}_{\text{USD}} \times (1 - \text{Offset Rate}) + \text{Living Cost}_{\text{USD}}$.
- **Local 10-Year Post-Tax Cumulative Wealth (`cumulative_wealth_local_usd`)**:
  $$W_{\text{local}}(t) = -C_{\text{net, local}} + \sum_{\tau=1}^{t} \max\left(0, \text{Salary}(\tau) \times (1 - \text{Tax Rate}) - \text{Living}(\tau)\right)$$
  Evaluated with disciplinary sensitivity bounds for Computer Science / AI (`cumulative_wealth_local_cs_usd`) and Mechanical Engineering (`cumulative_wealth_local_mech_usd`), and in PPP terms (`cumulative_wealth_local_ppp`).

### F. Multi-Ranking Institutional & Discipline Normalization
To prevent distortion from single-provider methodology biases and provide an absolute cardinal evaluation:
- **Times Higher Education (THE 2025)**:
  - `the_2025_rank`: Global institutional rank.
  - `the_2025_overall_score`: Standardized cardinal composite score (0–100 scale) evaluating Teaching (29.5%), Research Environment (29.0%), Research Quality (30.0%), International Outlook (7.5%), and Industry (4.0%).
  - `the_eng_tech_rank_2025`: Field-specific discipline rank across general, electrical, mechanical, aerospace, civil, and chemical engineering.
- **ShanghaiRanking Academic Ranking of World Universities (ARWU 2024)**:
  - `arwu_2024_rank`: Global institutional rank based on Nobel/Fields alumni and staff, Highly Cited Researchers (Clarivate), papers in Nature/Science, and per-capita academic performance.
  - `arwu_2024_score`: Scaled total score benchmarked against Harvard University ($= 100.0$).
- **QS Quacquarelli Symonds 2025**:
  - `qs_2025_rank` & `qs_2025_overall_score`: Overall composite rank and cardinal score (0–100 scale).
  - `qs_eng_tech_rank_2024`: Subject-specific Engineering & Technology world rank.
  - `qs_employer_reputation_score`: Direct evaluation score (0–100 scale) based on 50,000+ corporate recruiter surveys worldwide.
- **Emerging Global Employability University Ranking (GEURS 2025)**:
  - `geurs_employability_rank_2025`: Direct global corporate recruiter ranking of graduate workplace effectiveness and technical problem-solving ability.
- **The Technical University Discipline Pivot**:
  $$\Delta_{\text{Eng-Pivot}} = \text{Median}(\text{Rank}_{\text{QS}}, \text{Rank}_{\text{THE}}, \text{Rank}_{\text{ARWU}}) - \text{Rank}_{\text{THE/QS Eng}}$$
  Measures the rank improvement when technical universities are evaluated on their core engineering mission rather than general institutional breadth.

