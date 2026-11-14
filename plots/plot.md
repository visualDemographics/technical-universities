# Systematic Documentation of All Generated Figures (`plots/plot.md`)

This document provides complete methodological provenance, mathematical formulations, empirical validity classifications, and accounting boundaries for all standalone figures, the 4-variant bottom-row comparison matrix, and the composite $3 \times 3$ synoptic matrices generated deterministically by `src/modeling.py`.

---

## 1. Summary Catalog of Generated Figures

| Figure Filename | Panel ID | Semantic Topic | Visual Representation | Methodological Classification |
| :--- | :---: | :--- | :--- | :--- |
| [`technical_universities_4x3.png`](./technical_universities_4x3.png) | **Matrix 4x3 (Default/EN)** | 12-Panel Synoptic Benchmark (Row 3: Bachelor Intl, Row 4: Master Domestic) | Composite $4 \times 3$ Synthesis Matrix (`figsize=(19, 21.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_4x3_en.png`](./technical_universities_4x3_en.png) | **Matrix 4x3 EN (Intl Bac / Dom Mas)** | 12-Panel Synoptic Benchmark (Row 3: Bachelor Intl, Row 4: Master Domestic) | Composite $4 \times 3$ Synthesis Matrix (`figsize=(19, 21.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_4x3_de.png`](./technical_universities_4x3_de.png) | **Matrix 4x3 DE (Intl Bac / Dom Mas)** | 12-Panel Synoptische Matrix (Zeile 3: Bachelor Intl, Zeile 4: Master Einheimisch) | Verbundene $4 \times 3$ Synthesematrix (`figsize=(19, 21.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_4x3_domestic_en.png`](./technical_universities_4x3_domestic_en.png) | **Matrix 4x3 Domestic EN** | 12-Panel Synoptic Benchmark (Row 3: Bachelor Domestic, Row 4: Master Domestic) | Composite $4 \times 3$ Synthesis Matrix (`figsize=(19, 21.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_4x3_domestic_de.png`](./technical_universities_4x3_domestic_de.png) | **Matrix 4x3 Domestic DE** | 12-Panel Synoptische Matrix (Zeile 3: Bachelor Einheimisch, Zeile 4: Master Einheimisch) | Verbundene $4 \times 3$ Synthesematrix (`figsize=(19, 21.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_en.png`](./technical_universities_3x3_en.png) | **Matrix EN (Baseline/v1)** | 9-Panel Synoptic Benchmark (Master's International Edition) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(19, 16.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_de.png`](./technical_universities_3x3_de.png) | **Matrix DE (Baseline/v1)** | 9-Panel Synoptische Vergleichsmatrix (Master International) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(19, 16.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_v1_en.png`](./technical_universities_3x3_v1_en.png) | **Matrix EN (v1)** | 9-Panel Synoptic Benchmark (Master's Non-Native / International) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(19, 16.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_v1_de.png`](./technical_universities_3x3_v1_de.png) | **Matrix DE (v1)** | 9-Panel Synoptische Matrix (Master Nicht-Einheimisch / International) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(19, 16.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_v2_en.png`](./technical_universities_3x3_v2_en.png) | **Matrix EN (v2)** | 9-Panel Synoptic Benchmark (Master's Native / Domestic / In-State) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(19, 16.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_v2_de.png`](./technical_universities_3x3_v2_de.png) | **Matrix DE (v2)** | 9-Panel Synoptische Matrix (Master Einheimisch / In-State) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(19, 16.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_v3_en.png`](./technical_universities_3x3_v3_en.png) | **Matrix EN (v3)** | 9-Panel Synoptic Benchmark (Bachelor's Non-Native / International) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(19, 16.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_v3_de.png`](./technical_universities_3x3_v3_de.png) | **Matrix DE (v3)** | 9-Panel Synoptische Matrix (Bachelor Nicht-Einheimisch / International) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(19, 16.5)`) | Publikationsreife synoptische Synthese |
| [`technical_universities_3x3_v4_en.png`](./technical_universities_3x3_v4_en.png) | **Matrix EN (v4)** | 9-Panel Synoptic Benchmark (Bachelor's Native / Domestic / In-State) | Composite $3 \times 3$ Synthesis Matrix (`figsize=(19, 16.5)`) | Publication-Grade Synoptic Synthesis |
| [`technical_universities_3x3_v4_de.png`](./technical_universities_3x3_v4_de.png) | **Matrix DE (v4)** | 9-Panel Synoptische Matrix (Bachelor Einheimisch / In-State) | Verbundene $3 \times 3$ Synthesematrix (`figsize=(19, 16.5)`) | Publikationsreife synoptische Synthese |
| [`bottom_row_4_variants_comparison.png`](./bottom_row_4_variants_comparison.png) | **Bottom-Row Matrix** | 4-Cohort Comparative Synthesis (Master & Bachelor x Native & Non-Native) | $4 \times 3$ Composite Grid (`figsize=(19, 21)`) | Cross-Cohort Comparative Simulation |
| [`bottom_row_4_variants_comparison_en.png`](./bottom_row_4_variants_comparison_en.png) | **Bottom-Row Matrix (EN)** | 4-Cohort Comparative Synthesis (English) | $4 \times 3$ Composite Grid (`figsize=(19, 21)`) | Cross-Cohort Comparative Simulation |
| [`bottom_row_4_variants_comparison_de.png`](./bottom_row_4_variants_comparison_de.png) | **Bottom-Row Matrix (DE)** | 4-Kohorten Vergleichende Synthese (Deutsch) | $4 \times 3$ Zusammengesetzte Matrix (`figsize=(19, 21)`) | Cross-Cohort Comparative Simulation |
| [`panel_a_budget_tiers_ppp.png`](./panel_a_budget_tiers_ppp.png) | **Panel A** | Institutional Operating Budgets (Nominal USD Tiers 0, 1, 2) | 3-Bar Grouped Bar Chart (Tier 0 Gross Operating Exp, Tier 1 Core Academic, Tier 2 Augmented Student-Facing in Nominal USD) | Audited Financial Registry Comparison |
| [`panel_b_enrollment_fte_supervision.png`](./panel_b_enrollment_fte_supervision.png) | **Panel B** | Student Enrollment Scale & On-Campus Denominators | Grouped Bar Chart (Headcount vs. On-Campus FTE) | Administrative Census & Distance-Cohort Split |
| [`panel_c_student_facing_budget_per_fte.png`](./panel_c_student_facing_budget_per_fte.png) | **Panel C** | Corrected Student-Facing Budget per On-Campus FTE | Grouped Bar Chart (Nominal USD / FTE vs. PPP Int'l \$ / FTE) | Price-Level Deflated Per-Capita Ratio |
| [`panel_d_rankings_employability_profile.png`](./panel_d_rankings_employability_profile.png) | **Panel D** | Multi-Pillar Absolute Scores & Global Multi-Ranking Profile | Dual-Subplot Architecture: Absolute Cardinal Scores (0–100) vs. Multi-System Global Profile | Multi-Source Triangulation & Cardinal Normalization |
| [`panel_e_research_efficiency_multidim.png`](./panel_e_research_efficiency_multidim.png) | **Panel E** | Cost-Normalized High-Impact Research Efficiency | Grouped Bar Chart (Top-10% cited papers per \$10M PPP spend) | Field-Normalized Scientific Output Ratio |
| [`panel_f_2d_efficiency_frontier_surface.png`](./panel_f_2d_efficiency_frontier_surface.png) | **Panel F** | Undergraduate Admissions Selectivity & Exam Screening | Grouped Bar Chart (Admissions Acceptance Rate % vs. First-Year Exam Screening Attrition %) | Institutional Selectivity & Filtering Paradigm |
| [`panel_g_masters_cost_lifecycle.png`](./panel_g_masters_cost_lifecycle.png) | **Panel G (Master Intl)** | International Master's Total Upfront Investment | Grouped Bar Chart (Sticker Cost vs. Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_g_masters_cost_lifecycle_v2.png`](./panel_g_masters_cost_lifecycle_v2.png) | **Panel G (Master Domestic)** | Domestic / In-State Master's Total Upfront Investment | Grouped Bar Chart (Local Sticker vs. Local Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_g_bachelors_cost_lifecycle.png`](./panel_g_bachelors_cost_lifecycle.png) | **Panel G (Bachelor Intl)** | International Bachelor's Total Upfront Investment | Grouped Bar Chart (Sticker Cost vs. Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_g_bachelors_cost_lifecycle_v2.png`](./panel_g_bachelors_cost_lifecycle_v2.png) | **Panel G (Bachelor Domestic)** | Domestic / In-State Bachelor's Total Upfront Investment | Grouped Bar Chart (Local Sticker vs. Local Net Out-of-Pocket) | Total Cost of Ownership (TCO) Model |
| [`panel_h_career_outcome_salaries.png`](./panel_h_career_outcome_salaries.png) | **Panel H (Master)** | Early-Career, 10-Year & 20-Year Master's Career Outcome Salaries | Grouped Bar Chart (Year 1 Starting, Year 10 Mid-Career, Year 20 Senior Nom USD & PPP Int'l \$) | Longitudinal Career Survey Triangulation |
| [`panel_h_career_outcome_salaries_bachelors.png`](./panel_h_career_outcome_salaries_bachelors.png) | **Panel H (Bachelor)** | Early-Career, 10-Year & 20-Year Bachelor's Career Outcome Salaries | Grouped Bar Chart (Year 1 Starting, Year 10 Mid-Career, Year 20 Senior Nom USD & PPP Int'l \$) | Longitudinal Career Survey Triangulation |
| [`panel_i_10y_salary_roi_trajectories.png`](./panel_i_10y_salary_roi_trajectories.png) | **Panel I (Master Intl)** | 20-Year Career ROI Multiple & Excess Wealth vs. No-College Baseline (Master Intl) | Multi-Line Trajectory (ROI Multiple x & +\$ Excess Wealth) with MechEng-to-CS/AI Band | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_i_10y_salary_roi_trajectories_v2.png`](./panel_i_10y_salary_roi_trajectories_v2.png) | **Panel I (Master Domestic)** | 20-Year Career ROI Multiple & Excess Wealth vs. No-College Baseline (Master Domestic) | Multi-Line Trajectory (ROI Multiple x & +\$ Excess Wealth) with MechEng-to-CS/AI Band | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_i_10y_salary_roi_trajectories_bachelors.png`](./panel_i_10y_salary_roi_trajectories_bachelors.png) | **Panel I (Bachelor Intl)** | 20-Year Career ROI Multiple & Excess Wealth vs. No-College Baseline (Bachelor Intl) | Multi-Line Trajectory (ROI Multiple x & +\$ Excess Wealth) with MechEng-to-CS/AI Band | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_i_10y_salary_roi_trajectories_bachelors_v2.png`](./panel_i_10y_salary_roi_trajectories_bachelors_v2.png) | **Panel I (Bachelor Domestic)** | 20-Year Career ROI Multiple & Excess Wealth vs. No-College Baseline (Bachelor Domestic) | Multi-Line Trajectory (ROI Multiple x & +\$ Excess Wealth) with MechEng-to-CS/AI Band | Longitudinal After-Tax Cash Flow Simulation |
| [`panel_shapley_waterfall_decomposition.png`](./panel_shapley_waterfall_decomposition.png) | **Auxiliary Figure 1** | Path-Independent Causal Waterfall (US Private vs. TUM) | 6-Bar Sequential Waterfall with Shapley Value Attributions ($K! = 120$) | Path-Independent Shapley Permutation Model |
| [`panel_historical_panel_trajectories.png`](./panel_historical_panel_trajectories.png) | **Auxiliary Figure 2** | 15-Year Longitudinal Trajectory: Real Budget per FTE | Multi-Line Trajectory (2010–2024 Base 2010 = 100.0) | Price-Deflated Longitudinal Panel Index |

---

## 2. Methodological & Validity Audits

### The 4 Bottom-Row Lifecycle Variants (`bottom_row_4_variants_comparison.png`)
To provide comprehensive lifecycle evaluation, the bottom row of the synoptic matrix (Panels G, H, I) is modeled and rendered across a full $2 \times 2$ factorial design:
1. **Master's Degree — International (Non-Native)**: Overseas tuition rates and living expenses with baseline fellowships and graduate student employment (RA/TA/HiWi).
2. **Master's Degree — Domestic / In-State (Native)**: In-state statutory tuition discounts (US public), UK Home fees, Swiss domestic matura fees, and German/EU tuition-free status under BayHIG.
3. **Bachelor's Degree — International (Non-Native)**: 3-year (Imperial BEng cohort-locked) and 4-year empirical engineering median duration (MIT, Caltech, GT, ETH Zurich, TUM, Tsinghua, KAIST, NTU) undergraduate degrees under international tuition schedules.
4. **Bachelor's Degree — Domestic / In-State (Native)**: Undergraduate programs under statutory home student caps (£9,250 in UK, Georgia in-state Zell Miller scholarships, CHF 1,460/yr Swiss domestic, 0 EUR German tuition).

### Panel D: Global Rankings & Multi-Pillar Absolute Evaluation (`panel_d_rankings_employability_profile.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` across QS 2025, THE 2025, ARWU 2024, US News 2025, THE Engineering 2025, and GEURS Employability 2025.
- **Overlapping Text Elimination**:
  1. Expanded headroom to $y \in [0, 140]$.
  2. Implemented vertical alternation for text badges (`y = max_bar + 2.5` for even index; `y = max_bar + 9.5` for odd index). Adjacent text blocks never collide horizontally.
  3. Relocated reference line labels to the left margin ($x = -0.45$).
  4. Positioned legend in upper right over KAIST and Georgia Tech where bars reach only $y \le 78$.
- **Expanded Global Rankings**: Integrates US News Best Global Universities 2024-2025 (MIT #2, Caltech #7, Georgia Tech #33, Imperial #12, ETH Zurich #28, TUM #28, Tsinghua #16, KAIST #120, NTU #27), QS Engineering, THE Engineering, ARWU, and GEURS.

### Panel F: Admissions Selectivity & First-Year Cohort Attrition (`panel_f_2d_efficiency_frontier_surface.png`)
- **Input Data**: `datasets/university_master_comparison_2024.csv` across `undergrad_acceptance_rate_pct` and `first_year_screening_attrition_pct`.
- **The Core Institutional Insight (Gatekeeper vs. Examination Sieve)**:
  1. **The Anglo-Saxon & Asian "Gatekeeper Model"** (Tsinghua ~0.03% Gaokao / 1.0%, Caltech 3.1%, MIT 4.5%, Imperial 11.2%): Extreme upfront filtering at the admissions gate, with first-year cohort attrition near zero (1%–4%).
  2. **The Continental European "Examination Sieve Model"** (ETH Zurich 28.0% overall / 100% statutory access for Swiss Matura; TUM 35.0% overall / 45% German/EU): Broad access at the admissions gate, coupled with rigorous first-year academic screening (**ETH Zurich *Basisprüfung* actual 1st-year cohort attrition: 20.0%** [out of 31% total multi-year attrition / 69% BFS Bachelor completion, as 1st-attempt non-passers may repeat once]; **TUM *Grundlagen- und Orientierungsprüfung* [GOP] actual 1st-year cohort attrition: 15.0%** [out of 20.0% total 8-semester EFV exmatriculation]).
  3. **The State Flagship / Merit Gate Model** (Georgia Tech 16.0%, NTU 17.5%, KAIST 18.0%): In-state / national science quotas with moderate initial selectivity and high retention (3.0%–4.5% 1st-year attrition).
- **Visual Architecture**: Grouped bar chart comparing Admissions Acceptance Rate (navy `#1F407A`) against First-Year Cohort Attrition (coral `#D9534F`) with annotated percentages and directional callouts. Headroom set to $y \in [0, 44]$ to ensure zero collisions with titles and legends.

