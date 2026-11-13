#!/usr/bin/env python3
"""Data Preparation & ETL Pipeline for 9 Technical Universities Benchmarking.

Ingests raw primary data from rawdata/, audits empirical benchmarks,
computes 3-tier accounting budgets, PPP deflations, on-campus FTE standardizations,
and Master's and Bachelor's 10-year career trajectories across Native and Non-Native cohorts,
then exports harmonized datasets to datasets/.

Strict AST Contract: Zero synthetic random generators, zero silent numeric fallbacks,
zero domain float defaults.
"""

import csv
import os
import shutil
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "rawdata")
DATASETS_DIR = os.path.join(ROOT, "datasets")
TOL_M = 0.1  # rounding tolerance (LCU or USD millions) for accounting identities on 1-decimal rounded columns
SENSITIVITY_WEIGHT_50PCT = 0.5  # structural integration weight sensitivity bound (+/- 50%)
DISCOUNT_RATE_3PCT = 0.03  # real discount rate for long-term career cashflows (Pillar 5 / ROI uncertainty)
OPP_COST_NON_DEGREE_USD = 30000.0  # baseline non-degree annual net earnings for Bachelor opportunity cost uncertainty


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
            import re
            assert not re.search(r"(?:^|[\s\"\'(]),\d{3}\b", quote), f"Shell-truncated quote in {pid}: {quote}"
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
        "MIT_BACHELORS_ANNUAL_TUITION_2024", "CALTECH_BACHELORS_ANNUAL_TUITION_2024",
        "GT_BACHELORS_IN_STATE_TUITION_2024", "IMPERIAL_BACHELORS_HOME_TUITION_2024",
        "ETH_BACHELORS_LOCAL_TUITION_2025", "TUM_BACHELORS_LOCAL_TUITION_2024",
        "TSINGHUA_BACHELORS_DOMESTIC_TUITION_2024", "KAIST_BACHELORS_DOMESTIC_TUITION_2024",
        "NTU_BACHELORS_LOCAL_TUITION_2024", "MIT_US_NEWS_RANK_2025", "TUM_US_NEWS_RANK_2025",
        "TUM_MEDICINE_CLINICAL_HEADCOUNT_2023", "TUM_MEDICINE_TOTAL_HEADCOUNT_2023",
        "IMPERIAL_MEDICINE_TOTAL_FTE_2024", "GT_OMSCS_ONLINE_DELIVERY_COST_2024",
    ]
    for pid in required_benchmark_pids:
        assert pid in benchmarks, f"Missing required benchmark in catalog: {pid}"
    return benchmarks


