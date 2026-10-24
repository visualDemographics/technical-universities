# Systematic Documentation of All Generated Figures (`plots/plot.md`)

This document provides complete methodological provenance, mathematical formulations, empirical validity classifications, and accounting boundaries for all standalone figures and the composite $3 \times 3$ synoptic matrices generated deterministically by `src/modeling.py`.

---

## 1. Summary Catalog of Generated Figures

| Figure Filename | Panel ID | Semantic Topic | Visual Representation | Methodological Classification |
| :--- | :---: | :--- | :--- | :--- |
| [`technical_universities_3x3_en.png`](./technical_universities_3x3_en.png) | **Matrix EN (v1)** | 9-Panel Synoptic Cross-Continental Benchmark (International) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(18, 15)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_de.png`](./technical_universities_3x3_de.png) | **Matrix DE (v1)** | 9-Panel Synoptische Vergleichsmatrix (Deutsch, International) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(18, 15)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_v2_en.png`](./technical_universities_3x3_v2_en.png) | **Matrix EN (v2)** | 9-Panel Synoptic Benchmark (Domestic / In-State Local Tuition Edition) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(18, 15)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_v2_de.png`](./technical_universities_3x3_v2_de.png) | **Matrix DE (v2)** | 9-Panel Synoptische Vergleichsmatrix (Inlandstarife / In-State Edition) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(18, 15)`) | Publikationsreife synoptische Synthese |
| [`panel_a_budget_tiers_ppp.png`](./panel_a_budget_tiers_ppp.png) | **Panel A** | Institutional Accounting Boundaries & External Ecosystems | Grouped Bar Chart (Tiers 0, 1, 2 in Million PPP Int'l \$) | Audited Financial Registry Comparison |
| [`panel_b_enrollment_fte_supervision.png`](./panel_b_enrollment_fte_supervision.png) | **Panel B** | Student Enrollment Scale & On-Campus Denominators | Grouped Bar Chart (Headcount vs. On-Campus FTE) | Administrative Census & Distance-Cohort Split |
| [`panel_c_student_facing_budget_per_fte.png`](./panel_c_student_facing_budget_per_fte.png) | **Panel C** | Corrected Student-Facing Budget per On-Campus FTE | Grouped Bar Chart (Nominal USD vs. PPP Int'l \$) | Price-Level Deflated Per-Capita Ratio |
| [`panel_d_rankings_employability_profile.png`](./panel_d_rankings_employability_profile.png) | **Panel D** | Multi-Pillar Absolute Scores (0–100 Scale) & Global Rankings Profile | Dual-Subplot Architecture: Absolute Cardinal Scores (0–100) vs. The Engineering Pivot (Ranks) | Multi-Source Triangulation & Cardinal Normalization |
| [`panel_e_research_efficiency_multidim.png`](./panel_e_research_efficiency_multidim.png) | **Panel E** | Cost-Normalized High-Impact Research Efficiency | Grouped Bar Chart (Top-10% cited papers per \$10M PPP spend) | Field-Normalized Scientific Output Ratio |
| [`panel_f_2d_efficiency_frontier_surface.png`](./panel_f_2d_efficiency_frontier_surface.png) | **Panel F** | 2D Institutional Efficiency Frontier ($B \times F \to Q$) | 2D Contour Map (`viridis`) with Marginal Conservation | Bivariate Marginal-Preserving Iso-Quality Surface |
| [`panel_g_masters_cost_lifecycle.png`](./panel_g_masters_cost_lifecycle.png) | **Panel G (v1)** | International Master's Total Upfront Investment | Grouped Bar Chart (Sticker Cost vs. Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_g_masters_cost_lifecycle_v2.png`](./panel_g_masters_cost_lifecycle_v2.png) | **Panel G (v2)** | Domestic / In-State Master's Total Upfront Investment | Grouped Bar Chart (Local Sticker vs. Local Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_h_career_outcome_salaries.png`](./panel_h_career_outcome_salaries.png) | **Panel H** | Early-Career vs. 10-Year Career Outcome Salaries | Grouped Bar Chart (Year 1 Median with Mech-CS range, Year 10 Nom USD, Year 10 PPP Int'l \$) | Longitudinal Career Survey Triangulation |
| [`panel_i_10y_salary_roi_trajectories.png`](./panel_i_10y_salary_roi_trajectories.png) | **Panel I (v1)** | 10-Year Post-Graduation Cumulative Net Wealth & ROI (International) | Multi-Line Trajectory ($t = -2 \dots +10$ Career Years) with Disciplinary Sensitivity Bands | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_i_10y_salary_roi_trajectories_v2.png`](./panel_i_10y_salary_roi_trajectories_v2.png) | **Panel I (v2)** | 10-Year Cumulative Net Wealth & ROI (Domestic / In-State Local Tuition) | Multi-Line Trajectory ($t = -2 \dots +10$ Career Years) with Disciplinary Sensitivity Bands | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_shapley_waterfall_decomposition.png`](./panel_shapley_waterfall_decomposition.png) | **Auxiliary Figure 1** | Path-Independent Causal Waterfall (US Private vs. TUM) | 7-Bar Sequential Waterfall with Shapley Value Attributions ($K! = 120$) | Path-Independent Shapley Permutation Model |
| [`panel_historical_panel_trajectories.png`](./panel_historical_panel_trajectories.png) | **Auxiliary Figure 2** | 15-Year Longitudinal Trajectory: Real Budget per FTE | Multi-Line Trajectory (2010–2024 Base 2010 = 100.0) | Price-Deflated Longitudinal Panel Index |

---

## 2. Panel-by-Panel Validity Audit

### Panel A: Accounting Boundaries & External Ecosystems (`panel_a_budget_tiers_ppp.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `tier0_gross_usd_ppp_m`, `tier1_core_usd_ppp_m`, `tier2_augmented_usd_ppp_m`).
- **Mathematical Formulation**:
  $$\text{Tier 0} = \frac{\text{Gross Operating Exp}_{\text{LCU}}}{\text{PPP}_{\text{LCU}}}, \quad \text{Tier 1} = \frac{\text{Gross}_{\text{LCU}} - \text{Hospitals} - \text{FFRDCs}}{\text{PPP}_{\text{LCU}}}, \quad \text{Tier 2} = \text{Tier 1} + \frac{\sum_k (B_k \times w_k)}{\text{PPP}_{\text{LCU}}}$$
- **Statistical Validity**: Complete Audited Financial Statement (`Amtliche_Registerstatistik`).
- **Key Insight**: Caltech's gross spend drops by 74.1% and MIT's by 29.8% once non-student FFRDC pass-throughs (JPL and Lincoln Lab) are removed. TUM's core spend drops by 42.0% after stripping the *Klinikum rechts der Isar*, but expands by €419.4M PPP when incorporating the academically integrated Garching and Munich research cluster.

### Panel B: Enrollment Scale & On-Campus Denominators (`panel_b_enrollment_fte_supervision.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `enrolled_headcount_total`, `on_campus_fte_students`).
- **Mathematical Formulation**: $\text{On-Campus FTE} = \text{Total Headcount} - \text{Online Distance Enrollees}$.
- **Statistical Validity**: Complete Administrative Register (`Amtliche_Registerstatistik`).
- **Key Insight**: Georgia Tech's headline enrollment of 53,350 students conceals 20,850 online distance Master's students (OMSCS/OMSA/OMSCyber). Comparing on-campus FTEs (30,800) prevents a 40% underestimation of campus instructional resources.

### Panel C: Corrected Student-Facing Budget per On-Campus FTE (`panel_c_student_facing_budget_per_fte.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `tier2_per_fte_usd_nom`, `tier2_per_fte_usd_ppp`).
- **Mathematical Formulation**:
  $$\text{Nominal / FTE} = \frac{\text{Tier 2 Budget}_{\text{USD, Nom}}}{N_{\text{FTE}}}, \quad \text{PPP / FTE} = \frac{\text{Tier 2 Budget}_{\text{USD, PPP}}}{N_{\text{FTE}}}$$
- **Statistical Validity**: Price-Level Deflated Indicator (`Amtliche_Registerstatistik` + World Bank ICP).
- **Key Insight**: PPP adjustment significantly enhances the real resource base of Tsinghua ($172k to $191k PPP/FTE), KAIST ($120k to $157k PPP/FTE), and TUM ($31k to $42k PPP/FTE), whereas ETH Zurich's nominal lead is compressed due to Switzerland's high price level index (113.4).

### Panel D: Global Rankings & Multi-Pillar Absolute Evaluation (`panel_d_rankings_employability_profile.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `qs_2025_rank`, `qs_2025_overall_score`, `the_2025_rank`, `the_2025_overall_score`, `the_eng_tech_rank_2025`, `arwu_2024_rank`, `arwu_2024_score`, `qs_employer_reputation_score`, `geurs_employability_rank_2025`).
- **Mathematical Formulation & Normalization**:
  $$\text{Academic Score Composite} \in [0, 100], \quad \text{Employer Score} \in [0, 100]$$
  Evaluates both **absolute cardinal performance** (standardized 0–100 scores across QS, THE, and Employer surveys) and **ordinal rank shifts**:
  $$\Delta_{\text{Eng-Pivot}} = \text{Median}(\text{Rank}_{\text{QS}}, \text{Rank}_{\text{THE}}, \text{Rank}_{\text{ARWU}}) - \text{Rank}_{\text{THE/QS Eng}}$$
- **Visual Architecture**:
  - **3x3 Matrix Edition**: A 3-bar grouped cardinal evaluation per university on an absolute 0–100 scale (QS Overall, THE Overall, QS Employer Reputation) grounded at 0, overlaid with reference benchmarks (Top 10 Tier $\ge 90.0$; World Elite Tier $\ge 80.0$) and exact ordinal rank callouts (`QS | THE | Eng | GEURS`).
  - **Standalone Edition (`panel_d_rankings_employability_profile.png`)**: A 2-subplot deep-dive architecture:
    - **Subplot A (Left)**: Multi-Pillar Absolute Cardinal Scores (0–100 Scale) with reference lines.
    - **Subplot B (Right)**: The Technical University Pivot, contrasting General Comprehensive Ranks (median of QS, THE, ARWU) against Engineering Discipline Ranks (THE/QS Engineering) and Corporate Employability Ranks (GEURS).
- **Statistical Validity**: Triangulated Global Institutional Audit across 4 independent evaluation systems (Times Higher Education 2025, QS Quacquarelli Symonds 2025, ShanghaiRanking ARWU 2024, and Emerging/GEURS 2025).
- **Key Analytical Insights**:
  1. **The Fallacy of Ordinal Ranks**: In ordinal rank space, an institution ranked #28 (TUM) appears far inferior to #1 (MIT). In absolute cardinal score space, TUM scores **84.0 in QS** and **83.5 in THE** (firmly within the World Elite Tier $\ge 80.0$), and achieves **97.2 out of 100 in Employer Reputation**—virtually indistinguishable from MIT's 100.0.
  2. **The General vs. Engineering Discipline Surge**: General rankings penalize specialized technical universities lacking medical schools, law faculties, or massive humanities divisions. In specialized **Engineering & Technology Discipline Tables**, public technical powerhouses surge dramatically:
     - **Georgia Tech**: Jumps from general rank #114 (QS) / #175 (ARWU) to **#15 globally** in Engineering (+99 to +160 positions).
     - **TUM**: Jumps from general rank #28 (QS) / #47 (ARWU) to **#19** (QS Eng) / **#22** (THE Eng) and **#13 globally** in GEURS Employability.
     - **NTU Singapore**: Jumps from general rank #30 (THE) / #90 (ARWU) to **#15 globally** in Engineering.
     - **KAIST**: Jumps from general rank #82 (THE) / #250 (ARWU) to **#23 / #35** in Engineering.
  3. **Employer Reputation Supremacy**: Global corporate recruiters prioritize engineering problem-solving rigor over institutional age or humanities breadth. Public powerhouses (Tsinghua 99.2, Imperial 99.5, TUM 97.2, NTU 96.4, ETH 95.8) form an ultra-elite cluster matching or exceeding private US Ivy institutions.

### Panel E: Cost-Normalized Research Efficiency (`panel_e_research_efficiency_multidim.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `annual_top10_pubs_per_10m_ppp_spend`, `top10_pubs_per_10m_ppp_spend`).
- **Mathematical Formulation**:
  $$\text{Annual Efficiency} = \frac{(\text{Total Publications}_{2019-2022} / 4.0) \times (\text{PP}_{\text{top 10\%}} / 100)}{\text{Tier 1 Core Academic Budget}_{\text{PPP}} / 10^7}$$
- **Statistical Validity**: Field-Normalized Bibliometric Impact Ratio (CWTS Leiden Ranking 2024).
- **Key Insight**: Annualized breakthrough research yields per \$10M PPP core spend are led by NTU (10.36/yr), Imperial (9.55/yr), Caltech (9.08/yr), ETH Zurich (8.45/yr), TUM (7.62/yr), MIT (7.36/yr), Georgia Tech (5.99/yr), KAIST (5.88/yr), and Tsinghua (3.13/yr).

### Panel F: 2D Institutional Efficiency Frontier (`panel_f_2d_efficiency_frontier_surface.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` across budget per FTE ($B$), faculty ratio ($F$), and CWTS Leiden Top-10% breakthrough share ($Y$).
- **Mathematical Formulation**: $\text{Top10\%}(B, F) = c_0 + \beta \ln(B) + \gamma \ln(F)$ fitted via `scipy.optimize.curve_fit` to empirical observations.
- **Statistical Validity**: Non-linear response surface with verified empirical sample mean preservation ($|\bar{Y}_{\text{obs}} - \bar{Y}_{\text{pred}}| < 10^{-4}$), explicit goodness-of-fit ($R^2 = 0.59$), and runtime-asserted slice-wise marginal conservation ($|\mathbb{E}_F[Q(B, F)] - \hat{Y}(B)| < 10^{-10}$).
- **Key Insight**: Maps three distinct institutional production regimes: (1) The Boutique Endowment Regime (Caltech & MIT, high spend & high supervision density), (2) The Public Core & Ecosystem Regime (ETH Zurich & Imperial, intermediate scale & strong core state funding), and (3) The Mass-Enrollment Innovation Frontier (TUM, Tsinghua, Georgia Tech, NTU, KAIST, high-throughput efficiency).

### Panel G: International Master's Total Upfront Investment (`panel_g_masters_cost_lifecycle.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `total_sticker_cost_usd`, `net_total_degree_cost_usd`).
- **Mathematical Formulation**:
  $$\text{Sticker Cost} = \text{Tuition}_{\text{Total}} + \text{Living Cost}_{\text{Total}}, \quad \text{Net Cost} = \text{Sticker Cost} - \text{Fellowship/TA/RA/HiWi Offsets}$$
- **Statistical Validity**: Audited Graduate Admissions & Financial Aid Guidelines.
- **Key Insight**: KAIST (\$1,683 net) and Tsinghua (\$11,340 net) provide heavily subsidized degrees with stipends. TUM (\$49,123 net over 2 years) and ETH (\$66,892 net over 2 years) remain 40%–60% cheaper than MIT (\$117,490 net) and Caltech (\$106,575 net).

### Panel G (v2): Domestic / In-State Master's Total Upfront Investment (`panel_g_masters_cost_lifecycle_v2.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `local_total_sticker_cost_usd`, `local_net_total_degree_cost_usd`).
- **Mathematical Formulation**:
  $$\text{Local Sticker Cost} = \text{Local Tuition}_{\text{Total}} + \text{Living Cost}_{\text{Total}}$$
  $$\text{Local Net Cost} = \text{Local Tuition}_{\text{Total}} \times (1 - \text{Offset Rate}) + \text{Living Cost}_{\text{Total}}$$
- **Statistical Validity**: Audited Graduate Admissions & Domestic/In-State Bursar Schedules (`Amtliche_Registerstatistik`).
- **Key Insight**: Incorporating domestic and state-residency tuition subsidies fundamentally alters the European and public US investment equation:
  - **TUM**: German/EU domestic students pay **€0 tuition**, dropping total net degree expenses from \$49,123 to **\$22,787** (living costs only minus HiWi offset).
  - **Georgia Tech**: US in-state graduate tuition drops total net degree expenses from \$70,241 down to **\$50,467** (a \$19,774 direct state-taxpayer subsidy).
  - **Imperial College London**: UK Home fee status drops total net degree costs from \$73,583 to **\$49,139** (a \$24,444 savings).
  - **ETH Zurich**: Swiss domestic standard fees drop total net degree costs from \$66,892 to **\$45,276** (a \$21,616 savings).
  - **NTU Singapore**: Singapore citizen subsidized tuition reduces net costs from \$48,041 to **\$22,195**.
  - **Tsinghua & KAIST**: Domestic academic scholarship fees drop net upfront costs to **\$4,892** and **\$1,100** respectively.
  - **MIT & Caltech (US Private Endowments)**: Private US institutions offer no in-state residency subsidies; adhering strictly to the user constraint of *no need-based cuts for family income*, their net costs remain invariant at full sticker aid rates (**\$117,490** and **\$106,575**).

### Panel H: Early-Career vs. 10-Year Career Outcome Salaries (`panel_h_career_outcome_salaries.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` (columns: `year1_median_salary_usd`, `year1_mech_salary_usd`, `year1_cs_ai_salary_usd`, `year10_median_salary_usd`, `year10_median_salary_ppp`).
- **Mathematical Formulation**:
  $$\text{Nominal Disparity Spread} = S_{\text{CS/AI}} - S_{\text{Mech}}, \quad \text{PPP Salary} = \frac{S_{10,\text{Nominal, LCU}}}{\text{PPP}_{\text{LCU}}}$$
- **Statistical Validity**: Official Graduate Career Registry & Longitudinal Industry Survey Triangulation (Emolument, Payscale, HESA, Hochschul-Bildungs-Report).
- **Key Insight**: In Nominal USD, US private elites (MIT \$196.9k, Caltech \$192.0k, Georgia Tech \$168.0k) and ETH Zurich (\$153.3k) lead at Year 10. However, in Purchasing Power Parity (PPP Int'l \$), Asian powerhouses Tsinghua (\$260.7k PPP), NTU (\$225.7k PPP), and KAIST (\$197.3k PPP) match or surpass US nominal compensation due to lower domestic price levels. TUM reaches \$134.1k PPP. Disciplinary error bars show CS/AI graduates commanding 15%–30% higher entry packages than Mechanical Engineers across all institutions.

### Panel I: 10-Year Cumulative Post-Tax Wealth & ROI Trajectories (`panel_i_10y_salary_roi_trajectories.png`)
- **Input Data**: `datasets/masters_10y_cashflow_trajectories.csv` (columns: `career_year`, `cumulative_wealth_funded_usd`, `cumulative_wealth_cs_usd`, `cumulative_wealth_mech_usd`).
- **Mathematical Formulation**:
  $$W(t) = -C_{\text{net}} + \sum_{\tau=1}^{t} \max\left(0, S(\tau) \times (1 - \text{Tax Rate}) - L(\tau)\right)$$
- **Statistical Validity**: Longitudinal Cashflow Simulation based on Official Graduate Employment Registries with CS/AI vs. Mechanical Engineering sensitivity bands.
- **Key Insight**: Tracks all 9 universities across their regional tech hub placements with shaded disciplinary uncertainty bounds. Break-even occurs fastest at KAIST (1 yr) and Tsinghua (1 yr), followed by MIT (2 yrs), ETH (2 yrs), Georgia Tech (2 yrs), NTU (2 yrs), Caltech (3 yrs), TUM (3 yrs), and Imperial (7 yrs due to London living costs). Over 10 years, MIT (\$718k) and ETH (\$572k) lead in cumulative post-tax savings.

### Panel I (v2): 10-Year Cumulative Post-Tax Wealth & ROI Trajectories (Domestic / In-State Edition) (`panel_i_10y_salary_roi_trajectories_v2.png`)
- **Input Data**: `datasets/masters_10y_cashflow_trajectories.csv` (columns: `career_year`, `cumulative_wealth_local_usd`, `cumulative_wealth_local_cs_usd`, `cumulative_wealth_local_mech_usd`).
- **Mathematical Formulation**:
  $$W_{\text{local}}(t) = -C_{\text{net, local}} + \sum_{\tau=1}^t \max\left(0, S(\tau)(1 - \text{Tax Rate}) - L(\tau)\right)$$
- **Statistical Validity**: Longitudinal Cashflow Simulation based on Domestic Tuition Feeregs and Official Graduate Employment Registries with CS/AI vs. Mechanical Engineering sensitivity bands.
- **Key Insight**: Comparing domestic/in-state student cohorts accelerates break-even points and elevates cumulative career wealth across public institutions:
  - **Accelerated Break-Even Horizons**:
    - **Georgia Tech (US In-State)**: Break-even accelerates to **Year 1** (down from Year 2 for out-of-state/international).
    - **Imperial College London (UK Home)**: Break-even accelerates to **Year 5** (down from Year 7).
    - **ETH Zurich (Swiss Domestic)**: Break-even accelerates to **Year 1** (down from Year 2).
    - **TUM (German/EU Tuition-Free)**: Break-even accelerates to **Year 2** (down from Year 3).
    - **NTU Singapore (Citizen Subsidized)**: Break-even accelerates to **Year 1** (down from Year 2).
  - **10-Year Cumulative Post-Tax Wealth Expansion**:
    - **Georgia Tech**: \$685,748 (+\$22,598 vs v1), closely approaching MIT (\$718k) due to low in-state debt and high Atlanta/US tech compensation.
    - **Imperial**: \$104,085 (+\$24,444 vs v1), overcoming London living cost pressures earlier.
    - **ETH Zurich**: \$593,558 (+\$21,616 vs v1), ranking second globally only to MIT.
    - **TUM**: \$220,338 (+\$26,336 vs v1), delivering a clean return on zero-tuition investment.
    - **NTU Singapore**: \$608,454 (+\$25,846 vs v1), surpassing Caltech (\$605k) in total 10-year accumulated wealth.
    - **MIT & Caltech**: Invariant at \$718,206 and \$605,039 due to lack of in-state discounts and strict enforcement of the no-income-cuts constraint.

### Auxiliary Figure 1: Path-Independent Shapley Waterfall Decomposition (`panel_shapley_waterfall_decomposition.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` and `datasets/literature_empirical_benchmarks.csv` (MIT/Caltech average vs. TUM).
- **Mathematical Formulation**: Evaluates all $5! = 120$ permutation sequences in `compute_shapley_waterfall_decomposition`:
  $$\phi_j = \frac{1}{K!} \sum_{\pi} \Delta_j(\pi)$$
- **Statistical Validity**: Path-Independent Causal Decomposition with exact efficiency axiom preservation.
- **Key Insight**: The raw headline funding gap of \$889k per student collapses by **65.7%** down to \$305k per student: stripping defense FFRDCs accounts for $-\$602\text{k}$ ($\phi$), stripping clinical hospitals adds $+\$19\text{k}$ ($\phi$), crediting external campus research ecosystems adds $+\$11\text{k}$ ($\phi$), German purchasing power parity (PPP) reduces the gap by $-\$11\text{k}$ ($\phi$), and on-campus FTE denominator normalization reduces it by $-\$1.4\text{k}$ ($\phi$).

### Auxiliary Figure 2: 15-Year Longitudinal Trajectory: Real Budget per FTE (`panel_historical_panel_trajectories.png`)
- **Input Data**: `datasets/historical_panel_harmonized.csv` (columns: `year`, `on_campus_fte`, `real_budget_per_fte_usd_ppp`, `budget_per_fte_index_2010`).
- **Mathematical Formulation**:
  $$\text{Index}_{u, t} = \frac{\text{Budget per FTE}_{u, t, \text{PPP}}}{\text{Budget per FTE}_{u, 2010, \text{PPP}}} \times 100.0$$
- **Statistical Validity**: Multi-Year Price-Level Deflated Panel Index ($2010 = 100.0$).
- **Key Insight**: Documents divergent institutional trajectories from 2010 to 2024: Tsinghua University experienced unprecedented real per-student resource expansion ($+206\%$ index surge to 306.2), while mass-enrollment European universities maintained steady real support (TUM at 103.3, ETH Zurich at 95.7, and Imperial at 120.3) despite rapid student body expansion. MIT and Caltech expanded per-student resources by $+54\%$ and $+53\%$ respectively.

