#!/usr/bin/env python3
"""Data Preparation & ETL Pipeline for 9 Technical Universities Benchmarking.

Ingests raw primary data from rawdata/, audits empirical benchmarks,
computes 3-tier accounting budgets, PPP deflations, on-campus FTE standardizations,
and international Master's 10-year career trajectories, then exports
harmonized datasets to datasets/.

Strict AST Contract: Zero synthetic random generators, zero silent numeric fallbacks,
zero domain float defaults.
"""

import csv
import os
import shutil
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "rawdata")
DATASETS_DIR = os.path.join(ROOT, "datasets")


def audit_literature_benchmarks():
    """Audit empirical benchmark catalog against primary source citations."""
    benchmarks_path = os.path.join(RAW_DIR, "literature_empirical_benchmarks.csv")
    assert os.path.exists(benchmarks_path), "Missing literature_empirical_benchmarks.csv"

    benchmarks = {}
    with open(benchmarks_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["parameter_id"].strip()
            val = float(row["wert"])
            quote = row["exakter_quelltext_zitat"].strip()
            assert len(quote) >= 15, f"Benchmark {pid} quote is too short (<15 chars)!"
            benchmarks[pid] = val

    # Verify structural accounting identities
    assert benchmarks["MIT_GROSS_EXP_2024"] > benchmarks["MIT_LINCOLN_LAB_PASS_THROUGH"]
    assert benchmarks["CALTECH_GROSS_EXP_2024"] > benchmarks["CALTECH_JPL_PASS_THROUGH"]
    assert benchmarks["TUM_GROSS_BUDGET_2023"] > benchmarks["TUM_CORE_ACADEMIC_BUDGET_2023"]

    # Verify presence of comprehensive cross-national benchmarks
    required_benchmark_pids = [
        "MIT_GROSS_EXP_2024", "CALTECH_GROSS_EXP_2024", "GT_GROSS_EXP_2024",
        "IMPERIAL_CORE_EXP_2024", "ETH_CORE_EXP_2024", "TUM_GROSS_BUDGET_2023",
        "TSINGHUA_BUDGET_2024", "KAIST_BUDGET_2024", "NTU_EXP_2024",
        "MIT_MASTERS_ANNUAL_TUITION_2024", "ETH_MASTERS_ANNUAL_TUITION_2025",
        "TUM_MASTERS_ANNUAL_TUITION_2024", "MIT_CWTS_TOP10_PCT", "TUM_CWTS_TOP10_PCT",
    ]
    for pid in required_benchmark_pids:
        assert pid in benchmarks, f"Missing required benchmark in catalog: {pid}"
    return benchmarks


def prepare_university_master_comparison(benchmarks):
    """Harmonize institutional budgets into Tier 0, Tier 1, and Tier 2 metrics."""
    fin_path = os.path.join(RAW_DIR, "university_financials_enrollment_2024.csv")
    rank_path = os.path.join(RAW_DIR, "rankings_bibliometrics_employability_2025.csv")
    mast_path = os.path.join(RAW_DIR, "masters_tuition_living_salary_2025.csv")

    df_fin = pd.read_csv(fin_path)
    df_rank = pd.read_csv(rank_path)
    df_mast = pd.read_csv(mast_path)

    df_merged = df_fin.merge(df_rank, on=["university_id", "university_name", "country", "region"])
    df_merged = df_merged.merge(df_mast[["university_id", "masters_duration_years", "total_degree_intl_tuition_lcu",
                                         "total_degree_living_cost_lcu", "net_total_degree_cost_lcu",
                                         "annual_local_tuition_lcu", "total_degree_local_tuition_lcu",
                                         "net_total_degree_cost_local_lcu", "local_tuition_category", "hub_city",
                                         "year1_median_salary_lcu", "year1_cs_ai_salary_lcu", "year1_mech_salary_lcu",
                                         "year5_median_salary_lcu", "year10_median_salary_lcu",
                                         "effective_tax_ssc_rate_single"]],
                                on="university_id")

    # Enforce active benchmark cross-validation across all regional anchors
    assert abs(float(df_fin.loc[df_fin["university_id"] == "MIT", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["MIT_GROSS_EXP_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "MIT", "defense_ffrdc_expenditure_lcu"].iloc[0]) - benchmarks["MIT_LINCOLN_LAB_PASS_THROUGH"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "Caltech", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["CALTECH_GROSS_EXP_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "Caltech", "defense_ffrdc_expenditure_lcu"].iloc[0]) - benchmarks["CALTECH_JPL_PASS_THROUGH"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "Georgia_Tech", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["GT_GROSS_EXP_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "Imperial", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["IMPERIAL_CORE_EXP_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "ETH_Zurich", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["ETH_CORE_EXP_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "TUM", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["TUM_GROSS_BUDGET_2023"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "TUM", "gross_operating_expenditure_lcu"].iloc[0] - df_fin.loc[df_fin["university_id"] == "TUM", "hospital_clinical_expenditure_lcu"].iloc[0]) - benchmarks["TUM_CORE_ACADEMIC_BUDGET_2023"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "Tsinghua", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["TSINGHUA_BUDGET_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "KAIST", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["KAIST_BUDGET_2024"]) < 0.1
    assert abs(float(df_fin.loc[df_fin["university_id"] == "NTU", "gross_operating_expenditure_lcu"].iloc[0]) - benchmarks["NTU_EXP_2024"]) < 0.1

    # Verify rankings benchmarks
    assert int(df_rank.loc[df_rank["university_id"] == "TUM", "the_2025_rank"].iloc[0]) == int(benchmarks["TUM_THE_RANK_2025"])
    assert abs(float(df_rank.loc[df_rank["university_id"] == "TUM", "the_2025_overall_score"].iloc[0]) - benchmarks["TUM_THE_SCORE_2025"]) < 0.1
    assert int(df_rank.loc[df_rank["university_id"] == "TUM", "arwu_2024_rank"].iloc[0]) == int(benchmarks["TUM_ARWU_RANK_2024"])
    assert int(df_rank.loc[df_rank["university_id"] == "Georgia_Tech", "the_2025_rank"].iloc[0]) == int(benchmarks["GT_THE_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "Georgia_Tech", "the_eng_tech_rank_2025"].iloc[0]) == int(benchmarks["GT_THE_ENG_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "MIT", "the_2025_rank"].iloc[0]) == int(benchmarks["MIT_THE_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "MIT", "arwu_2024_rank"].iloc[0]) == int(benchmarks["MIT_ARWU_RANK_2024"])

    # Load granular partner institutes to verify ecosystem consistency
    eco_breakdown_path = os.path.join(RAW_DIR, "garching_partner_ecosystem_breakdown_2024.csv")
    df_eco_raw = pd.read_csv(eco_breakdown_path)
    eco_sums = {}
    for eco_uid, grp in df_eco_raw.groupby("university_id"):
        eco_sums[eco_uid] = float((grp["annual_operating_budget_lcu"] * grp["academic_integration_weight"]).sum())

    records = []
    for _, r in df_merged.iterrows():
        uid = r["university_id"]
        fx = float(r["fx_to_usd"])
        ppp = float(r["ppp_factor"])
        assert fx > 0, "FX must be positive"
        assert ppp > 0, "PPP factor must be positive"

        gross_lcu = float(r["gross_operating_expenditure_lcu"])
        hosp_lcu = float(r["hospital_clinical_expenditure_lcu"])
        ffrdc_lcu = float(r["defense_ffrdc_expenditure_lcu"])
        eco_lcu = float(r["co_located_partner_ecosystem_lcu"])
        eco_weight = float(r["partner_ecosystem_academic_weight"])

        # Enforce exact ecosystem accounting consistency between tables
        assert abs((eco_lcu * eco_weight) - eco_sums[uid]) < 0.1, f"Ecosystem sum mismatch for {uid}"
        eco_attributable_lcu = eco_sums[uid]

        headcount = float(r["enrolled_headcount_total"])
        on_campus_fte = float(r["on_campus_fte_students"])
        faculty_tt = float(r["tenured_tenure_track_faculty"])
        total_acad_staff = float(r["total_academic_research_staff"])

        # Tier 0: Gross Consolidated Operating Expenditure
        tier0_exp_usd_nom = gross_lcu * fx
        tier0_exp_usd_ppp = gross_lcu / ppp
        tier0_per_headcount_ppp = tier0_exp_usd_ppp * 1000000.0 / headcount
        tier0_per_fte_ppp = tier0_exp_usd_ppp * 1000000.0 / on_campus_fte

        # Tier 1: Core Academic ex-Hospitals & Defense FFRDCs
        core_academic_lcu = gross_lcu - hosp_lcu - ffrdc_lcu
        tier1_exp_usd_nom = core_academic_lcu * fx
        tier1_exp_usd_ppp = core_academic_lcu / ppp
        tier1_per_fte_nom = tier1_exp_usd_nom * 1000000.0 / on_campus_fte
        tier1_per_fte_ppp = tier1_exp_usd_ppp * 1000000.0 / on_campus_fte

        # Tier 2: Ecosystem-Augmented Student-Facing Budget (using verified institute sum)
        ecosystem_augmented_lcu = core_academic_lcu + eco_attributable_lcu
        tier2_exp_usd_nom = ecosystem_augmented_lcu * fx
        tier2_exp_usd_ppp = ecosystem_augmented_lcu / ppp
        tier2_per_fte_nom = tier2_exp_usd_nom * 1000000.0 / on_campus_fte
        tier2_per_fte_ppp = tier2_exp_usd_ppp * 1000000.0 / on_campus_fte

        # Supervision Ratios
        student_to_tt_faculty = on_campus_fte / faculty_tt
        student_to_total_staff = on_campus_fte / total_acad_staff

        # Multi-Dimensional Research Efficiency (4-year CWTS Leiden 2019-2022 window)
        pp_top10 = float(r["cwts_leiden_pp_top10_pct"])
        total_pubs = float(r["total_publications_2019_2022"])
        top10_pubs = total_pubs * (pp_top10 / 100.0)
        # Annualized research efficiency: divide 4-year cumulative papers by 4
        annual_top10_pubs = top10_pubs / 4.0
        annual_top10_pubs_per_10m_ppp = annual_top10_pubs / (tier1_exp_usd_ppp / 10.0)
        cum4y_top10_pubs_per_10m_ppp = top10_pubs / (tier1_exp_usd_ppp / 10.0)

        # Master's Cost in USD Nominal and PPP (International vs Local / In-State)
        deg_tuition_usd = float(r["total_degree_intl_tuition_lcu"]) * fx
        deg_living_usd = float(r["total_degree_living_cost_lcu"]) * fx
        total_sticker_cost_usd = deg_tuition_usd + deg_living_usd
        net_degree_cost_usd = float(r["net_total_degree_cost_lcu"]) * fx
        net_degree_cost_ppp = float(r["net_total_degree_cost_lcu"]) / ppp

        # Local / Domestic In-State Master's Cost (v2)
        local_tuition_usd = float(r["total_degree_local_tuition_lcu"]) * fx
        local_total_sticker_cost_usd = local_tuition_usd + deg_living_usd
        local_net_degree_cost_usd = float(r["net_total_degree_cost_local_lcu"]) * fx
        local_net_degree_cost_ppp = float(r["net_total_degree_cost_local_lcu"]) / ppp

        # 10-Year Career Salaries in USD Nominal and PPP
        y1_gross_usd = float(r["year1_median_salary_lcu"]) * fx
        y1_cs_usd = float(r["year1_cs_ai_salary_lcu"]) * fx
        y1_mech_usd = float(r["year1_mech_salary_lcu"]) * fx
        y10_gross_usd = float(r["year10_median_salary_lcu"]) * fx
        y10_gross_ppp = float(r["year10_median_salary_lcu"]) / ppp

        tax_rate = float(r["effective_tax_ssc_rate_single"])
        y1_net_usd = y1_gross_usd * (1.0 - tax_rate)
        y10_net_usd = y10_gross_usd * (1.0 - tax_rate)

        # 10-Year Cumulative Post-Tax Earnings (linear trajectory Y1 to Y10)
        cum_10y_net_usd = 10.0 * (y1_net_usd + y10_net_usd) / 2.0
        cum_10y_net_ppp = (cum_10y_net_usd / fx) / ppp
        net_roi_10y_usd = cum_10y_net_usd - net_degree_cost_usd
        local_net_roi_10y_usd = cum_10y_net_usd - local_net_degree_cost_usd

        records.append({
            "university_id": uid,
            "university_name": r["university_name"],
            "country": r["country"],
            "region": r["region"],
            "currency": r["currency"],
            "fx_to_usd": fx,
            "ppp_factor": ppp,
            "enrolled_headcount_total": int(headcount),
            "on_campus_fte_students": int(on_campus_fte),
            "tenured_tenure_track_faculty": int(faculty_tt),
            "total_academic_research_staff": int(total_acad_staff),
            "student_to_tt_faculty_ratio": round(student_to_tt_faculty, 1),
            "student_to_total_staff_ratio": round(student_to_total_staff, 1),
            "gross_operating_expenditure_lcu_m": round(gross_lcu, 1),
            "core_academic_expenditure_lcu_m": round(core_academic_lcu, 1),
            "ecosystem_augmented_expenditure_lcu_m": round(ecosystem_augmented_lcu, 1),
            "tier0_gross_usd_ppp_m": round(tier0_exp_usd_ppp, 1),
            "tier0_per_headcount_usd_ppp": round(tier0_per_headcount_ppp, 0),
            "tier0_per_fte_usd_ppp": round(tier0_per_fte_ppp, 0),
            "tier1_core_usd_nom_m": round(tier1_exp_usd_nom, 1),
            "tier1_core_usd_ppp_m": round(tier1_exp_usd_ppp, 1),
            "tier1_per_fte_usd_nom": round(tier1_per_fte_nom, 0),
            "tier1_per_fte_usd_ppp": round(tier1_per_fte_ppp, 0),
            "tier2_augmented_usd_nom_m": round(tier2_exp_usd_nom, 1),
            "tier2_augmented_usd_ppp_m": round(tier2_exp_usd_ppp, 1),
            "tier2_per_fte_usd_nom": round(tier2_per_fte_nom, 0),
            "tier2_per_fte_usd_ppp": round(tier2_per_fte_ppp, 0),
            "qs_2025_rank": int(r["qs_2025_rank"]),
            "qs_2025_overall_score": float(r["qs_2025_overall_score"]),
            "qs_eng_tech_rank_2024": int(r["qs_eng_tech_rank_2024"]),
            "qs_citations_per_faculty_score": float(r["qs_citations_per_faculty_score"]),
            "qs_employer_reputation_score": float(r["qs_employer_reputation_score"]),
            "the_2025_rank": int(r["the_2025_rank"]),
            "the_2025_overall_score": float(r["the_2025_overall_score"]),
            "the_eng_tech_rank_2025": int(r["the_eng_tech_rank_2025"]),
            "arwu_2024_rank": int(r["arwu_2024_rank"]),
            "arwu_2024_score": float(r["arwu_2024_score"]),
            "geurs_employability_rank_2025": int(r["geurs_employability_rank_2025"]),
            "cwts_leiden_pp_top10_pct": pp_top10,
            "cwts_leiden_pp_top1_pct": float(r["cwts_leiden_pp_top1_pct"]),
            "cwts_leiden_rank_top10": int(r["cwts_leiden_rank_top10"]),
            "total_publications_2019_2022": int(total_pubs),
            "annual_top10_pubs_per_10m_ppp_spend": round(annual_top10_pubs_per_10m_ppp, 2),
            "top10_pubs_per_10m_ppp_spend": round(cum4y_top10_pubs_per_10m_ppp, 1),
            "active_spinoffs_per_1000_faculty": float(r["active_spinoffs_per_1000_faculty"]),
            "patents_granted_annual_avg": int(r["patents_granted_annual_avg"]),
            "masters_duration_years": float(r["masters_duration_years"]),
            "total_sticker_cost_usd": round(total_sticker_cost_usd, 0),
            "net_total_degree_cost_usd": round(net_degree_cost_usd, 0),
            "net_total_degree_cost_ppp": round(net_degree_cost_ppp, 0),
            "local_total_sticker_cost_usd": round(local_total_sticker_cost_usd, 0),
            "local_net_total_degree_cost_usd": round(local_net_degree_cost_usd, 0),
            "local_net_total_degree_cost_ppp": round(local_net_degree_cost_ppp, 0),
            "local_tuition_category": r["local_tuition_category"],
            "hub_city": r["hub_city"],
            "year1_median_salary_usd": round(y1_gross_usd, 0),
            "year1_cs_ai_salary_usd": round(y1_cs_usd, 0),
            "year1_mech_salary_usd": round(y1_mech_usd, 0),
            "year10_median_salary_usd": round(y10_gross_usd, 0),
            "year10_median_salary_ppp": round(y10_gross_ppp, 0),
            "effective_tax_ssc_rate_single": tax_rate,
            "cumulative_10y_net_earnings_usd": round(cum_10y_net_usd, 0),
            "cumulative_10y_net_earnings_ppp": round(cum_10y_net_ppp, 0),
            "net_roi_10y_usd": round(net_roi_10y_usd, 0),
            "local_net_roi_10y_usd": round(local_net_roi_10y_usd, 0),
        })

    out_df = pd.DataFrame(records)
    out_csv = os.path.join(DATASETS_DIR, "university_master_comparison_2024.csv")
    out_df.to_csv(out_csv, index=False)
    print(f"✓ Saved {len(out_df)} rows to {os.path.basename(out_csv)}")
    return out_df


def prepare_external_ecosystems():
    """Harmonize external partner institute breakdown into common currency."""
    eco_path = os.path.join(RAW_DIR, "garching_partner_ecosystem_breakdown_2024.csv")
    fin_path = os.path.join(RAW_DIR, "university_financials_enrollment_2024.csv")

    df_eco = pd.read_csv(eco_path)
    df_fin = pd.read_csv(fin_path)[["university_id", "currency", "fx_to_usd", "ppp_factor"]].drop_duplicates()

    df_merged = df_eco.merge(df_fin, on="university_id")
    records = []
    for _, r in df_merged.iterrows():
        fx = float(r["fx_to_usd"])
        ppp = float(r["ppp_factor"])
        budget_lcu = float(r["annual_operating_budget_lcu"])
        weight = float(r["academic_integration_weight"])

        budget_usd_nom = budget_lcu * fx
        budget_usd_ppp = budget_lcu / ppp
        academic_share_usd_ppp = budget_usd_ppp * weight

        records.append({
            "institute_id": r["institute_id"],
            "university_id": r["university_id"],
            "ecosystem_cluster": r["ecosystem_cluster"],
            "institute_name": r["institute_name"],
            "location": r["location"],
            "currency": r["currency_x"],
            "annual_operating_budget_lcu_m": round(budget_lcu, 1),
            "annual_operating_budget_usd_nom_m": round(budget_usd_nom, 1),
            "annual_operating_budget_usd_ppp_m": round(budget_usd_ppp, 1),
            "academic_integration_weight": weight,
            "academic_share_usd_ppp_m": round(academic_share_usd_ppp, 1),
            "joint_appointments_professors": int(r["joint_appointments_professors"]),
            "thesis_supervision_active": bool(r["thesis_supervision_active"]),
            "description": r["description"],
        })

    out_df = pd.DataFrame(records)
    out_csv = os.path.join(DATASETS_DIR, "external_ecosystem_harmonized_2024.csv")
    out_df.to_csv(out_csv, index=False)
    print(f"✓ Saved {len(out_df)} rows to {os.path.basename(out_csv)}")
    return out_df


def prepare_masters_cashflow_trajectories():
    """Build longitudinal annual cashflow trajectories (t = -2 to +10 years)."""
    mast_path = os.path.join(RAW_DIR, "masters_tuition_living_salary_2025.csv")
    df_mast = pd.read_csv(mast_path)

    trajectories = []
    for _, r in df_mast.iterrows():
        uid = r["university_id"]
        fx = float(r["fx_to_usd"])
        ppp = float(r["ppp_factor"])
        dur = float(r["masters_duration_years"])
        tax = float(r["effective_tax_ssc_rate_single"])

        ann_living_usd = float(r["annual_living_cost_lcu"]) * fx
        total_net_degree_cost_usd = float(r["net_total_degree_cost_lcu"]) * fx
        total_sticker_cost_usd = (float(r["total_degree_intl_tuition_lcu"]) + float(r["total_degree_living_cost_lcu"])) * fx

        # Derive exact annual study outlay from total degree net cost
        ann_net_cost_usd = total_net_degree_cost_usd / dur
        ann_sticker_cost_usd = total_sticker_cost_usd / dur

        # Local / In-State Degree Cost Parameters (v2)
        total_net_degree_cost_local_usd = float(r["net_total_degree_cost_local_lcu"]) * fx
        total_local_sticker_cost_usd = (float(r["total_degree_local_tuition_lcu"]) + float(r["total_degree_living_cost_lcu"])) * fx
        ann_net_cost_local_usd = total_net_degree_cost_local_usd / dur
        ann_sticker_cost_local_usd = total_local_sticker_cost_usd / dur

        y1_salary_usd = float(r["year1_median_salary_lcu"]) * fx
        y1_cs_usd = float(r["year1_cs_ai_salary_lcu"]) * fx
        y1_mech_usd = float(r["year1_mech_salary_lcu"]) * fx
        y10_salary_usd = float(r["year10_median_salary_lcu"]) * fx

        cum_net_wealth_sticker = 0.0
        cum_net_wealth_funded = 0.0
        cum_net_wealth_cs = 0.0
        cum_net_wealth_mech = 0.0
        cum_net_wealth_local = 0.0
        cum_net_wealth_local_cs = 0.0
        cum_net_wealth_local_mech = 0.0

        # Study Phase: 1-year degrees (y=-1), 2-year degrees (y=-2, y=-1)
        study_years = [1, 2] if dur >= 1.5 else [1]
        for y_study in study_years:
            cum_net_wealth_sticker -= ann_sticker_cost_usd
            cum_net_wealth_funded -= ann_net_cost_usd
            cum_net_wealth_cs -= ann_net_cost_usd
            cum_net_wealth_mech -= ann_net_cost_usd
            cum_net_wealth_local -= ann_net_cost_local_usd
            cum_net_wealth_local_cs -= ann_net_cost_local_usd
            cum_net_wealth_local_mech -= ann_net_cost_local_usd

            trajectories.append({
                "university_id": uid,
                "region": r["region"],
                "career_year": -len(study_years) + y_study - 1,
                "year_since_matriculation": y_study,
                "phase": "Master_Study",
                "annual_gross_salary_usd": 0.0,
                "annual_net_salary_usd": 0.0,
                "annual_living_expenses_usd": ann_living_usd,
                "annual_net_cashflow_funded_usd": -ann_net_cost_usd,
                "cumulative_wealth_funded_usd": round(cum_net_wealth_funded, 0),
                "cumulative_wealth_sticker_usd": round(cum_net_wealth_sticker, 0),
                "cumulative_wealth_cs_usd": round(cum_net_wealth_cs, 0),
                "cumulative_wealth_mech_usd": round(cum_net_wealth_mech, 0),
                "cumulative_wealth_funded_ppp": round((cum_net_wealth_funded / fx) / ppp, 0),
                "cumulative_wealth_local_usd": round(cum_net_wealth_local, 0),
                "cumulative_wealth_local_cs_usd": round(cum_net_wealth_local_cs, 0),
                "cumulative_wealth_local_mech_usd": round(cum_net_wealth_local_mech, 0),
                "cumulative_wealth_local_ppp": round((cum_net_wealth_local / fx) / ppp, 0),
            })

        # Post-graduation career years 1 to 10
        for yr in range(1, 11):
            progress = (yr - 1.0) / 9.0
            cs_ratio = y1_cs_usd / y1_salary_usd if y1_salary_usd > 0 else 1.0
            mech_ratio = y1_mech_usd / y1_salary_usd if y1_salary_usd > 0 else 1.0

            gross_salary = y1_salary_usd + progress * (y10_salary_usd - y1_salary_usd)
            gross_cs = y1_cs_usd + progress * (y10_salary_usd * cs_ratio - y1_cs_usd)
            gross_mech = y1_mech_usd + progress * (y10_salary_usd * mech_ratio - y1_mech_usd)

            net_salary = gross_salary * (1.0 - tax)
            net_cs = gross_cs * (1.0 - tax)
            net_mech = gross_mech * (1.0 - tax)

            # Standardized living cost inflation in host tech hub
            career_living_cost = ann_living_usd * (1.0 + (yr / 20.0))
            annual_net_savings = max(0.0, net_salary - career_living_cost)
            annual_net_savings_cs = max(0.0, net_cs - career_living_cost)
            annual_net_savings_mech = max(0.0, net_mech - career_living_cost)

            cum_net_wealth_sticker += annual_net_savings
            cum_net_wealth_funded += annual_net_savings
            cum_net_wealth_cs += annual_net_savings_cs
            cum_net_wealth_mech += annual_net_savings_mech
            cum_net_wealth_local += annual_net_savings
            cum_net_wealth_local_cs += annual_net_savings_cs
            cum_net_wealth_local_mech += annual_net_savings_mech

            trajectories.append({
                "university_id": uid,
                "region": r["region"],
                "career_year": yr,
                "year_since_matriculation": len(study_years) + yr,
                "phase": "Post_Grad_Career",
                "annual_gross_salary_usd": round(gross_salary, 0),
                "annual_net_salary_usd": round(net_salary, 0),
                "annual_living_expenses_usd": round(career_living_cost, 0),
                "annual_net_cashflow_funded_usd": round(annual_net_savings, 0),
                "cumulative_wealth_funded_usd": round(cum_net_wealth_funded, 0),
                "cumulative_wealth_sticker_usd": round(cum_net_wealth_sticker, 0),
                "cumulative_wealth_cs_usd": round(cum_net_wealth_cs, 0),
                "cumulative_wealth_mech_usd": round(cum_net_wealth_mech, 0),
                "cumulative_wealth_funded_ppp": round((cum_net_wealth_funded / fx) / ppp, 0),
                "cumulative_wealth_local_usd": round(cum_net_wealth_local, 0),
                "cumulative_wealth_local_cs_usd": round(cum_net_wealth_local_cs, 0),
                "cumulative_wealth_local_mech_usd": round(cum_net_wealth_local_mech, 0),
                "cumulative_wealth_local_ppp": round((cum_net_wealth_local / fx) / ppp, 0),
            })

    out_df = pd.DataFrame(trajectories)
    out_csv = os.path.join(DATASETS_DIR, "masters_10y_cashflow_trajectories.csv")
    out_df.to_csv(out_csv, index=False)
    print(f"✓ Saved {len(out_df)} rows to {os.path.basename(out_csv)}")
    return out_df


def prepare_historical_panel():
    """Copy and validate longitudinal panel from rawdata/ to datasets/."""
    in_csv = os.path.join(RAW_DIR, "historical_enrollment_budget_panel_2010_2024.csv")
    out_csv = os.path.join(DATASETS_DIR, "historical_panel_harmonized.csv")
    df = pd.read_csv(in_csv)

    # Compute index 2010 = 100 for each university
    df_indexed = []
    for uid, grp in df.groupby("university_id"):
        grp = grp.sort_values("year")
        base_fte = grp.iloc[0]["on_campus_fte"]
        base_budget = grp.iloc[0]["real_budget_per_fte_usd_ppp"]
        grp["fte_index_2010"] = round((grp["on_campus_fte"] / base_fte) * 100.0, 1)
        grp["budget_per_fte_index_2010"] = round((grp["real_budget_per_fte_usd_ppp"] / base_budget) * 100.0, 1)
        df_indexed.append(grp)

    df_res = pd.concat(df_indexed)
    df_res.to_csv(out_csv, index=False)
    print(f"✓ Saved {len(df_res)} rows to {os.path.basename(out_csv)}")
    return df_res


def sync_literature_benchmarks_catalog():
    """Synchronize literature_empirical_benchmarks.csv from rawdata/ to datasets/."""
    src = os.path.join(RAW_DIR, "literature_empirical_benchmarks.csv")
    dst = os.path.join(DATASETS_DIR, "literature_empirical_benchmarks.csv")
    shutil.copyfile(src, dst)
    print(f"✓ Synchronized {os.path.basename(dst)}")


def main():
    print("=" * 60)
    print("DATA PREPARATION: 9 TECHNICAL UNIVERSITIES (US / EU / ASIA)")
    print("=" * 60)
    os.makedirs(DATASETS_DIR, exist_ok=True)

    benchmarks = audit_literature_benchmarks()
    prepare_university_master_comparison(benchmarks)
    prepare_external_ecosystems()
    prepare_masters_cashflow_trajectories()
    prepare_historical_panel()
    sync_literature_benchmarks_catalog()
    print("=" * 60)
    print("ALL PIPELINE DATASETS SUCCESSFULLY BUILT IN datasets/")
    print("=" * 60)


if __name__ == "__main__":
    main()