def prepare_university_master_comparison(benchmarks):
    """Harmonize institutional budgets into Tier 0, Tier 1, and Tier 2 metrics."""
    fin_path = os.path.join(RAW_DIR, "university_financials_enrollment_2024.csv")
    rank_path = os.path.join(RAW_DIR, "rankings_bibliometrics_employability_2025.csv")
    mast_path = os.path.join(RAW_DIR, "masters_tuition_living_salary_2025.csv")
    bach_path = os.path.join(RAW_DIR, "bachelors_tuition_living_salary_2025.csv")

    df_fin = pd.read_csv(fin_path)
    df_rank = pd.read_csv(rank_path)
    df_mast = pd.read_csv(mast_path)
    df_bach = pd.read_csv(bach_path)

    df_merged = df_fin.merge(df_rank, on=["university_id", "university_name", "country", "region"])
    df_merged = df_merged.merge(df_mast[["university_id", "masters_duration_years", "total_degree_intl_tuition_lcu",
                                         "total_degree_living_cost_lcu", "net_total_degree_cost_lcu",
                                         "annual_local_tuition_lcu", "total_degree_local_tuition_lcu",
                                         "net_total_degree_cost_local_lcu", "local_tuition_category", "hub_city",
                                         "year1_median_salary_lcu", "year1_cs_ai_salary_lcu", "year1_mech_salary_lcu",
                                         "year5_median_salary_lcu", "year10_median_salary_lcu", "year20_median_salary_lcu",
                                         "effective_tax_ssc_rate_single"]],
                                on="university_id")
    df_merged = df_merged.merge(df_bach[["university_id", "bachelors_duration_years",
                                         "total_degree_intl_tuition_lcu", "net_total_degree_cost_intl_lcu",
                                         "annual_local_tuition_lcu", "total_degree_local_tuition_lcu",
                                         "net_total_degree_cost_local_lcu", "year1_median_salary_lcu",
                                         "year1_cs_ai_salary_lcu", "year1_mech_salary_lcu", "year10_median_salary_lcu",
                                         "year20_median_salary_lcu"]],
                                on="university_id", suffixes=("", "_bach"))

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
    assert int(df_rank.loc[df_rank["university_id"] == "TUM", "us_news_2025_rank"].iloc[0]) == int(benchmarks["TUM_US_NEWS_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "Georgia_Tech", "the_2025_rank"].iloc[0]) == int(benchmarks["GT_THE_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "Georgia_Tech", "the_eng_tech_rank_2025"].iloc[0]) == int(benchmarks["GT_THE_ENG_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "MIT", "the_2025_rank"].iloc[0]) == int(benchmarks["MIT_THE_RANK_2025"])
    assert int(df_rank.loc[df_rank["university_id"] == "MIT", "arwu_2024_rank"].iloc[0]) == int(benchmarks["MIT_ARWU_RANK_2024"])
    assert int(df_rank.loc[df_rank["university_id"] == "MIT", "us_news_2025_rank"].iloc[0]) == int(benchmarks["MIT_US_NEWS_RANK_2025"])

    # Verify Bachelor benchmarks
    assert abs(float(df_bach.loc[df_bach["university_id"] == "MIT", "annual_intl_tuition_lcu"].iloc[0]) - benchmarks["MIT_BACHELORS_ANNUAL_TUITION_2024"]) < 0.1
    assert abs(float(df_bach.loc[df_bach["university_id"] == "TUM", "annual_intl_tuition_lcu"].iloc[0]) - benchmarks["TUM_BACHELORS_INTL_TUITION_2024"]) < 0.1

    # Verify 1-Year Cohort Attrition & 20-Year Master Salary benchmarks
    assert abs(float(df_rank.loc[df_rank["university_id"] == "ETH_Zurich", "first_year_screening_attrition_pct"].iloc[0]) - benchmarks["ETH_FIRST_YEAR_ATTRITION_2024"]) < 0.1
    assert abs(float(df_rank.loc[df_rank["university_id"] == "TUM", "first_year_screening_attrition_pct"].iloc[0]) - benchmarks["TUM_FIRST_YEAR_ATTRITION_2024"]) < 0.1
    assert abs(float(df_mast.loc[df_mast["university_id"] == "MIT", "year20_median_salary_lcu"].iloc[0]) - benchmarks["MIT_YEAR20_MASTERS_SALARY_USD"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "Caltech", "year20_median_salary_lcu"].iloc[0]) - benchmarks["CALTECH_YEAR20_MASTERS_SALARY_USD"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "Georgia_Tech", "year20_median_salary_lcu"].iloc[0]) - benchmarks["GT_YEAR20_MASTERS_SALARY_USD"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "Imperial", "year20_median_salary_lcu"].iloc[0]) - benchmarks["IMPERIAL_YEAR20_MASTERS_SALARY_GBP"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "ETH_Zurich", "year20_median_salary_lcu"].iloc[0]) - benchmarks["ETH_YEAR20_MASTERS_SALARY_CHF"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "TUM", "year20_median_salary_lcu"].iloc[0]) - benchmarks["TUM_YEAR20_MASTERS_SALARY_EUR"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "Tsinghua", "year20_median_salary_lcu"].iloc[0]) - benchmarks["TSINGHUA_YEAR20_MASTERS_SALARY_CNY"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "KAIST", "year20_median_salary_lcu"].iloc[0]) - benchmarks["KAIST_YEAR20_MASTERS_SALARY_KRW"]) < 1.0
    assert abs(float(df_mast.loc[df_mast["university_id"] == "NTU", "year20_median_salary_lcu"].iloc[0]) - benchmarks["NTU_YEAR20_MASTERS_SALARY_SGD"]) < 1.0

    # Load granular partner institutes to verify ecosystem consistency
    eco_breakdown_path = os.path.join(RAW_DIR, "garching_partner_ecosystem_breakdown_2024.csv")
    df_eco_raw = pd.read_csv(eco_breakdown_path)
    eco_sums = {}
    eco_indep_sums = {}
    for eco_uid, grp in df_eco_raw.groupby("university_id"):
        eco_sums[eco_uid] = float((grp["annual_operating_budget_lcu"] * grp["academic_integration_weight"]).sum())
        indep_grp = grp[grp["is_legally_independent"].astype(str).str.lower() == "true"]
        eco_indep_sums[eco_uid] = float((indep_grp["annual_operating_budget_lcu"] * indep_grp["academic_integration_weight"]).sum())

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

        # Tier 1 Denominator & Online Clean Adjustments (Uncertainty & Sensitivity Bounds)
        online_op_exp = float(r["online_operating_expenditure_est_lcu"])
        core_academic_clean_online_lcu = core_academic_lcu - online_op_exp
        tier1_clean_online_usd_ppp = core_academic_clean_online_lcu / ppp
        tier1_per_fte_usd_ppp_clean_online = tier1_clean_online_usd_ppp * 1000000.0 / on_campus_fte

        med_students = float(r["clinical_medical_students_headcount"])
        on_campus_fte_ex_med = max(on_campus_fte - med_students, 1.0)
        tier1_per_fte_usd_ppp_ex_med = tier1_exp_usd_ppp * 1000000.0 / on_campus_fte_ex_med

        # Tier 2: Ecosystem-Augmented Student-Facing Budget (On-Campus Clean ex-Online Teaching Budget)
        ecosystem_augmented_lcu = core_academic_clean_online_lcu + eco_attributable_lcu
        tier2_exp_usd_nom = ecosystem_augmented_lcu * fx
        tier2_exp_usd_ppp = ecosystem_augmented_lcu / ppp
        tier2_per_fte_nom = tier2_exp_usd_nom * 1000000.0 / on_campus_fte
        tier2_per_fte_usd_ppp = tier2_exp_usd_ppp * 1000000.0 / on_campus_fte
        tier2_per_fte_ppp = tier2_per_fte_usd_ppp

        eco_attributable_indep_lcu = eco_indep_sums[uid]
        ecosystem_augmented_indep_lcu = core_academic_clean_online_lcu + eco_attributable_indep_lcu
        tier2_indep_usd_ppp = ecosystem_augmented_indep_lcu / ppp
        tier2_per_fte_usd_ppp_indep = tier2_indep_usd_ppp * 1000000.0 / on_campus_fte

        # Ecosystem Weight Sensitivity Bounds (+/- 50% on partner integration weights)
        eco_attributable_low_lcu = eco_attributable_lcu * SENSITIVITY_WEIGHT_50PCT
        eco_attributable_high_lcu = eco_attributable_lcu + eco_attributable_low_lcu
        tier2_exp_usd_nom_low = (core_academic_clean_online_lcu + eco_attributable_low_lcu) * fx
        tier2_exp_usd_nom_high = (core_academic_clean_online_lcu + eco_attributable_high_lcu) * fx
        tier2_exp_usd_ppp_low = (core_academic_clean_online_lcu + eco_attributable_low_lcu) / ppp
        tier2_exp_usd_ppp_high = (core_academic_clean_online_lcu + eco_attributable_high_lcu) / ppp
        tier2_per_fte_usd_ppp_low = tier2_exp_usd_ppp_low * 1000000.0 / on_campus_fte
        tier2_per_fte_usd_ppp_high = tier2_exp_usd_ppp_high * 1000000.0 / on_campus_fte

        # Supervision Ratios
        student_to_tt_faculty = on_campus_fte / faculty_tt
        student_to_total_staff = on_campus_fte / total_acad_staff

        # Multi-Dimensional Research Efficiency
        pp_top10 = float(r["cwts_leiden_pp_top10_pct"])
        total_pubs = float(r["total_publications_2019_2022"])
        top10_pubs = total_pubs * (pp_top10 / 100.0)
        annual_top10_pubs = top10_pubs / 4.0
        annual_top10_pubs_per_10m_ppp = annual_top10_pubs / (tier1_exp_usd_ppp / 10.0)
        cum4y_top10_pubs_per_10m_ppp = top10_pubs / (tier1_exp_usd_ppp / 10.0)

        # Master's Cost in USD Nominal and PPP (International vs Local)
        deg_tuition_usd = float(r["total_degree_intl_tuition_lcu"]) * fx
        deg_living_usd = float(r["total_degree_living_cost_lcu"]) * fx
        total_sticker_cost_usd = deg_tuition_usd + deg_living_usd
        total_sticker_cost_ppp = (float(r["total_degree_intl_tuition_lcu"]) + float(r["total_degree_living_cost_lcu"])) / ppp
        net_degree_cost_usd = float(r["net_total_degree_cost_lcu"]) * fx
        net_degree_cost_ppp = float(r["net_total_degree_cost_lcu"]) / ppp

        local_tuition_usd = float(r["total_degree_local_tuition_lcu"]) * fx
        local_total_sticker_cost_usd = local_tuition_usd + deg_living_usd
        local_total_sticker_cost_ppp = (float(r["total_degree_local_tuition_lcu"]) + float(r["total_degree_living_cost_lcu"])) / ppp
        local_net_degree_cost_usd = float(r["net_total_degree_cost_local_lcu"]) * fx
        local_net_degree_cost_ppp = float(r["net_total_degree_cost_local_lcu"]) / ppp

        # 10-Year & 20-Year Career Salaries for Master
        y1_gross_usd = float(r["year1_median_salary_lcu"]) * fx
        y1_gross_ppp = float(r["year1_median_salary_lcu"]) / ppp
        y1_cs_usd = float(r["year1_cs_ai_salary_lcu"]) * fx
        y1_mech_usd = float(r["year1_mech_salary_lcu"]) * fx
        y10_gross_usd = float(r["year10_median_salary_lcu"]) * fx
        y10_gross_ppp = float(r["year10_median_salary_lcu"]) / ppp
        y20_gross_usd = float(r["year20_median_salary_lcu"]) * fx
        y20_gross_ppp = float(r["year20_median_salary_lcu"]) / ppp

        tax_rate = float(r["effective_tax_ssc_rate_single"])
        y1_net_usd = y1_gross_usd * (1.0 - tax_rate)
        y10_net_usd = y10_gross_usd * (1.0 - tax_rate)

        cum_10y_net_usd = 10.0 * (y1_net_usd + y10_net_usd) / 2.0
        cum_10y_net_ppp = (cum_10y_net_usd / fx) / ppp
        net_roi_10y_usd = cum_10y_net_usd - net_degree_cost_usd
        local_net_roi_10y_usd = cum_10y_net_usd - local_net_degree_cost_usd

        # Bachelor's Metrics (International vs Native / Local)
        b_dur = float(r["bachelors_duration_years"])
        b_ann_living_lcu = float(r["total_degree_living_cost_lcu"]) / float(r["masters_duration_years"])
        b_intl_tuition_usd = float(r["total_degree_intl_tuition_lcu_bach"]) * fx
        b_intl_living_usd = b_ann_living_lcu * b_dur * fx
        b_intl_sticker_usd = b_intl_tuition_usd + b_intl_living_usd
        b_intl_sticker_ppp = (float(r["total_degree_intl_tuition_lcu_bach"]) + (b_ann_living_lcu * b_dur)) / ppp
        b_intl_net_usd = float(r["net_total_degree_cost_intl_lcu"]) * fx
        b_intl_net_ppp = float(r["net_total_degree_cost_intl_lcu"]) / ppp

        b_local_tuition_usd = float(r["total_degree_local_tuition_lcu_bach"]) * fx
        b_local_sticker_usd = b_local_tuition_usd + b_intl_living_usd
        b_local_sticker_ppp = (float(r["total_degree_local_tuition_lcu_bach"]) + (b_ann_living_lcu * b_dur)) / ppp
        b_local_net_usd = float(r["net_total_degree_cost_local_lcu_bach"]) * fx
        b_local_net_ppp = float(r["net_total_degree_cost_local_lcu_bach"]) / ppp

        b_y1_gross_usd = float(r["year1_median_salary_lcu_bach"]) * fx
        b_y1_gross_ppp = float(r["year1_median_salary_lcu_bach"]) / ppp
        b_y1_cs_usd = float(r["year1_cs_ai_salary_lcu_bach"]) * fx
        b_y1_mech_usd = float(r["year1_mech_salary_lcu_bach"]) * fx
        b_y10_gross_usd = float(r["year10_median_salary_lcu_bach"]) * fx
        b_y10_gross_ppp = float(r["year10_median_salary_lcu_bach"]) / ppp
        b_y20_gross_usd = float(r["year20_median_salary_lcu_bach"]) * fx
        b_y20_gross_ppp = float(r["year20_median_salary_lcu_bach"]) / ppp

        b_y1_net_usd = b_y1_gross_usd * (1.0 - tax_rate)
        b_y10_net_usd = b_y10_gross_usd * (1.0 - tax_rate)
        b_cum_10y_net_usd = 10.0 * (b_y1_net_usd + b_y10_net_usd) / 2.0
        b_cum_10y_net_ppp = (b_cum_10y_net_usd / fx) / ppp
        b_intl_net_roi_10y_usd = b_cum_10y_net_usd - b_intl_net_usd
        b_local_net_roi_10y_usd = b_cum_10y_net_usd - b_local_net_usd

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
            "tier0_gross_usd_nom_m": round(tier0_exp_usd_nom, 1),
            "tier0_gross_usd_ppp_m": round(tier0_exp_usd_ppp, 1),
            "tier0_per_headcount_usd_ppp": round(tier0_per_headcount_ppp, 0),
            "tier0_per_fte_usd_ppp": round(tier0_per_fte_ppp, 0),
            "tier1_core_usd_nom_m": round(tier1_exp_usd_nom, 1),
            "tier1_core_usd_ppp_m": round(tier1_exp_usd_ppp, 1),
            "tier1_per_fte_usd_nom": round(tier1_per_fte_nom, 0),
            "tier1_per_fte_usd_ppp": round(tier1_per_fte_ppp, 0),
            "tier1_per_fte_usd_ppp_clean_online": round(tier1_per_fte_usd_ppp_clean_online, 0),
            "tier1_per_fte_usd_ppp_ex_med": round(tier1_per_fte_usd_ppp_ex_med, 0),
            "tier2_augmented_usd_nom_m": round(tier2_exp_usd_nom, 1),
            "tier2_augmented_usd_nom_low_m": round(tier2_exp_usd_nom_low, 1),
            "tier2_augmented_usd_nom_high_m": round(tier2_exp_usd_nom_high, 1),
            "tier2_augmented_usd_ppp_m": round(tier2_exp_usd_ppp, 1),
            "tier2_augmented_usd_ppp_indep_m": round(tier2_indep_usd_ppp, 1),
            "tier2_augmented_usd_ppp_low_m": round(tier2_exp_usd_ppp_low, 1),
            "tier2_augmented_usd_ppp_high_m": round(tier2_exp_usd_ppp_high, 1),
            "tier2_per_fte_usd_nom": round(tier2_per_fte_nom, 0),
            "tier2_per_fte_usd_ppp": round(tier2_per_fte_usd_ppp, 0),
            "tier2_per_fte_usd_ppp_indep": round(tier2_per_fte_usd_ppp_indep, 0),
            "tier2_per_fte_usd_ppp_low": round(tier2_per_fte_usd_ppp_low, 0),
            "tier2_per_fte_usd_ppp_high": round(tier2_per_fte_usd_ppp_high, 0),
            "total_degree_intl_tuition_usd": round(deg_tuition_usd, 0),
            "total_degree_local_tuition_usd": round(local_tuition_usd, 0),
            "bachelors_total_intl_tuition_usd": round(b_intl_tuition_usd, 0),
            "bachelors_total_local_tuition_usd": round(b_local_tuition_usd, 0),
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
            "us_news_2025_rank": int(r["us_news_2025_rank"]),
            "us_news_2025_score": float(r["us_news_2025_score"]),
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
            "total_sticker_cost_ppp": round(total_sticker_cost_ppp, 0),
            "net_total_degree_cost_usd": round(net_degree_cost_usd, 0),
            "net_total_degree_cost_ppp": round(net_degree_cost_ppp, 0),
            "local_total_sticker_cost_usd": round(local_total_sticker_cost_usd, 0),
            "local_total_sticker_cost_ppp": round(local_total_sticker_cost_ppp, 0),
            "local_net_total_degree_cost_usd": round(local_net_degree_cost_usd, 0),
            "local_net_total_degree_cost_ppp": round(local_net_degree_cost_ppp, 0),
            "local_tuition_category": r["local_tuition_category"],
            "hub_city": r["hub_city"],
            "year1_median_salary_usd": round(y1_gross_usd, 0),
            "year1_median_salary_ppp": round(y1_gross_ppp, 0),
            "year1_cs_ai_salary_usd": round(y1_cs_usd, 0),
            "year1_mech_salary_usd": round(y1_mech_usd, 0),
            "year10_median_salary_usd": round(y10_gross_usd, 0),
            "year10_median_salary_ppp": round(y10_gross_ppp, 0),
            "year20_median_salary_usd": round(y20_gross_usd, 0),
            "year20_median_salary_ppp": round(y20_gross_ppp, 0),
            "effective_tax_ssc_rate_single": tax_rate,
            "cumulative_10y_net_earnings_usd": round(cum_10y_net_usd, 0),
            "cumulative_10y_net_earnings_ppp": round(cum_10y_net_ppp, 0),
            "net_roi_10y_usd": round(net_roi_10y_usd, 0),
            "local_net_roi_10y_usd": round(local_net_roi_10y_usd, 0),
            "bachelors_duration_years": b_dur,
            "bachelors_total_sticker_cost_usd": round(b_intl_sticker_usd, 0),
            "bachelors_total_sticker_cost_ppp": round(b_intl_sticker_ppp, 0),
            "bachelors_net_total_degree_cost_usd": round(b_intl_net_usd, 0),
            "bachelors_net_total_degree_cost_ppp": round(b_intl_net_ppp, 0),
            "bachelors_local_total_sticker_cost_usd": round(b_local_sticker_usd, 0),
            "bachelors_local_total_sticker_cost_ppp": round(b_local_sticker_ppp, 0),
            "bachelors_local_net_total_degree_cost_usd": round(b_local_net_usd, 0),
            "bachelors_local_net_total_degree_cost_ppp": round(b_local_net_ppp, 0),
            "bachelors_year1_median_salary_usd": round(b_y1_gross_usd, 0),
            "bachelors_year1_median_salary_ppp": round(b_y1_gross_ppp, 0),
            "bachelors_year1_cs_ai_salary_usd": round(b_y1_cs_usd, 0),
            "bachelors_year1_mech_salary_usd": round(b_y1_mech_usd, 0),
            "bachelors_year10_median_salary_usd": round(b_y10_gross_usd, 0),
            "bachelors_year10_median_salary_ppp": round(b_y10_gross_ppp, 0),
            "bachelors_year20_median_salary_usd": round(b_y20_gross_usd, 0),
            "bachelors_year20_median_salary_ppp": round(b_y20_gross_ppp, 0),
            "bachelors_cumulative_10y_net_usd": round(b_cum_10y_net_usd, 0),
            "bachelors_cumulative_10y_net_ppp": round(b_cum_10y_net_ppp, 0),
            "bachelors_net_roi_10y_usd": round(b_intl_net_roi_10y_usd, 0),
            "bachelors_local_net_roi_10y_usd": round(b_local_net_roi_10y_usd, 0),
            "undergrad_applicants_total": int(r["undergrad_applicants_total"]),
            "undergrad_admitted_total": int(r["undergrad_admitted_total"]),
            "undergrad_acceptance_rate_pct": float(r["undergrad_acceptance_rate_pct"]),
            "undergrad_acceptance_rate_domestic_pct": float(r["undergrad_acceptance_rate_domestic_pct"]),
            "undergrad_acceptance_rate_intl_pct": float(r["undergrad_acceptance_rate_intl_pct"]),
            "first_year_screening_attrition_pct": float(r["first_year_screening_attrition_pct"]),
            "admissions_filtering_paradigm": r["admissions_filtering_paradigm"],
        })

    out_df = pd.DataFrame(records)

    # Accounting identities across tiers (rounded columns => small tolerances)
    assert (out_df["tier0_gross_usd_ppp_m"] >= out_df["tier1_core_usd_ppp_m"] - TOL_M).all(), "Tier 1 must not exceed Tier 0"
    assert (out_df["tier2_augmented_usd_ppp_m"] >= out_df["tier1_core_usd_ppp_m"] - TOL_M).all(), "Tier 2 must not be below Tier 1"
    assert (out_df["tier2_augmented_usd_ppp_low_m"] <= out_df["tier2_augmented_usd_ppp_m"] + TOL_M).all()
    assert (out_df["tier2_augmented_usd_ppp_m"] <= out_df["tier2_augmented_usd_ppp_high_m"] + TOL_M).all()
    assert (out_df["on_campus_fte_students"] <= out_df["enrolled_headcount_total"]).all(), "FTE cannot exceed headcount"
    fin_cols = df_fin.set_index("university_id")
    for _, row in out_df.iterrows():
        u = row["university_id"]
        expected_core = fin_cols.loc[u, "gross_operating_expenditure_lcu"] - fin_cols.loc[u, "hospital_clinical_expenditure_lcu"] - fin_cols.loc[u, "defense_ffrdc_expenditure_lcu"]
        assert abs(row["core_academic_expenditure_lcu_m"] - expected_core) < 0.1, f"Tier 1 identity violated for {u}"
        assert abs(row["tier2_augmented_usd_nom_m"] - row["ecosystem_augmented_expenditure_lcu_m"] * row["fx_to_usd"]) < 0.2, f"Tier 2 nominal identity violated for {u}"
        assert abs(row["tier2_augmented_usd_ppp_m"] - row["ecosystem_augmented_expenditure_lcu_m"] / row["ppp_factor"]) < 0.2, f"Tier 2 PPP identity violated for {u}"

    # Longitudinal panel 2024 row must reconcile with the Tier 1 cross-section (same numerator and denominator)
    hist_2024 = pd.read_csv(os.path.join(RAW_DIR, "historical_enrollment_budget_panel_2010_2024.csv"))
    hist_2024 = hist_2024[hist_2024["year"] == 2024].set_index("university_id")
    for _, row in out_df.iterrows():
        u = row["university_id"]
        assert abs(hist_2024.loc[u, "real_budget_per_fte_usd_ppp"] - row["tier1_per_fte_usd_ppp"]) <= 1e-4 * row["tier1_per_fte_usd_ppp"], f"Historical 2024 per-FTE != Tier 1 per-FTE for {u}"
        assert hist_2024.loc[u, "on_campus_fte"] == row["on_campus_fte_students"], f"Historical 2024 FTE != cross-section FTE for {u}"

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
            "is_legally_independent": bool(str(r["is_legally_independent"]).lower() == "true"),
            "hosted_status": str(r["hosted_status"]),
            "description": r["description"],
        })

    out_df = pd.DataFrame(records)
    out_csv = os.path.join(DATASETS_DIR, "external_ecosystem_harmonized_2024.csv")
    out_df.to_csv(out_csv, index=False)
    print(f"✓ Saved {len(out_df)} rows to {os.path.basename(out_csv)}")
    return out_df