### Zero-Collision 3x3 Matrix Grid Layout
- Enlarged composite matrix dimensions from `(18, 15)` to `(19, 16.5)`.
- Increased vertical spacing `hspace` from `0.32` to `0.46`, expanding vertical clearance between rows by over 40%.
- Adjusted horizontal spacing `wspace=0.28`.
- Formatted university x-axis tick labels to 30-degree rotation (`ha="right"`, `fontsize=7.5`), ensuring labels never encroach on lower subplot titles.

### 12-Panel Composite Matrix ($4 \times 3$ Synoptic Matrix Architecture)
- **Matrix Dimensions & Visual Geometry**: Rendered at `figsize=(19, 21.5)` with `hspace=0.46` and `wspace=0.28` (`technical_universities_4x3_en.png`, `technical_universities_4x3_de.png`, `technical_universities_4x3_domestic_en.png`, `technical_universities_4x3_domestic_de.png`).
- **Row-by-Row Structural Architecture**:
  - **Row 1 (Macro Financial Framework)**:
    - **Panel A**: Institutional Accounting Boundaries (Nominal USD Gross/Core/Augmented vs. PPP Int'l \$).
    - **Panel B**: Student Enrollment Scale & Supervision (Headcount vs On-Campus FTE).
    - **Panel C**: Student-Facing Operating Resource per On-Campus FTE (Nominal USD vs. PPP Int'l \$).
  - **Row 2 (Academic Quality & Global Benchmarking)**:
    - **Panel D**: Multi-Ranking Standing & Absolute Scores (US News, QS, THE, ARWU, GEURS, Leiden).
    - **Panel E**: Field-Normalized High-Impact Research Efficiency (Top-10% cited papers per \$10M PPP).
    - **Panel F**: Undergraduate Admissions Selectivity & First-Year Exam Screening Attrition (%).
  - **Row 3 (Bachelor's Lifecycle & Net Wealth Dynamics)**:
    - **Panel G (Bachelor)**: Undergraduate Total Degree Investment (Tuition, Living Costs & Median Degree Duration).
    - **Panel H (Bachelor)**: Undergraduate Early-Career, 10-Year & 20-Year Career Outcome Salaries.
    - **Panel I (Bachelor)**: 24-Year Post-Matriculation Economic ROI Multiple & Excess Wealth Trajectories.
  - **Row 4 (Master's Domestic Lifecycle & Net Wealth Dynamics)**:
    - **Panel G (Master Domestic)**: Domestic Master's Total Degree Investment (Tuition, Living Costs & Median Degree Duration).
    - **Panel H (Master Domestic)**: Master's Early-Career, 10-Year & 20-Year Career Outcome Salaries.
    - **Panel I (Master Domestic)**: 22-Year Post-Matriculation Economic ROI Multiple & Excess Wealth Trajectories.
- **Language & Cohort Variants**:
  - `technical_universities_4x3_en.png`: English edition with Row 3 International Bachelor and Row 4 Domestic Master.
  - `technical_universities_4x3_de.png`: German edition with Row 3 International Bachelor and Row 4 Domestic Master.
  - `technical_universities_4x3_domestic_en.png`: English edition with Row 3 Domestic Bachelor and Row 4 Domestic Master.
  - `technical_universities_4x3_domestic_de.png`: German edition with Row 3 Domestic Bachelor and Row 4 Domestic Master.

### Panel A: Institutional Operating Budgets (Nominal USD Tiers 0, 1, 2)
- **3-Bar Clean Nominal Architecture**:
  1. **Tier 0 Gross Operating Exp (Nominal)**: Total consolidated unadjusted financial budget converted at market FX rates to Nominal USD.
  2. **Tier 1 Core Academic ex-Hospital/FFRDC**: Core student/academic budget stripped of off-campus clinical hospitals and national defense FFRDCs.
  3. **Tier 2 Augmented Student-Facing (Ecosystem)**: Attributable co-located partner research institutes (Max Planck, Helmholtz, ETH Domain, Broad, A*STAR).
- **Narrative Motivation**: Panel A establishes macro-level institutional accounting boundaries cleanly in Nominal USD, highlighting the vast gap between gross statutory figures (inflated by hospitals and defense labs) and core academic operations before PPP deflation is introduced in Panel C.

### Panel C: Corrected Student-Facing Budget per On-Campus FTE (Nominal vs. PPP)
- **Side-by-Side Dual-Currency Architecture**:
  - Compares **Nominal USD / FTE** against **PPP Int'l $ / FTE** across all 9 universities without visual clutter or error whiskers.
  - Demonstrates the dramatic purchasing power divergence between nominal currency exchange rates and real local educational resources in Europe and Asia.

### Panel G: Undergraduate & Graduate Net Price Modeling (`Tuition, Living Costs & Median Degree Duration`)
- **Grouped Bar Architecture & Explicit Subtitle**:
  - Displays Total Sticker Cost alongside Net Out-of-Pocket Cost across empirical median degree durations (`1.0 yr` Imperial/NTU MSc vs. `1.5–2.0 yr` other MS; `3.0 yr` Imperial BEng vs. `4.0 yr` empirical engineering median for ETH Zurich, TUM, US, and Asia), titled `Panel G: Total Degree Investment (<Cohort>)\n(Tuition, Living Costs & Median Degree Duration)`.
  - Reflects the official **U.S. Department of Education IPEDS Median Net Price for Aided Students** for US domestic students, statutory domestic rates for Europe and Asia, and verified research/teaching assistantship (RA/TA/HiWi) and bursary offsets (`€12.41–€14.00/hr` TUM HiWi, `CHF 30.70/hr` ETH *Hilfsassistierende*, Imperial Bursary).

### Panel H: Career Outcome Salaries (Year 1, Year 10 & Year 20)
- **4-Bar Architecture**:
  - Reports **Year 1 Starting Median Salaries (Nominal USD)**, **Year 10 Mid-Career Median (Nominal USD)**, **Year 20 Senior Median (Nominal USD)**, and **Year 20 Senior Median in World Bank PPP International Dollars**.
  - Provides a clean, direct comparison of entry-level, mid-career, and 20-year senior compensation across all 9 tech hubs.

### Panel I: Post-Matriculation Economic ROI Multiple (Excess Wealth / Total Economic Investment)
- **Fixed Post-Matriculation Horizon (`22`-Yr Master / `24`-Yr Bachelor) & Empirical No-College Counterfactual Baseline**:
  - Plotted on `year_since_matriculation` (`0..22` for Master [ages 22–44] and `0..24` for Bachelor [ages 18–42]), with shaded `Study Phase` (`1-Yr` / `3-Yr`) and hatched additional study year (`2nd Study Yr (2-Yr MS)` / `4th Study Yr (4-Yr BSc)`), so 1-year MSc (Imperial, NTU) and 3-year BEng (Imperial) naturally capture their 1-year labor-market head start (`21` career years vs. `20` career years).
  - **Study vs. Career Living Expenses**: Study years use campus student living budgets (`annual_living_cost_lcu`), whereas post-graduation career years use each country's **empirical age-graded (`20–45` yr) no-college net salary** (`nocollege_salary_20_24_lcu` .. `nocollege_salary_40_45_lcu`, from BLS/NCES, ONS ASHE/DfE LEO, BFS LSE, Destatis/BA, NBS/NBER, MOEL/KOSTAT, Singapore MOM CLFS) as the counterfactual baseline (where shared single-adult city living expenses cancel out identically between the graduate and non-college counterfactual).
  - **Foregone Earnings**: Incorporates country-specific **median 20-year-old net wages** (`youth_median_gross_salary_lcu`) during Bachelor study years and Bachelor Year-1 net salaries during Master study years.
  - The vertical axis plots the **Economic ROI Multiple (x)** of cumulative excess wealth (with 20-year Nominal USD excess wealth `+$X.XXM` / `+$XXXk` annotated on each curve and in the legend) divided by **Total Economic Investment** ($\text{Median Net Cost} + \text{Foregone Net Earnings}$):
    $$\text{ROI}_u(t) = \frac{\text{Cumulative Excess Wealth}_{u,\text{opp}}(t)}{\text{Median Net Degree Cost}_u + \text{Foregone Net Earnings}_u}$$
  - **Horizontal Reference Line**: $y = 0.0\text{x}$ marks the **Economic Break-Even Point** (where cumulative post-graduation excess earnings repay both out-of-pocket degree costs and foregone earnings).
  - **Disciplinary Uncertainty Bands**: The shaded region between Mechanical Engineering and CS/AI illustrates the career ROI dispersion across engineering tracks.
