# Harmonized Research Datasets & Data Dictionary (`datasets/`)

This directory contains deterministic, analysis-ready empirical datasets derived exclusively from `rawdata/` via `src/data_preparation.py`. All indicators are standardized across currencies (Nominal USD & OECD/World Bank PPP International Dollars), institutional accounting boundaries (Tiers 0, 1, and 2), and student enrollment models (Raw Headcount vs. On-Campus Full-Time Equivalent [FTE]).

---

## 1. Catalog of Datasets

| File | Description | Granularity | Key Primary Source Provenance |
| :--- | :--- | :--- | :--- |
| [`university_master_comparison_2024.csv`](./university_master_comparison_2024.csv) | Primary institutional cross-section for all 9 universities across 3-tier budgets, student/faculty supervision, rankings, research efficiency, and Master's career metrics | 9 institutions (3 US, 3 EU, 3 ASIA) | Audited Financial Statements FY24, Common Data Sets / Factbooks, QS 2025, GEURS 2024/2025, CWTS Leiden 2024, World Bank WDI |
| [`external_ecosystem_harmonized_2024.csv`](./external_ecosystem_harmonized_2024.csv) | Granular breakdown of 26 co-located external research institutes across all 9 university ecosystems in local currency, Nominal USD, and PPP International Dollars | 26 research institutes & centers | Max Planck Society, Helmholtz Munich, ESO, MLZ, LRZ, ETH Domain (PSI, Empa, Eawag, WSL), Broad, Whitehead, Lincoln Lab, JPL, GTRI, Crick, BNRist, ETRI, IBS, A*STAR |
| [`masters_10y_cashflow_trajectories.csv`](./masters_10y_cashflow_trajectories.csv) | Annual financial cash-flow and net wealth trajectories ($t = -2 \dots +10$ years) for international STEM Master's students comparing sticker vs. funded paths | 106 annual cohort records across 9 universities | Official graduate tuition schedules, living expense guidelines, MOE GES, and StepStone / BFS / Payscale career progression surveys |
| [`historical_panel_harmonized.csv`](./historical_panel_harmonized.csv) | 15-year longitudinal panel (2010, 2015, 2020, 2024) of student enrollment expansion vs. real core academic budget per FTE indexed to $2010 = 100$ | 36 institutional year points | Historical university annual reports and Destatis / IPEDS longitudinal registries |
| [`literature_empirical_benchmarks.csv`](./literature_empirical_benchmarks.csv) | Full cryptographic catalog of literature benchmarks with exact page/table coordinates and verbatim quotes | 21 verified primary benchmark parameters | Primary research reports, financial statements, and World Bank / OECD statistical series |

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
- **Top-10% Cited Output per \$10M PPP Spend**:
  $$\text{Efficiency}_{\text{Top10}} = \frac{\text{Total Publications} \times (\text{PP}_{\text{top 10\%}} / 100)}{\text{Core Academic Budget}_{\text{PPP}} / 10^7}$$
  Measures field-normalized breakthrough scientific output yield per unit of real purchasing power investment.

### D. International Master's Student Lifecycle & 10-Year Career ROI
- **Total Sticker Degree Cost**: $\text{Tuition}_{\text{Total}} + \text{Living Cost}_{\text{Total}}$ (accounting for 1.0-year UK/SG degrees vs. 1.5–2.0-year US/EU/Asia degrees).
- **Net Degree Cost**: Sticker cost reduced by audited fellowship, graduate research/teaching assistantship (GRA/GTA), and student job (*HiWi*) offset rates.
- **10-Year Post-Tax Net Cumulative Wealth**:
  $$\text{Wealth}(t) = -\text{Net Cost} + \sum_{\tau=1}^{t} \max\left(0, \text{Salary}(\tau) \times (1 - \text{Tax Rate}) - \text{Living}(\tau)\right)$$
- **Payback Horizon**: Smallest year $t^* \in [1, 10]$ where $\text{Wealth}(t^*) \ge 0$.