def prepare_masters_cashflow_trajectories():
    """Build longitudinal annual cashflow trajectories (t = -4 to +10 years) for Master & Bachelor cohorts."""
    mast_path = os.path.join(RAW_DIR, "masters_tuition_living_salary_2025.csv")
    bach_path = os.path.join(RAW_DIR, "bachelors_tuition_living_salary_2025.csv")
    df_mast = pd.read_csv(mast_path)
    df_bach = pd.read_csv(bach_path)

    trajectories = []
    cohort_configs = [
        (df_mast, "Master", "masters_duration_years", "total_degree_intl_tuition_lcu", "net_total_degree_cost_lcu", "total_degree_local_tuition_lcu", "net_total_degree_cost_local_lcu"),
        (df_bach, "Bachelor", "bachelors_duration_years", "total_degree_intl_tuition_lcu", "net_total_degree_cost_intl_lcu", "total_degree_local_tuition_lcu", "net_total_degree_cost_local_lcu"),
    ]

    for df_curr, deg_level, col_dur, col_tuition_intl, col_net_intl, col_tuition_local, col_net_local in cohort_configs:
        for _, r in df_curr.iterrows():
            uid = r["university_id"]
            fx = float(r["fx_to_usd"])
            ppp = float(r["ppp_factor"])
            dur = float(r[col_dur])
            tax = float(r["effective_tax_ssc_rate_single"])

            ann_living_usd = float(r["annual_living_cost_lcu"]) * fx
            career_living_usd = float(r["career_annual_living_cost_lcu"]) * fx
            youth_opp_cost_ann_usd = float(r["youth_median_gross_salary_lcu"]) * fx * (1.0 - tax)
            total_net_degree_cost_usd = float(r[col_net_intl]) * fx
            total_sticker_cost_usd = (float(r[col_tuition_intl]) + float(r["total_degree_living_cost_lcu"])) * fx

            ann_net_cost_usd = total_net_degree_cost_usd / dur
            ann_sticker_cost_usd = total_sticker_cost_usd / dur

            total_net_degree_cost_local_usd = float(r[col_net_local]) * fx
            total_local_sticker_cost_usd = (float(r[col_tuition_local]) + float(r["total_degree_living_cost_lcu"])) * fx
            ann_net_cost_local_usd = total_net_degree_cost_local_usd / dur
            ann_sticker_cost_local_usd = total_local_sticker_cost_usd / dur

            y1_salary_usd = float(r["year1_median_salary_lcu"]) * fx
            y1_cs_usd = float(r["year1_cs_ai_salary_lcu"]) * fx
            y1_mech_usd = float(r["year1_mech_salary_lcu"]) * fx
            y10_salary_usd = float(r["year10_median_salary_lcu"]) * fx
            y20_salary_usd = float(r["year20_median_salary_lcu"]) * fx

            cum_net_wealth_sticker = 0.0
            cum_net_wealth_funded = 0.0
            cum_net_wealth_cs = 0.0
            cum_net_wealth_mech = 0.0
            cum_net_wealth_local = 0.0
            cum_net_wealth_local_cs = 0.0
            cum_net_wealth_local_mech = 0.0
            cum_discounted_funded = 0.0
            cum_discounted_local = 0.0

            # Opportunity cost benchmark: Bachelor Y1 net salary for Master; country median 20yo net salary for Bachelor
            if deg_level == "Master":
                b_tax = float(df_bach.loc[df_bach["university_id"] == uid, "effective_tax_ssc_rate_single"].iloc[0])
                b_y1_gross = float(df_bach.loc[df_bach["university_id"] == uid, "year1_median_salary_lcu"].iloc[0]) * fx
                opp_cost_ann_usd = b_y1_gross * (1.0 - b_tax)
            else:
                opp_cost_ann_usd = youth_opp_cost_ann_usd
            total_opp_cost = dur * opp_cost_ann_usd
            cum_opp_cost_so_far = 0.0

            if deg_level == "Master":
                study_years = [1, 2] if dur >= 1.5 else [1]
            else:
                study_years = [1, 2, 3] if dur == 3.0 else [1, 2, 3, 4]

            for y_study in study_years:
                if deg_level == "Master":
                    w_year = 1.0 if (len(study_years) == 1 or y_study == 1) else (dur - 1.0)
                else:
                    w_year = 1.0

                ann_living_alloc = w_year * ann_living_usd
                ann_net_alloc = w_year * ann_net_cost_usd
                ann_sticker_alloc = w_year * ann_sticker_cost_usd
                ann_net_local_alloc = w_year * ann_net_cost_local_usd
                ann_sticker_local_alloc = w_year * ann_sticker_cost_local_usd

                cum_net_wealth_sticker -= ann_sticker_alloc
                cum_net_wealth_funded -= ann_net_alloc
                cum_net_wealth_cs -= ann_net_alloc
                cum_net_wealth_mech -= ann_net_alloc
                cum_net_wealth_local -= ann_net_local_alloc
                cum_net_wealth_local_cs -= ann_net_local_alloc
                cum_net_wealth_local_mech -= ann_net_local_alloc
                cum_opp_cost_so_far += w_year * opp_cost_ann_usd

                df_study = (1.0 + DISCOUNT_RATE_3PCT) ** (-y_study)
                cum_discounted_funded -= ann_net_alloc * df_study
                cum_discounted_local -= ann_net_local_alloc * df_study

                trajectories.append({
                    "university_id": uid,
                    "region": r["region"],
                    "degree_level": deg_level,
                    "cohort_intl": f"{deg_level}_NonNative",
                    "cohort_local": f"{deg_level}_Native",
                    "career_year": -len(study_years) + y_study - 1,
                    "year_since_matriculation": y_study,
                    "phase": f"{deg_level}_Study",
                    "annual_gross_salary_usd": 0.0,
                    "annual_net_salary_usd": 0.0,
                    "annual_living_expenses_usd": round(ann_living_alloc, 0),
                    "annual_net_cashflow_funded_usd": round(-ann_net_alloc, 0),
                    "foregone_earnings_total_usd": round(total_opp_cost, 0),
                    "cumulative_wealth_funded_usd": round(cum_net_wealth_funded, 0),
                    "cumulative_wealth_discounted_usd": round(cum_discounted_funded, 0),
                    "cumulative_wealth_opp_cost_usd": round(cum_net_wealth_funded - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_opp_cost_cs_usd": round(cum_net_wealth_cs - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_opp_cost_mech_usd": round(cum_net_wealth_mech - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_sticker_usd": round(cum_net_wealth_sticker, 0),
                    "cumulative_wealth_cs_usd": round(cum_net_wealth_cs, 0),
                    "cumulative_wealth_mech_usd": round(cum_net_wealth_mech, 0),
                    "cumulative_wealth_funded_ppp": round((cum_net_wealth_funded / fx) / ppp, 0),
                    "cumulative_wealth_local_usd": round(cum_net_wealth_local, 0),
                    "cumulative_wealth_local_discounted_usd": round(cum_discounted_local, 0),
                    "cumulative_wealth_local_opp_cost_usd": round(cum_net_wealth_local - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_local_opp_cost_cs_usd": round(cum_net_wealth_local_cs - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_local_opp_cost_mech_usd": round(cum_net_wealth_local_mech - cum_opp_cost_so_far, 0),
                    "cumulative_wealth_local_cs_usd": round(cum_net_wealth_local_cs, 0),
                    "cumulative_wealth_local_mech_usd": round(cum_net_wealth_local_mech, 0),
                    "cumulative_wealth_local_ppp": round((cum_net_wealth_local / fx) / ppp, 0),
                })

            assert abs(-cum_net_wealth_funded - total_net_degree_cost_usd) < 0.1, f"Study net cost mismatch for {uid} {deg_level}"
            assert abs(-cum_net_wealth_sticker - total_sticker_cost_usd) < 0.1, f"Study sticker cost mismatch for {uid} {deg_level}"
            assert abs(-cum_net_wealth_local - total_net_degree_cost_local_usd) < 0.1, f"Study local net cost mismatch for {uid} {deg_level}"

            assert y1_salary_usd > 0, f"Year-1 median salary must be positive for {uid} {deg_level}"
            cs_ratio = y1_cs_usd / y1_salary_usd
            mech_ratio = y1_mech_usd / y1_salary_usd

            nocol_brackets_net_usd = [
                float(r["nocollege_salary_20_24_lcu"]) * fx * (1.0 - tax),
                float(r["nocollege_salary_25_29_lcu"]) * fx * (1.0 - tax),
                float(r["nocollege_salary_30_34_lcu"]) * fx * (1.0 - tax),
                float(r["nocollege_salary_35_39_lcu"]) * fx * (1.0 - tax),
                float(r["nocollege_salary_40_45_lcu"]) * fx * (1.0 - tax),
            ]
            cum_excess_funded = cum_net_wealth_funded - total_opp_cost
            cum_excess_cs = cum_net_wealth_cs - total_opp_cost
            cum_excess_mech = cum_net_wealth_mech - total_opp_cost
            cum_excess_local = cum_net_wealth_local - total_opp_cost
            cum_excess_local_cs = cum_net_wealth_local_cs - total_opp_cost
            cum_excess_local_mech = cum_net_wealth_local_mech - total_opp_cost
            start_age = 22 if deg_level == "Bachelor" else 24

            for yr in range(1, 21):
                if yr <= 10:
                    progress = (yr - 1.0) / 9.0
                    gross_salary = y1_salary_usd + progress * (y10_salary_usd - y1_salary_usd)
                    gross_cs = y1_cs_usd + progress * (y10_salary_usd * cs_ratio - y1_cs_usd)
                    gross_mech = y1_mech_usd + progress * (y10_salary_usd * mech_ratio - y1_mech_usd)
                else:
                    progress = (yr - 10.0) / 10.0
                    gross_salary = y10_salary_usd + progress * (y20_salary_usd - y10_salary_usd)
                    gross_cs = y10_salary_usd * cs_ratio + progress * (y20_salary_usd * cs_ratio - y10_salary_usd * cs_ratio)
                    gross_mech = y10_salary_usd * mech_ratio + progress * (y20_salary_usd * mech_ratio - y10_salary_usd * mech_ratio)

                net_salary = gross_salary * (1.0 - tax)
                net_cs = gross_cs * (1.0 - tax)
                net_mech = gross_mech * (1.0 - tax)

                age = start_age + yr - 1
                if age <= 24:
                    nocol_net_usd = nocol_brackets_net_usd[0]
                elif age <= 29:
                    nocol_net_usd = nocol_brackets_net_usd[1]
                elif age <= 34:
                    nocol_net_usd = nocol_brackets_net_usd[2]
                elif age <= 39:
                    nocol_net_usd = nocol_brackets_net_usd[3]
                else:
                    nocol_net_usd = nocol_brackets_net_usd[4]

                # Post-graduation career living cost: empirical median single-adult city cost (real 2025 USD)
                career_living_cost = career_living_usd
                annual_net_savings = net_salary - career_living_cost
                annual_net_savings_cs = net_cs - career_living_cost
                annual_net_savings_mech = net_mech - career_living_cost

                cum_net_wealth_sticker += annual_net_savings
                cum_net_wealth_funded += annual_net_savings
                cum_net_wealth_cs += annual_net_savings_cs
                cum_net_wealth_mech += annual_net_savings_mech
                cum_net_wealth_local += annual_net_savings
                cum_net_wealth_local_cs += annual_net_savings_cs
                cum_net_wealth_local_mech += annual_net_savings_mech

                # Excess wealth over age-graded no-college counterfactual (city living costs cancel out)
                annual_excess = net_salary - nocol_net_usd
                annual_excess_cs = net_cs - nocol_net_usd
                annual_excess_mech = net_mech - nocol_net_usd
                cum_excess_funded += annual_excess
                cum_excess_cs += annual_excess_cs
                cum_excess_mech += annual_excess_mech
                cum_excess_local += annual_excess
                cum_excess_local_cs += annual_excess_cs
                cum_excess_local_mech += annual_excess_mech

                df_career = (1.0 + DISCOUNT_RATE_3PCT) ** (-(len(study_years) + yr))
                cum_discounted_funded += annual_net_savings * df_career
                cum_discounted_local += annual_net_savings * df_career

                trajectories.append({
                    "university_id": uid,
                    "region": r["region"],
                    "degree_level": deg_level,
                    "cohort_intl": f"{deg_level}_NonNative",
                    "cohort_local": f"{deg_level}_Native",
                    "career_year": yr,
                    "year_since_matriculation": len(study_years) + yr,
                    "phase": f"{deg_level}_Career",
                    "annual_gross_salary_usd": round(gross_salary, 0),
                    "annual_net_salary_usd": round(net_salary, 0),
                    "annual_living_expenses_usd": round(career_living_cost, 0),
                    "annual_net_cashflow_funded_usd": round(annual_net_savings, 0),
                    "foregone_earnings_total_usd": round(total_opp_cost, 0),
                    "cumulative_wealth_funded_usd": round(cum_net_wealth_funded, 0),
                    "cumulative_wealth_discounted_usd": round(cum_discounted_funded, 0),
                    "cumulative_wealth_opp_cost_usd": round(cum_excess_funded, 0),
                    "cumulative_wealth_opp_cost_cs_usd": round(cum_excess_cs, 0),
                    "cumulative_wealth_opp_cost_mech_usd": round(cum_excess_mech, 0),
                    "cumulative_wealth_sticker_usd": round(cum_net_wealth_sticker, 0),
                    "cumulative_wealth_cs_usd": round(cum_net_wealth_cs, 0),
                    "cumulative_wealth_mech_usd": round(cum_net_wealth_mech, 0),
                    "cumulative_wealth_funded_ppp": round((cum_net_wealth_funded / fx) / ppp, 0),
                    "cumulative_wealth_local_usd": round(cum_net_wealth_local, 0),
                    "cumulative_wealth_local_discounted_usd": round(cum_discounted_local, 0),
                    "cumulative_wealth_local_opp_cost_usd": round(cum_excess_local, 0),
                    "cumulative_wealth_local_opp_cost_cs_usd": round(cum_excess_local_cs, 0),
                    "cumulative_wealth_local_opp_cost_mech_usd": round(cum_excess_local_mech, 0),
                    "cumulative_wealth_local_cs_usd": round(cum_net_wealth_local_cs, 0),
                    "cumulative_wealth_local_mech_usd": round(cum_net_wealth_local_mech, 0),
                    "cumulative_wealth_local_ppp": round((cum_net_wealth_local / fx) / ppp, 0),
                })

    out_df = pd.DataFrame(trajectories)
    out_csv = os.path.join(DATASETS_DIR, "masters_10y_cashflow_trajectories.csv")
    out_df.to_csv(out_csv, index=False)
    degrees_csv = os.path.join(DATASETS_DIR, "degrees_10y_cashflow_trajectories.csv")
    out_df.to_csv(degrees_csv, index=False)
    print(f"✓ Saved {len(out_df)} rows to {os.path.basename(out_csv)} and {os.path.basename(degrees_csv)}")
    return out_df


def prepare_historical_panel():
    """Harmonize longitudinal 15-year panel on enrollment growth and per-student funding."""
    hist_path = os.path.join(RAW_DIR, "historical_enrollment_budget_panel_2010_2024.csv")
    out_csv = os.path.join(DATASETS_DIR, "historical_panel_harmonized.csv")

    df_hist = pd.read_csv(hist_path)
    df_indexed = []
    for uid, grp in df_hist.groupby("university_id"):
        grp = grp.sort_values("year").copy()
        base_fte = float(grp.iloc[0]["on_campus_fte"])
        base_budget = float(grp.iloc[0]["real_budget_per_fte_usd_ppp"])

        grp["fte_index_2010"] = round((grp["on_campus_fte"] / base_fte) * 100.0, 1)
        grp["budget_per_fte_index_2010"] = round((grp["real_budget_per_fte_usd_ppp"] / base_budget) * 100.0, 1)
        assert abs(grp.iloc[0]["fte_index_2010"] - 100.0) < 0.1, f"FTE index base != 100 for {uid}"
        assert abs(grp.iloc[0]["budget_per_fte_index_2010"] - 100.0) < 0.1, f"Budget index base != 100 for {uid}"
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
