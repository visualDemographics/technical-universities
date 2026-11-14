#!/usr/bin/env python3
"""Econometric Modeling & Synoptic Matrix Visualization (`src/modeling.py`).

Fits statistical, non-linear, and causal decomposition models to datasets/,
evaluates path-independent Shapley waterfall attributions across all K! = 120
permutations, and deterministically renders all individual panels (Panels A–I),
the 4-variant bottom-row comparison matrix (Master & Bachelor vs Native & Non-Native),
plus the publication-grade 9-Panel (3x3) Synoptic Matrices in both English and German.

Strict AST Contract: Zero synthetic random generators, zero silent numeric fallbacks,
zero domain float defaults.
"""

import csv
import itertools
import math
import os
import shutil
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(ROOT, "datasets")
REL_TOL = 1e-4  # relative tolerance for accounting reconciliations on rounded dataset columns
PLOTS_DIR = os.path.join(ROOT, "plots")

# Coordinated Visual Language Palette
COLOR_US = "#A31F34"       # Cardinal Red / MIT
COLOR_EU = "#0065BD"       # TUM Blue / European Tech
COLOR_ASIA = "#008080"     # Teal / Asian Tech Flagships
COLOR_NEUTRAL = "#4A4A4A"
COLOR_ACCENT = "#D9534F"

PALETTE_9 = {
    "MIT": "#A31F34",
    "Caltech": "#FF6C0C",
    "Georgia_Tech": "#B3A369",
    "Imperial": "#002147",
    "ETH_Zurich": "#1F407A",
    "TUM": "#0065BD",
    "Tsinghua": "#82318E",
    "KAIST": "#004191",
    "NTU": "#C8102E",
}


def load_datasets_and_benchmarks():
    """Load empirical datasets and benchmark catalog."""
    master_path = os.path.join(DATASETS_DIR, "university_master_comparison_2024.csv")
    eco_path = os.path.join(DATASETS_DIR, "external_ecosystem_harmonized_2024.csv")
    traj_path = os.path.join(DATASETS_DIR, "masters_10y_cashflow_trajectories.csv")
    hist_path = os.path.join(DATASETS_DIR, "historical_panel_harmonized.csv")
    bench_path = os.path.join(DATASETS_DIR, "literature_empirical_benchmarks.csv")

    df_master = pd.read_csv(master_path)
    df_eco = pd.read_csv(eco_path)
    df_traj = pd.read_csv(traj_path)
    df_hist = pd.read_csv(hist_path)

    benchmarks = {}
    with open(bench_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            benchmarks[r["parameter_id"].strip()] = float(r["wert"])

    return {
        "master": df_master,
        "ecosystem": df_eco,
        "trajectories": df_traj,
        "historical": df_hist,
        "benchmarks": benchmarks,
    }


def compute_shapley_waterfall_decomposition(df_master, benchmarks):
    """Compute path-independent Shapley value decomposition for MIT/Caltech vs. TUM.

    Evaluates all K! = 120 permutations of 5 structural adjustments:
    1. strip_ffrdc: Strip DoD/NASA FFRDCs (Lincoln Lab & JPL)
    2. strip_hospital: Strip Clinical Hospital Patient Turnover (TUM Klinikum)
    3. add_ecosystem: Incorporate Co-located Campus Research Clusters
    4. ppp_deflation: OECD / World Bank Purchasing Power Parity (PPP) Price Deflation
    5. scale_dilution: Student Scale (On-Campus FTE vs. Headcount Normalization)
    """
    row_mit = df_master.loc[df_master["university_id"] == "MIT"].iloc[0]
    row_cal = df_master.loc[df_master["university_id"] == "Caltech"].iloc[0]
    row_tum = df_master.loc[df_master["university_id"] == "TUM"].iloc[0]

    mit_ffrdc = benchmarks["MIT_LINCOLN_LAB_PASS_THROUGH"]
    cal_ffrdc = benchmarks["CALTECH_JPL_PASS_THROUGH"]
    tum_hosp = benchmarks["TUM_GROSS_BUDGET_2023"] - benchmarks["TUM_CORE_ACADEMIC_BUDGET_2023"]

    mit_eco = row_mit["ecosystem_augmented_expenditure_lcu_m"] - row_mit["core_academic_expenditure_lcu_m"]
    cal_eco = row_cal["ecosystem_augmented_expenditure_lcu_m"] - row_cal["core_academic_expenditure_lcu_m"]
    tum_eco = row_tum["ecosystem_augmented_expenditure_lcu_m"] - row_tum["core_academic_expenditure_lcu_m"]

    factors = ["strip_ffrdc", "strip_hospital", "add_ecosystem", "ppp_deflation", "scale_dilution"]

    def evaluate_state(active_set):
        """Gap = mean of US per-student ratios (MIT, Caltech) minus TUM per-student ratio.

        Per-student ratios are computed per university BEFORE averaging so that the
        fully adjusted state reconciles exactly with the Tier 2 per-FTE table
        (a pooled ratio of means would weight MIT by its larger student body).
        """
        mit_exp = row_mit["gross_operating_expenditure_lcu_m"]
        cal_exp = row_cal["gross_operating_expenditure_lcu_m"]
        tum_exp = row_tum["gross_operating_expenditure_lcu_m"]

        if "strip_ffrdc" in active_set:
            mit_exp -= mit_ffrdc
            cal_exp -= cal_ffrdc
        if "strip_hospital" in active_set:
            tum_exp -= tum_hosp
        if "add_ecosystem" in active_set:
            mit_exp += mit_eco
            cal_exp += cal_eco
            tum_exp += tum_eco

        mit_ppp = 1.0
        cal_ppp = 1.0
        tum_ppp = row_tum["ppp_factor"] if "ppp_deflation" in active_set else 1.0 / row_tum["fx_to_usd"]

        mit_val_usd = mit_exp / mit_ppp
        cal_val_usd = cal_exp / cal_ppp
        tum_val_usd = tum_exp / tum_ppp

        if "scale_dilution" in active_set:
            mit_students = row_mit["on_campus_fte_students"]
            cal_students = row_cal["on_campus_fte_students"]
            tum_students = row_tum["on_campus_fte_students"]
        else:
            mit_students = row_mit["enrolled_headcount_total"]
            cal_students = row_cal["enrolled_headcount_total"]
            tum_students = row_tum["enrolled_headcount_total"]

        us_per_cap = ((mit_val_usd * 1000000.0 / mit_students) + (cal_val_usd * 1000000.0 / cal_students)) / 2.0
        tum_per_cap = (tum_val_usd * 1000000.0) / tum_students
        return us_per_cap - tum_per_cap

    v_empty = evaluate_state(set())
    v_full = evaluate_state(set(factors))

    # Accounting identities: fully adjusted gap == Tier 2 PPP per-FTE gap; headline == Tier 0 nominal per-headcount gap
    tier2_gap = ((row_mit["tier2_per_fte_usd_ppp"] + row_cal["tier2_per_fte_usd_ppp"]) / 2.0) - row_tum["tier2_per_fte_usd_ppp"]
    assert abs(v_full - tier2_gap) < REL_TOL * abs(tier2_gap), f"Waterfall end state {v_full} != Tier 2 gap {tier2_gap}"
    tier0_nom_gap = (
        (row_mit["tier0_gross_usd_nom_m"] * 1e6 / row_mit["enrolled_headcount_total"])
        + (row_cal["tier0_gross_usd_nom_m"] * 1e6 / row_cal["enrolled_headcount_total"])
    ) / 2.0 - row_tum["tier0_gross_usd_nom_m"] * 1e6 / row_tum["enrolled_headcount_total"]
    assert abs(v_empty - tier0_nom_gap) < REL_TOL * abs(tier0_nom_gap), "Waterfall baseline != Tier 0 nominal per-headcount gap"

    shapley_values = {f: 0.0 for f in factors}
    all_perms = list(itertools.permutations(factors))
    n_perms = len(all_perms)

    for p in all_perms:
        curr = set()
        v_curr = v_empty
        for step_factor in p:
            next_set = curr | {step_factor}
            v_next = evaluate_state(next_set)
            marginal = v_next - v_curr
            shapley_values[step_factor] += marginal / n_perms
            curr = next_set
            v_curr = v_next

    canonical_order = ["strip_ffrdc", "strip_hospital", "add_ecosystem", "ppp_deflation", "scale_dilution"]
    canonical_steps = [("Baseline Headline Disparity", 0.0, v_empty, 0.0)]
    curr_s = set()
    v_c = v_empty
    for f in canonical_order:
        curr_s.add(f)
        v_n = evaluate_state(curr_s)
        canonical_steps.append((f, v_n - v_c, v_n, shapley_values[f]))
        v_c = v_n

    return {
        "v_empty": v_empty,
        "v_full": v_full,
        "shapley_values": shapley_values,
        "canonical_steps": canonical_steps,
    }


def fit_bivariate_efficiency_surface(df_master):
    """Fit 2D non-linear Cobb-Douglas production surface."""
    df = df_master.copy()
    B = df["tier2_per_fte_usd_ppp"].values / 1000.0
    F = (df["tenured_tenure_track_faculty"].values / df["on_campus_fte_students"].values) * 100.0
    Q = df["cwts_leiden_pp_top10_pct"].values

    def model_func(X, alpha, beta, gamma):
        b, f = X
        return alpha + beta * np.log(b) + gamma * np.log(f)

    popt, pcov = curve_fit(model_func, (B, F), Q, p0=[10.0, 3.0, 1.0])
    perr = np.sqrt(np.diag(pcov))

    b_grid = np.linspace(min(B) - 5.0, max(B) + 10.0, 60)
    f_grid = np.linspace(min(F) - 1.0, max(F) + 2.0, 60)
    B_mesh, F_mesh = np.meshgrid(b_grid, f_grid)
    Q_surface = model_func((B_mesh, F_mesh), *popt)

    residuals = Q - model_func((B, F), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((Q - np.mean(Q)) ** 2)
    r_squared = 1.0 - (ss_res / ss_tot)

    return {
        "popt": popt,
        "perr": perr,
        "r_squared": r_squared,
        "B_mesh": B_mesh,
        "F_mesh": F_mesh,
        "Q_surface": Q_surface,
    }


# ==============================================================================
# INDIVIDUAL PANEL RENDERERS (Panels A through I)
# ==============================================================================

def render_panel_a(ax, data, lang="en", is_standalone=False):
    """Panel A: Budget Accounting Tiers in Nominal USD (Raw vs Core vs Ecosystem-Augmented)."""
    df = data["master"].sort_values("tier2_augmented_usd_nom_m", ascending=False)
    x = np.arange(len(df))
    width = 0.26

    t0 = df["tier0_gross_usd_nom_m"].values
    t1 = df["tier1_core_usd_nom_m"].values
    t2 = df["tier2_augmented_usd_nom_m"].values

    lbl_t0 = "Tier 0: Gross Operating Exp (Nominal)" if lang == "en" else "Tier 0: Bruttoausgaben (Nominal)"
    lbl_t1 = "Tier 1: Core Academic ex-Hospital/FFRDC" if lang == "en" else "Tier 1: Kernausgaben ohne Klinik/FFRDC"
    lbl_t2 = "Tier 2: Augmented Student-Facing (Ecosystem)" if lang == "en" else "Tier 2: Erweitertes Ökosystem (Partner)"

    ax.bar(x - width, t0, width, label=lbl_t0, color="#999999", alpha=0.85)
    ax.bar(x, t1, width, label=lbl_t1, color="#1F407A", alpha=0.90)
    ax.bar(x + width, t2, width, label=lbl_t2, color="#0065BD", alpha=0.95)

    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Budget (Million Nominal USD)" if lang == "en" else "Budget (Mio. Nominal USD)", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Panel A: Institutional Operating Budgets (Nominal USD)" if lang == "en" else "Panel A: Institutionelle Betriebsbudgets (Nominal USD)", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=6.8 if not is_standalone else 9, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_b(ax, data, lang="en", is_standalone=False):
    """Panel B: Enrollment Scale (Headcount vs On-Campus FTE) & Supervision Ratios."""
    df = data["master"].sort_values("on_campus_fte_students", ascending=False)
    x = np.arange(len(df))
    width = 0.35

    hc = df["enrolled_headcount_total"].values
    fte = df["on_campus_fte_students"].values

    ax.bar(x - width/2.0, hc, width, label="Raw Headcount" if lang == "en" else "Kopfzahl (Gesamt)", color="#B3A369", alpha=0.85)
    ax.bar(x + width/2.0, fte, width, label="On-Campus FTE" if lang == "en" else "Präsenz-Vollzeitäquivalent (FTE)", color="#0065BD", alpha=0.95)

    gt_idx = list(df["university_id"]).index("Georgia_Tech")
    online_k = (hc[gt_idx] - fte[gt_idx]) / 1000.0
    y_offset = float(np.max(hc)) * 0.06
    ax.annotate(f"{online_k:.1f}k Online MS\n(OMSCS)", xy=(gt_idx - width/2.0, hc[gt_idx]), xytext=(gt_idx - 0.4, hc[gt_idx] + y_offset),
                arrowprops=dict(arrowstyle="->", color="black", lw=1), fontsize=6.2 if not is_standalone else 8.5, ha="center")

    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Enrolled Students" if lang == "en" else "Immatrikulierte Studierende", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Panel B: Enrollment Scale & On-Campus FTE Denominators" if lang == "en" else "Panel B: Studierendenzahlen & Präsenz-Nenner", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=6.8 if not is_standalone else 9, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_c(ax, data, lang="en", is_standalone=False):
    """Panel C: Corrected Student-Facing Budget per On-Campus FTE (Nominal vs PPP)."""
    df = data["master"].sort_values("tier2_per_fte_usd_ppp", ascending=False)
    x = np.arange(len(df))
    width = 0.35

    nom = df["tier2_per_fte_usd_nom"].values / 1000.0
    ppp = df["tier2_per_fte_usd_ppp"].values / 1000.0

    lbl_nom = "Nominal USD / FTE" if lang == "en" else "Nominal USD / FTE"
    lbl_ppp = "PPP Int'l $ / FTE" if lang == "en" else "Kaufkraftbereinigt (PPP) $ / FTE"

    ax.bar(x - width/2.0, nom, width, label=lbl_nom, color="#82318E", alpha=0.75)
    ax.bar(x + width/2.0, ppp, width, label=lbl_ppp, color="#008080", alpha=0.95)

    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Budget per FTE ($1,000)" if lang == "en" else "Budget pro FTE (Tsd. $)", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Panel C: Corrected Student-Facing Budget per FTE" if lang == "en" else "Panel C: Korrigiertes Budget pro Präsenz-Studierenden", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=6.8 if not is_standalone else 9, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_d(ax, data, lang="en", is_standalone=False):
    """Panel D: Multi-Pillar Absolute Cardinal Scores & Global Multi-Ranking Profile (Zero Overlap)."""
    df = data["master"].sort_values("the_2025_overall_score", ascending=False).reset_index(drop=True)
    x = np.arange(len(df))
    width = 0.19

    qs_score = df["qs_2025_overall_score"].values
    the_score = df["the_2025_overall_score"].values
    arwu_score = df["arwu_2024_score"].values
    emp_score = df["qs_employer_reputation_score"].values

    ax.bar(x - 1.5*width, qs_score, width, label="QS 2025 Score" if lang == "en" else "QS Gesamtnote", color="#1F407A", alpha=0.90)
    ax.bar(x - 0.5*width, the_score, width, label="THE 2025 Score" if lang == "en" else "THE Gesamtnote", color="#0065BD", alpha=0.92)
    ax.bar(x + 0.5*width, arwu_score, width, label="ARWU 2024 Score" if lang == "en" else "ARWU Gesamtnote", color="#708090", alpha=0.85)
    ax.bar(x + 1.5*width, emp_score, width, label="Employer Rep" if lang == "en" else "Arbeitgeber-Reputation", color="#D9534F", alpha=0.92)

    # Benchmark reference thresholds
    ax.axhline(90.0, color="#666666", linestyle=":", lw=0.9, alpha=0.6)
    ax.axhline(80.0, color="#888888", linestyle="--", lw=0.8, alpha=0.5)

    tier10_txt = "90+ (Top 10)" if lang == "en" else "90+ (Top-10)"
    ax.text(8.45, 91.0, tier10_txt, fontsize=5.8 if not is_standalone else 7.5, color="#555555", style="italic", ha="right")

    # Fixed 3-tier vertical bands above all bars guarantee zero overlap regardless of bar height
    tier_y = (103.0, 118.5, 134.0)
    for i, (_, row) in enumerate(df.iterrows()):
        qs_r = int(row["qs_2025_rank"])
        the_r = int(row["the_2025_rank"])
        arwu_r = int(row["arwu_2024_rank"])
        usn_r = int(row["us_news_2025_rank"])
        eng_r = int(row["the_eng_tech_rank_2025"])
        geurs_r = int(row["geurs_employability_rank_2025"])

        y_pos = tier_y[i % 3]
        badge = f"QS#{qs_r} THE#{the_r}\nARWU#{arwu_r} USN#{usn_r}\nEng#{eng_r} GEU#{geurs_r}"

        ax.text(x[i], y_pos, badge, ha="center", va="bottom",
                fontsize=4.1 if not is_standalone else 6.0, fontweight="bold",
                color="#222222", linespacing=0.92,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="#d0d0d0", alpha=0.90, lw=0.4))

    ax.set_ylim(0, 172)
    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Absolute Score (0–100 Scale)" if lang == "en" else "Absoluter Wertungsscore (0–100)", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Panel D: Absolute Evaluation Scores & Global Rank Profiles" if lang == "en" else "Panel D: Absolute Wertungsscores & Globale Rangprofile", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=5.8 if not is_standalone else 8.2, loc="upper right", ncol=2)
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_d_dual(fig, data, lang="en"):
    """Render 2-subplot deep dive for Panel D: Absolute Scores + Multi-Ranking Global Profile."""
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    fig.subplots_adjust(wspace=0.25)

    # Subplot 1: Absolute Scores (0-100)
    render_panel_d(ax1, data, lang=lang, is_standalone=True)
    ax1.set_title("A: Multi-Pillar Absolute Cardinal Scores (0–100 Scale)" if lang == "en" else "A: Absoluter Wertungsscore (0–100 Skala)", fontsize=11, fontweight="bold", pad=10)

    # Subplot 2: Multi-System Global Rank Profile
    df_sorted = data["master"].sort_values("the_2025_overall_score", ascending=False).reset_index(drop=True)
    x = np.arange(len(df_sorted))
    width = 0.20

    qs_ranks = df_sorted["qs_2025_rank"].values
    the_ranks = df_sorted["the_2025_rank"].values
    arwu_ranks = df_sorted["arwu_2024_rank"].values
    usn_ranks = df_sorted["us_news_2025_rank"].values

    ax2.bar(x - 1.5*width, qs_ranks, width, label="QS World Rank 2025" if lang == "en" else "QS Gesamtrang 2025", color="#1F407A", alpha=0.88)
    ax2.bar(x - 0.5*width, the_ranks, width, label="THE World Rank 2025" if lang == "en" else "THE Gesamtrang 2025", color="#0065BD", alpha=0.92)
    ax2.bar(x + 0.5*width, arwu_ranks, width, label="ARWU Shanghai 2024" if lang == "en" else "ARWU Shanghai 2024", color="#708090", alpha=0.85)
    ax2.bar(x + 1.5*width, usn_ranks, width, label="US News Global 2025" if lang == "en" else "US News Global 2025", color="#FF6C0C", alpha=0.90)

    for i in range(len(df_sorted)):
        eng_r = int(df_sorted["the_eng_tech_rank_2025"].iloc[i])
        geurs_r = int(df_sorted["geurs_employability_rank_2025"].iloc[i])
        max_r = max(qs_ranks[i], the_ranks[i], arwu_ranks[i], usn_ranks[i])
        ax2.annotate(f"Eng#{eng_r}\nGEU#{geurs_r}", xy=(x[i], max_r), xytext=(x[i], max_r + 14),
                     arrowprops=dict(arrowstyle="->", color="#008080", lw=0.8),
                     fontsize=6.6, ha="center", color="#008080", fontweight="bold")

    ax2.set_ylim(0, 305)
    ax2.set_xticks(x)
    ax2.set_xticklabels([u.replace("_", " ") for u in df_sorted["university_id"]], rotation=30, ha="right", fontsize=9.5)
    ax2.set_ylabel("Global Rank (Lower is Better)" if lang == "en" else "Weltweiter Rang (Niedriger ist besser)", fontsize=10.5, fontweight="bold")
    ax2.set_title("B: Multi-System Global Ranking Profiles & Discipline Pivot" if lang == "en" else "B: Multi-System-Rangprofile & TU-Pivot", fontsize=11, fontweight="bold", pad=10)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_e(ax, data, lang="en", is_standalone=False):
    """Panel E: Multi-Dimensional Research Efficiency (Annual Top-10% cited pubs per $10M PPP)."""
    df = data["master"].sort_values("annual_top10_pubs_per_10m_ppp_spend", ascending=False)
    x = np.arange(len(df))

    eff_ann = df["annual_top10_pubs_per_10m_ppp_spend"].values
    colors = [COLOR_US if r == "US" else (COLOR_EU if r == "EU" else COLOR_ASIA) for r in df["region"]]

    bars = ax.bar(x, eff_ann, color=colors, alpha=0.90, width=0.56, edgecolor="white", linewidth=0.6)
    for b, val in zip(bars, eff_ann):
        ax.text(
            b.get_x() + b.get_width() / 2.0,
            b.get_height() + 0.22,
            f"{val:.1f}/yr",
            ha="center",
            va="bottom",
            fontsize=6.6 if not is_standalone else 8.8,
            fontweight="bold",
            color="#222222",
        )

    ax.set_ylim(0, 12.0)
    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Top-10% Papers / Year / $10M PPP" if lang == "en" else "Top-10% Zitationen / Jahr / 10 Mio. $ KKP", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Panel E: Cost-Normalized Research Efficiency" if lang == "en" else "Panel E: Kostennormierte Forschungseffizienz", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)

    legend_patches = [
        mpatches.Patch(color=COLOR_US, label="US Universities" if lang == "en" else "USA"),
        mpatches.Patch(color=COLOR_EU, label="European Universities" if lang == "en" else "Europa"),
        mpatches.Patch(color=COLOR_ASIA, label="Asian Universities" if lang == "en" else "Asien"),
    ]
    ax.legend(handles=legend_patches, fontsize=6.8 if not is_standalone else 9, loc="upper right", framealpha=0.92)
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_f(ax, data, lang="en", is_standalone=False):
    """Panel F: Undergraduate Admissions Selectivity & First-Year Exam Screening Profile."""
    df = data["master"].sort_values("undergrad_acceptance_rate_pct", ascending=True)
    x = np.arange(len(df))
    width = 0.36

    acc_rate = df["undergrad_acceptance_rate_pct"].values
    attrition = df["first_year_screening_attrition_pct"].values

    lbl_acc = "Admissions Acceptance Rate (%)" if lang == "en" else "Zulassungsquote (%)"
    lbl_att = "First-Year Cohort Attrition (%)" if lang == "en" else "Studienabbruch im 1. Studienjahr (%)"

    ax.bar(x - width / 2.0, acc_rate, width, label=lbl_acc, color="#1F407A", alpha=0.92, edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2.0, attrition, width, label=lbl_att, color="#D9534F", alpha=0.88, edgecolor="white", linewidth=0.5)

    # Text badges above bars with outward offset when adjacent bars have similar height
    for idx in range(len(df)):
        y_acc = acc_rate[idx]
        y_att = attrition[idx]
        same_height = abs(y_acc - y_att) < 4.0 and y_att >= 10.0
        dx = 0.06 if same_height else 0.0

        acc_txt = f"{y_acc:.0f}%" if y_acc >= 20.0 else f"{y_acc:.1f}%"
        ax.text(
            x[idx] - width / 2.0 - dx,
            y_acc + 0.7,
            acc_txt,
            ha="center",
            va="bottom",
            fontsize=5.6 if not is_standalone else 8.2,
            fontweight="bold",
            color="#1F407A",
        )

        if y_att >= 10.0:
            ax.text(
                x[idx] + width / 2.0 + dx,
                y_att + 0.7,
                f"{y_att:.0f}%",
                ha="center",
                va="bottom",
                fontsize=5.6 if not is_standalone else 8.2,
                fontweight="bold",
                color="#C0392B",
            )
        else:
            ax.text(
                x[idx] + width / 2.0,
                y_att + 0.5,
                f"{y_att:.1f}%" if y_att not in (1.0, 2.0, 3.0, 4.0) else f"{y_att:.0f}%",
                ha="center",
                va="bottom",
                fontsize=4.8 if not is_standalone else 7.0,
                color="#B03A2E",
                alpha=0.85,
            )

    # Paradigm annotation for ETH (arrow terminates above the 20% label and above the 28% acceptance bar)
    eth_idx = list(df["university_id"]).index("ETH_Zurich")
    ax.annotate(
        "Basisprüfung\nScreening" if lang == "en" else "Basisprüfungs-\nFilter",
        xy=(eth_idx + width / 2.0, attrition[eth_idx] + 3.2),
        xytext=(eth_idx - 0.12, 34.5),
        arrowprops=dict(arrowstyle="->", color="#900C3F", lw=1.0, shrinkA=0, shrinkB=2),
        fontsize=5.6 if not is_standalone else 8.0,
        ha="center",
        va="bottom",
        color="#900C3F",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.18", fc="#FFF8F8", ec="#E6B0AA", lw=0.6, alpha=0.92),
    )

    ax.set_ylim(0, 44)
    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Rate (%)" if lang == "en" else "Quote (%)", fontsize=8.5 if not is_standalone else 11)

    title_en = "Panel F: Admissions Acceptance Rate vs. First-Year Attrition"
    title_de = "Panel F: Bachelor-Zulassungsquote vs. Abbruch im 1. Studienjahr"
    ax.set_title(title_en if lang == "en" else title_de, fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=6.0 if not is_standalone else 8.8, loc="upper left", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_g(ax, data, lang="en", is_standalone=False, degree_level="Master", tuition_mode="intl"):
    """Panel G: Degree Total Cost Lifecycle (Sticker vs Net of Aid/Fellowships/HiWi)."""
    if degree_level == "Master":
        col_sticker = "total_sticker_cost_usd" if tuition_mode == "intl" else "local_total_sticker_cost_usd"
        col_net = "net_total_degree_cost_usd" if tuition_mode == "intl" else "local_net_total_degree_cost_usd"
        cohort_tag = "Engineering Master Intl" if tuition_mode == "intl" else "Engineering Master Domestic"
        cohort_tag_de = "Ingenieur-Master Intl" if tuition_mode == "intl" else "Ingenieur-Master Inland"
    else:
        col_sticker = "bachelors_total_sticker_cost_usd" if tuition_mode == "intl" else "bachelors_local_total_sticker_cost_usd"
        col_net = "bachelors_net_total_degree_cost_usd" if tuition_mode == "intl" else "bachelors_local_net_total_degree_cost_usd"
        cohort_tag = "Engineering Bachelor Intl" if tuition_mode == "intl" else "Engineering Bachelor Domestic"
        cohort_tag_de = "Ingenieur-Bachelor Intl" if tuition_mode == "intl" else "Ingenieur-Bachelor Inland"

    df = data["master"].sort_values(col_sticker, ascending=False)
    x = np.arange(len(df))
    width = 0.35

    sticker = df[col_sticker].values / 1000.0
    net = df[col_net].values / 1000.0

    lbl_sticker = ("Sticker Cost (Tuition + Living)" if tuition_mode == "intl" else "Local Sticker (In-State / Domestic)") if lang == "en" else ("Listenpreis (Studiengebühr + Leben)" if tuition_mode == "intl" else "Inlands-Listenpreis (In-State / Inland)")
    lbl_net = ("Net Cost (ex-RA/TA/HiWi Offsets)" if tuition_mode == "intl" else "Local Net Cost (ex-Fellowships/HiWi)") if lang == "en" else ("Nettokosten (nach RA/TA/HiWi)" if tuition_mode == "intl" else "Inlands-Nettokosten (nach Stipendien/HiWi)")

    bars_s = ax.bar(x - width/2.0, sticker, width, label=lbl_sticker, color="#D9534F", alpha=0.85)
    bars_n = ax.bar(x + width/2.0, net, width, label=lbl_net, color="#0065BD", alpha=0.95)

    max_val = max(float(np.max(sticker)), float(np.max(net)))
    lbl_fs = 4.9 if not is_standalone else 7.5
    for bar_s, s_val, bar_n, n_val in zip(bars_s, sticker, bars_n, net):
        near = abs(s_val - n_val) < max_val * 0.08
        s_y = s_val + max_val * (0.048 if near else 0.014)
        n_y = n_val + max_val * 0.012
        ax.text(bar_s.get_x() + bar_s.get_width() / 2.0 - 0.03, s_y, f"${s_val:.0f}k",
                ha="center", va="bottom", fontsize=lbl_fs, color="#A93226", fontweight="bold")
        ax.text(bar_n.get_x() + bar_n.get_width() / 2.0 + 0.03, n_y, f"${n_val:.0f}k",
                ha="center", va="bottom", fontsize=lbl_fs, color="#004C97", fontweight="bold")

    ax.set_ylim(0, max_val * 1.18)
    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    ax.set_ylabel("Total Degree Cost ($1,000 USD)" if lang == "en" else "Gesamte Studienkosten (Tsd. USD)", fontsize=8.5 if not is_standalone else 11)

    title_en = (
        f"Panel G: Total Degree Investment ({cohort_tag})\n"
        f"(Tuition, Living Costs & Median Degree Duration)"
    )
    title_de = (
        f"Panel G: Gesamte Studieninvestition ({cohort_tag_de})\n"
        f"(Studiengebühren, Lebenshaltung & Median-Studiendauer)"
    )
    ax.set_title(title_en if lang == "en" else title_de, fontsize=9.2 if not is_standalone else 12.5, fontweight="bold", pad=6)
    ax.legend(fontsize=6.8 if not is_standalone else 9, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_g_v2(ax, data, lang="en", is_standalone=False):
    """Panel G (v2): Master's Domestic / In-State Local Tuition Upfront Investment."""
    render_panel_g(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Master", tuition_mode="local")


def render_panel_g_bachelors(ax, data, lang="en", is_standalone=False):
    """Panel G (v3): Bachelor's International Tuition Upfront Investment."""
    render_panel_g(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Bachelor", tuition_mode="intl")


def render_panel_g_bachelors_v2(ax, data, lang="en", is_standalone=False):
    """Panel G (v4): Bachelor's Domestic / In-State Local Tuition Upfront Investment."""
    render_panel_g(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Bachelor", tuition_mode="local")


def render_panel_h(ax, data, lang="en", is_standalone=False, degree_level="Master"):
    """Panel H: Career Outcome Salaries at Year 1, Year 10, and Year 20 (Nominal USD vs. Year 20 PPP Int'l $)."""
    if degree_level == "Master":
        col_y1_med = "year1_median_salary_usd"
        col_y10_nom = "year10_median_salary_usd"
        col_y20_nom = "year20_median_salary_usd"
        col_y20_ppp = "year20_median_salary_ppp"
        deg_label = "Master's" if lang == "en" else "Master"
    else:
        col_y1_med = "bachelors_year1_median_salary_usd"
        col_y10_nom = "bachelors_year10_median_salary_usd"
        col_y20_nom = "bachelors_year20_median_salary_usd"
        col_y20_ppp = "bachelors_year20_median_salary_ppp"
        deg_label = "Bachelor's" if lang == "en" else "Bachelor"

    df = data["master"].sort_values(col_y20_nom, ascending=False)
    x = np.arange(len(df))
    width = 0.20

    y1_med = df[col_y1_med].values / 1000.0
    y10_nom = df[col_y10_nom].values / 1000.0
    y20_nom = df[col_y20_nom].values / 1000.0
    y20_ppp = df[col_y20_ppp].values / 1000.0

    lbl_y1_nom = "Year 1 Starting (Nominal USD)" if lang == "en" else "Jahr 1 Einstieg (Nominal USD)"
    lbl_y10_nom = "Year 10 Mid-Career (Nominal USD)" if lang == "en" else "Jahr 10 Berufserf. (Nominal USD)"
    lbl_y20_nom = "Year 20 Senior (Nominal USD)" if lang == "en" else "Jahr 20 Senior (Nominal USD)"
    lbl_y20_ppp = "Year 20 Senior (PPP Int'l $)" if lang == "en" else "Jahr 20 Senior (KKP Int'l $)"

    ax.bar(x - 1.5 * width, y1_med, width, label=lbl_y1_nom, color="#1F407A", alpha=0.90)
    ax.bar(x - 0.5 * width, y10_nom, width, label=lbl_y10_nom, color="#E67E22", alpha=0.90)
    ax.bar(x + 0.5 * width, y20_nom, width, label=lbl_y20_nom, color="#D9534F", alpha=0.92)
    ax.bar(x + 1.5 * width, y20_ppp, width, label=lbl_y20_ppp, color="#008080", alpha=0.95)

    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ") for u in df["university_id"]], rotation=30, ha="right", fontsize=7.5 if not is_standalone else 10)
    max_y = max(float(np.max(y20_ppp)), float(np.max(y20_nom)))
    ax.set_ylim(0, max_y * 1.28)
    ax.set_ylabel("Annual Salary (1,000 USD / Int'l $)" if lang == "en" else "Jahresgehalt (Tsd. USD / KKP $)", fontsize=8.5 if not is_standalone else 11)
    title_en = (
        f"Panel H: {deg_label} Career Salaries (Engineering Cohort)\n"
        f"(Y1 Starting, Y10 Mid-Career & Y20 Senior)"
    )
    title_de = (
        f"Panel H: {deg_label}-Karrieregehälter (Ingenieur-Kohorte)\n"
        f"(J1 Einstieg, J10 Berufserf. & J20 Senior)"
    )
    ax.set_title(title_en if lang == "en" else title_de, fontsize=9.2 if not is_standalone else 12.5, fontweight="bold", pad=6)
    ax.legend(fontsize=6.0 if not is_standalone else 8.2, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_panel_i(ax, data, lang="en", is_standalone=False, degree_level="Master", tuition_mode="intl"):
    """Panel I: 20-Year Post-Graduation Economic ROI Multiple (Excess Wealth / Total Economic Investment)."""
    df_traj = data["trajectories"]
    df_master = data["master"]
    universities = [
        "MIT", "Caltech", "Georgia_Tech",
        "Imperial", "ETH_Zurich", "TUM",
        "Tsinghua", "KAIST", "NTU"
    ]

    col_wealth = "cumulative_wealth_opp_cost_usd" if tuition_mode == "intl" else "cumulative_wealth_local_opp_cost_usd"
    col_cs = "cumulative_wealth_opp_cost_cs_usd" if tuition_mode == "intl" else "cumulative_wealth_local_opp_cost_cs_usd"
    col_mech = "cumulative_wealth_opp_cost_mech_usd" if tuition_mode == "intl" else "cumulative_wealth_local_opp_cost_mech_usd"
    cohort_tag = f"Engineering {degree_level} Intl" if tuition_mode == "intl" else f"Engineering {degree_level} Domestic"
    cohort_tag_de = f"Ingenieur-{degree_level} Intl" if tuition_mode == "intl" else f"Ingenieur-{degree_level} Inland"

    styles = {
        "MIT": {"ls": "-", "marker": "o"},
        "Caltech": {"ls": "--", "marker": "s"},
        "Georgia_Tech": {"ls": "-.", "marker": "^"},
        "Imperial": {"ls": "-", "marker": "D"},
        "ETH_Zurich": {"ls": "-", "marker": "v"},
        "TUM": {"ls": "--", "marker": "P"},
        "Tsinghua": {"ls": "-.", "marker": "p"},
        "KAIST": {"ls": ":", "marker": ">"},
        "NTU": {"ls": "-", "marker": "X"},
    }

    y_max_wealth = 2.05
    y_min_wealth = -0.35
    horizon_years = 24 if degree_level == "Bachelor" else 22
    short_grad = 3 if degree_level == "Bachelor" else 1
    long_grad = 4 if degree_level == "Bachelor" else 2
    end_labels = []

    for uid in universities:
        sub = df_traj.loc[(df_traj["university_id"] == uid) & (df_traj["degree_level"] == degree_level)].sort_values("year_since_matriculation")
        x_yrs = np.concatenate([[0.0], sub["year_since_matriculation"].values])

        net_tuition = float(sub["net_tuition_total_usd"].iloc[0] if tuition_mode == "intl" else sub["net_tuition_local_total_usd"].iloc[0])
        foregone_total = float(sub["foregone_earnings_total_usd"].iloc[0])
        econ_inv = net_tuition + foregone_total
        assert econ_inv > 0.0, f"Economic investment must be positive for {uid}"

        wealth_traj = np.concatenate([[0.0], sub[col_wealth].values / 1e6])
        wealth_cs = np.concatenate([[0.0], sub[col_cs].values / 1e6])
        wealth_mech = np.concatenate([[0.0], sub[col_mech].values / 1e6])
        wealth_20y_usd = float(sub[col_wealth].iloc[-1])
        roi_20y = wealth_20y_usd / econ_inv
        if abs(wealth_20y_usd) >= 1e6:
            w_str = f"+${wealth_20y_usd / 1e6:.2f}M"
        else:
            w_str = f"+${wealth_20y_usd / 1e3:.0f}k"

        color = PALETTE_9[uid]
        st = styles[uid]

        end_labels.append({"y": float(wealth_traj[-1]), "txt": w_str, "color": color})

        # Uncertainty band between Mechanical Engineering and CS/AI
        ax.fill_between(x_yrs, wealth_mech, wealth_cs, color=color, alpha=0.07)

        ax.plot(
            x_yrs,
            wealth_traj,
            linestyle=st["ls"],
            marker=st["marker"],
            markersize=3.0 if not is_standalone else 4.5,
            label=f"{uid.replace('_', ' ')} ({roi_20y:.1f}x, {w_str})",
            color=color,
            lw=1.5 if not is_standalone else 1.8,
            alpha=0.90,
        )

    # De-overlap endpoint excess wealth labels at x = horizon_years + 0.25
    end_labels.sort(key=lambda d: d["y"])
    min_gap = 0.085
    for i in range(1, len(end_labels)):
        if end_labels[i]["y"] - end_labels[i - 1]["y"] < min_gap:
            end_labels[i]["y"] = end_labels[i - 1]["y"] + min_gap
    for d in end_labels:
        ax.text(
            horizon_years + 0.25,
            min(d["y"], y_max_wealth - 0.05),
            d["txt"],
            ha="left",
            va="center",
            fontsize=5.0 if not is_standalone else 6.8,
            fontweight="bold",
            color=d["color"],
        )

    ax.axhline(0, color="gray", linestyle="--", alpha=0.6)
    ax.axvspan(0, short_grad, color="lightgray", alpha=0.25,
               label=f"{short_grad}-Yr Study Phase" if lang == "en" else f"{short_grad}-J. Studienphase")
    ax.axvspan(short_grad, long_grad, color="#d9d9d9", alpha=0.35, hatch="///", edgecolor="#b0b0b0",
               label=f"{long_grad}th Study Yr (4-Yr BSc)" if (lang == "en" and degree_level == "Bachelor") else (
                   f"2nd Study Yr (2-Yr MS)" if lang == "en" else f"{long_grad}. Studienjahr"))
    ax.axvline(short_grad, color="#777777", linestyle=":", lw=0.9, alpha=0.7)

    ax.set_xlim(-0.5, horizon_years + 3.3)
    ax.set_ylim(y_min_wealth, y_max_wealth)
    ax.set_xlabel("Years Since Matriculation (Fixed Age Horizon)" if lang == "en" else "Jahre seit Studienbeginn (Fester Altershorizont)", fontsize=8.5 if not is_standalone else 11)
    ax.set_ylabel("Cumulative Excess Wealth ($M USD)" if lang == "en" else "Kumuliertes Mehrvermögen (Mio. USD)", fontsize=8.0 if not is_standalone else 10.5)

    title_en = (
        f"Panel I: {horizon_years}-Year Post-Matriculation Excess Wealth ({cohort_tag})\n"
        f"(Baseline: Associate / Ausbildung / Vocational, Age 20–45)"
    )
    title_de = (
        f"Panel I: {horizon_years}-Jahres-Mehrvermögen ab Studienbeginn ({cohort_tag_de})\n"
        f"(Basis: Ausbildung / Facharbeiter / Associate, Alter 20–45)"
    )
    ax.set_title(title_en if lang == "en" else title_de, fontsize=9.2 if not is_standalone else 12.5, fontweight="bold", pad=6)
    ax.legend(fontsize=5.2 if not is_standalone else 7.5, loc="upper left", ncol=2, framealpha=0.9)
    ax.grid(True, linestyle="--", alpha=0.3)


def render_panel_i_v2(ax, data, lang="en", is_standalone=False):
    """Panel I (v2): Master's Domestic / In-State Local Tuition Cumulative Net Wealth Trajectories."""
    render_panel_i(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Master", tuition_mode="local")


def render_panel_i_bachelors(ax, data, lang="en", is_standalone=False):
    """Panel I (v3): Bachelor's International Tuition Cumulative Net Wealth Trajectories."""
    render_panel_i(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Bachelor", tuition_mode="intl")


def render_panel_i_bachelors_v2(ax, data, lang="en", is_standalone=False):
    """Panel I (v4): Bachelor's Domestic / In-State Local Tuition Cumulative Net Wealth Trajectories."""
    render_panel_i(ax, data, lang=lang, is_standalone=is_standalone, degree_level="Bachelor", tuition_mode="local")


def render_waterfall_decomposition(ax, data, lang="en", is_standalone=False):
    """Auxiliary Panel: Sequential Waterfall with Path-Independent Shapley Value Decomposition."""
    waterfall = compute_shapley_waterfall_decomposition(data["master"], data["benchmarks"])
    steps = waterfall["canonical_steps"]

    deltas = [s[1] / 1000.0 for s in steps]
    totals = [s[2] / 1000.0 for s in steps]
    shapleys = [s[3] / 1000.0 for s in steps]

    x = np.arange(len(steps))
    bottoms = [0.0]
    for i in range(1, len(steps)):
        if i == len(steps) - 1:
            bottoms.append(0.0)
        else:
            prev_tot = totals[i-1]
            d = deltas[i]
            bottoms.append(prev_tot if d > 0 else prev_tot + d)

    bar_heights = [totals[0]] + [abs(d) for d in deltas[1:-1]] + [totals[-1]]
    bar_colors = ["#A31F34"] + ["#0065BD" if d < 0 else "#D9534F" for d in deltas[1:-1]] + ["#008080"]

    bars = ax.bar(x, bar_heights, bottom=bottoms, color=bar_colors, width=0.55, alpha=0.90)

    for i, b in enumerate(bars):
        if i == 0 or i == len(steps) - 1:
            val = totals[i]
            ax.text(b.get_x() + b.get_width()/2.0, b.get_y() + b.get_height() + 8.0, f"${val:.0f}k", ha="center", fontsize=6.5 if not is_standalone else 8.5, fontweight="bold")
        else:
            d_val = deltas[i]
            sh_val = shapleys[i]
            sign = "+" if d_val > 0 else ""
            sh_sign = "+" if sh_val > 0 else ""
            ax.text(b.get_x() + b.get_width()/2.0, b.get_y() + b.get_height() + 8.0, f"{sign}{d_val:.0f}k\n(φ={sh_sign}{sh_val:.0f}k)", ha="center", fontsize=5.8 if not is_standalone else 7.8)

    short_labels = [
        "Raw Disparity\n(Headline)",
        "Strip FFRDC\n(JPL/Lincoln)",
        "Strip Hospital\n(Klinikum)",
        "Add Campus\nEcosystems",
        "PPP Deflator\n(Purchasing Power)",
        "FTE Scale\n(Final Tier 2)",
    ] if lang == "en" else [
        "Brutto-Kluft\n(Headline)",
        "Minus FFRDC\n(JPL/Lincoln)",
        "Minus Klinik\n(Klinikum)",
        "Plus Campus\nÖkosysteme",
        "KKP-Deflator\n(Kaufkraft)",
        "FTE-Skalierung\n(Endstand Tier 2)",
    ]

    ax.set_xticks(x)
    ax.set_xticklabels(short_labels, rotation=25, ha="right", fontsize=7.5 if not is_standalone else 9.5)
    ax.set_ylabel("Funding Disparity ($1,000 USD / Student)" if lang == "en" else "Finanzierungsdisparität (Tsd. $ / Stud.)", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("Shapley Waterfall Decomposition (US Private vs TUM)" if lang == "en" else "Shapley-Waterfall-Zerlegung (US-Privat vs. TUM)", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.grid(axis="y", linestyle="--", alpha=0.3)


def render_historical_trajectories(ax, data, lang="en", is_standalone=False):
    """Auxiliary Panel: 15-Year Longitudinal Real Core Budget per FTE (Index 2010=100)."""
    df_hist = data["historical"]
    for uid in PALETTE_9.keys():
        sub = df_hist.loc[df_hist["university_id"] == uid].sort_values("year")
        if len(sub) == 0:
            continue
        color = PALETTE_9[uid]
        ax.plot(
            sub["year"].values,
            sub["budget_per_fte_index_2010"].values,
            marker="o",
            markersize=3.5 if not is_standalone else 5.0,
            label=uid.replace("_", " "),
            color=color,
            lw=1.5 if not is_standalone else 1.8,
            alpha=0.90,
        )

    ax.axhline(100.0, color="gray", linestyle="--", alpha=0.5, label="2010 Parity Base (100.0)" if lang == "en" else "Basislinie 2010 (100.0)")
    ax.set_xlabel("Year" if lang == "en" else "Jahr", fontsize=8.5 if not is_standalone else 11)
    ax.set_ylabel("Real Budget per FTE Index (2010 = 100)" if lang == "en" else "Reales Budget pro FTE Index (2010 = 100)", fontsize=8.5 if not is_standalone else 11)
    ax.set_title("15-Year Longitudinal Trajectory: Real Budget per FTE (2010–2024)" if lang == "en" else "15-Jahre-Entwicklung: Reales Budget pro FTE (2010–2024)", fontsize=10 if not is_standalone else 13, fontweight="bold", pad=7)
    ax.legend(fontsize=6.0 if not is_standalone else 8.0, ncol=2, loc="upper left", framealpha=0.9)
    ax.grid(True, linestyle="--", alpha=0.3)


# ==============================================================================
# BOTTOM-ROW 4-VARIANT COMPARISON & 3x3 SYNOPTIC MATRICES
# ==============================================================================

def generate_bottom_row_4_variants_comparison(data, lang="en"):
    """Generate 4-row comparative composite of Panels G, H, I across Master & Bachelor x Native & Non-Native."""
    fig, axes = plt.subplots(4, 3, figsize=(19, 21), dpi=300)
    fig.subplots_adjust(top=0.93, bottom=0.055, left=0.08, right=0.97, hspace=0.44, wspace=0.26)

    suptitle_bot = (
        "Global Technical Universities (2024/2025): 4-Cohort Degree Cost, Career Salary & 20-Year ROI Comparison\n"
        "Master's & Bachelor's Degrees × International (Non-Native) & Domestic (In-State / Native) Tuition Regimes"
    ) if lang == "en" else (
        "Technische Universitäten Weltweit (2024/2025): 4-Kohorten-Vergleich zu Studienkosten, Gehalt & 20-Jahres-ROI\n"
        "Master- & Bachelor-Abschlüsse × Internationale (Nicht-Einheimische) & Inländische (Einheimische / In-State) Gebühren"
    )
    fig.suptitle(suptitle_bot, y=0.976, fontsize=14, fontweight="bold", color="#111111", linespacing=1.35)

    # Variant 1: Master's Degree – International (Non-Native)
    render_panel_g(axes[0, 0], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="intl")
    render_panel_h(axes[0, 1], data, lang=lang, is_standalone=False, degree_level="Master")
    render_panel_i(axes[0, 2], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="intl")

    # Variant 2: Master's Degree – Domestic / In-State (Native)
    render_panel_g(axes[1, 0], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="local")
    render_panel_h(axes[1, 1], data, lang=lang, is_standalone=False, degree_level="Master")
    render_panel_i(axes[1, 2], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="local")

    # Variant 3: Bachelor's Degree – International (Non-Native)
    render_panel_g(axes[2, 0], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode="intl")
    render_panel_h(axes[2, 1], data, lang=lang, is_standalone=False, degree_level="Bachelor")
    render_panel_i(axes[2, 2], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode="intl")

    # Variant 4: Bachelor's Degree – Domestic / In-State (Native)
    render_panel_g(axes[3, 0], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode="local")
    render_panel_h(axes[3, 1], data, lang=lang, is_standalone=False, degree_level="Bachelor")
    render_panel_i(axes[3, 2], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode="local")

    row_labels = [
        "Cohort 1: Master's Non-Native (International)",
        "Cohort 2: Master's Native (Domestic / In-State)",
        "Cohort 3: Bachelor's Non-Native (International)",
        "Cohort 4: Bachelor's Native (Domestic / In-State)",
    ] if lang == "en" else [
        "Kohorte 1: Master Nicht-Einheimisch (International)",
        "Kohorte 2: Master Einheimisch (Inland / In-State)",
        "Kohorte 3: Bachelor Nicht-Einheimisch (International)",
        "Kohorte 4: Bachelor Einheimisch (Inland / In-State)",
    ]

    for row_idx, r_label in enumerate(row_labels):
        axes[row_idx, 0].annotate(r_label, xy=(0, 0.5), xytext=(-axes[row_idx, 0].yaxis.labelpad - 58, 0),
                                  xycoords='axes fraction', textcoords='offset points',
                                  size=10, weight='bold', rotation=90, ha='center', va='center',
                                  color="#1F407A")

    footnote_bottom = (
        "Sources: Tuition, Assistantship & Aid Schedules (MIT OGE/RAS, Caltech, Georgia Tech GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024/25; US IPEDS);\n"
        "Career & Age-20–45 No-College Wage Registries: US NSF NSCG / BLS CPS / Payscale / College Scorecard; UK DfE LEO / IFS RR1642 / ONS ASHE;\n"
        "Swiss BFS LSE 2024 / KOF Study 152 / STV; German BA Entgeltatlas / Destatis / VDI; China NBS / Beijing HRSS / NBER WP 29523; Korea MOEL / KOSTAT / STEPI; Singapore MOM CLFS 2025 / MOE GES."
    ) if lang == "en" else (
        "Quellen: Studiengebühren-, HiWi- & Förderstatistiken (MIT OGE/RAS, Caltech, Georgia Tech GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024/25; US IPEDS);\n"
        "Karriere- & Nicht-Akademiker-Lohnregister (20–45 J.): US NSF NSCG / BLS CPS / Payscale / College Scorecard; UK DfE LEO / IFS RR1642 / ONS ASHE;\n"
        "BFS LSE 2024 / KOF-Studie 152 / STV; BA Entgeltatlas / Destatis / VDI; China NBS / Beijing HRSS / NBER WP 29523; Korea MOEL / KOSTAT / STEPI; Singapur MOM CLFS 2025 / MOE GES."
    )
    plt.figtext(0.5, 0.004, footnote_bottom, ha="center", fontsize=7.2, color="#555555", style="italic")

    out_file = os.path.join(PLOTS_DIR, f"bottom_row_4_variants_comparison_{lang}.png")
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    if lang == "en":
        shutil.copyfile(out_file, os.path.join(PLOTS_DIR, "bottom_row_4_variants_comparison.png"))
    print(f"✓ Saved 4-Variant Bottom-Row Composite: {os.path.basename(out_file)}")


def generate_composite_3x3_matrix(data, lang="en", edition="v1"):
    """Generate the full publication-grade 9-panel (3x3) synoptic matrix across 4 editions.

    Editions:
    - v1: Master's International (Non-Native)
    - v2: Master's Domestic / In-State (Native)
    - v3: Bachelor's International (Non-Native)
    - v4: Bachelor's Domestic / In-State (Native)
    """
    deg_level = "Master" if edition in ["v1", "v2"] else "Bachelor"
    t_mode = "intl" if edition in ["v1", "v3"] else "local"

    fig, axes = plt.subplots(3, 3, figsize=(19, 16.5), dpi=300)
    fig.subplots_adjust(top=0.915, bottom=0.06, left=0.06, right=0.97, hspace=0.46, wspace=0.28)

    render_panel_a(axes[0, 0], data, lang=lang, is_standalone=False)
    render_panel_b(axes[0, 1], data, lang=lang, is_standalone=False)
    render_panel_c(axes[0, 2], data, lang=lang, is_standalone=False)

    render_panel_d(axes[1, 0], data, lang=lang, is_standalone=False)
    render_panel_e(axes[1, 1], data, lang=lang, is_standalone=False)
    render_panel_f(axes[1, 2], data, lang=lang, is_standalone=False)

    render_panel_g(axes[2, 0], data, lang=lang, is_standalone=False, degree_level=deg_level, tuition_mode=t_mode)
    render_panel_h(axes[2, 1], data, lang=lang, is_standalone=False, degree_level=deg_level)
    render_panel_i(axes[2, 2], data, lang=lang, is_standalone=False, degree_level=deg_level, tuition_mode=t_mode)

    edition_desc_en = {
        "v1": "v1 Master's Non-Native (International)",
        "v2": "v2 Master's Native (Domestic / In-State)",
        "v3": "v3 Bachelor's Non-Native (International)",
        "v4": "v4 Bachelor's Native (Domestic / In-State)",
    }[edition]

    edition_desc_de = {
        "v1": "v1 Master International (Nicht-Einheimisch)",
        "v2": "v2 Master Inland (Einheimisch / In-State)",
        "v3": "v3 Bachelor International (Nicht-Einheimisch)",
        "v4": "v4 Bachelor Inland (Einheimisch / In-State)",
    }[edition]

    suptitle_3x3 = (
        "Global Technical Universities Benchmark (2024/2025): Budgets, Research Efficiency & 20-Year Career ROI\n"
        f"MIT • Caltech • Georgia Tech • Imperial • ETH Zurich • TUM • Tsinghua • KAIST • NTU Singapore  [{edition_desc_en}]"
    ) if lang == "en" else (
        "Globaler Vergleich Technischer Universitäten (2024/2025): Budgets, Forschungseffizienz & 20-Jahres-Karriere-ROI\n"
        f"MIT • Caltech • Georgia Tech • Imperial • ETH Zürich • TUM • Tsinghua • KAIST • NTU Singapur  [{edition_desc_de}]"
    )
    fig.suptitle(suptitle_3x3, y=0.972, fontsize=14, fontweight="bold", color="#111111", linespacing=1.35)

    footnote = (
        f"Sources: Audited Financial Statements & Aid/HiWi Schedules (MIT OGE/RAS, Caltech, GT GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024); Partner Institutes; "
        f"World Bank ICP (PA.NUS.PPP); Rankings & Bibliometrics (QS 2025, THE 2025, ARWU 2024, US News 2025, GEURS 2025, CWTS Leiden 2024);\n"
        f"Admissions & 1-Yr Attrition (US CDS, UCAS/HESA, BFS/ETH Rectorate, TUM EFV); Career & Age-20–45 No-College Wage Registries (US NSF NSCG/BLS/Payscale, UK DfE LEO/IFS RR1642/ONS ASHE, "
        f"Swiss BFS LSE/KOF 152, German BA Entgeltatlas/Destatis, China NBS/Beijing HRSS/NBER WP29523, Korea MOEL/KOSTAT/STEPI, Singapore MOM CLFS/MOE GES) [{edition_desc_en}]."
    ) if lang == "en" else (
        f"Quellen: Geprüfte Jahresabschlüsse & Förder-/HiWi-Statistiken (MIT OGE/RAS, Caltech, GT GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024); Partnerinstitute; "
        f"Weltbank KKP (PA.NUS.PPP); Rankings & Bibliometrie (QS 2025, THE 2025, ARWU 2024, US News 2025, GEURS 2025, CWTS Leiden 2024);\n"
        f"Zulassung & 1.-Jahr-Abbruch (US CDS, UCAS/HESA, BFS/ETH-Rektorat, TUM EFV); Karriere- & Nicht-Akademiker-Lohnregister 20–45 J. (US NSF NSCG/BLS/Payscale, UK DfE LEO/IFS RR1642/ONS ASHE, "
        f"BFS LSE/KOF 152, BA Entgeltatlas/Destatis, China NBS/Beijing HRSS/NBER WP29523, Korea MOEL/KOSTAT/STEPI, Singapur MOM CLFS/MOE GES) [{edition_desc_de}]."
    )
    plt.figtext(0.5, 0.012, footnote, ha="center", fontsize=7.0, color="#555555", style="italic")

    out_file = os.path.join(PLOTS_DIR, f"technical_universities_3x3_{edition}_{lang}.png")
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()

    # Synchronize default baseline filenames with v1
    if edition == "v1":
        base_file = os.path.join(PLOTS_DIR, f"technical_universities_3x3_{lang}.png")
        shutil.copyfile(out_file, base_file)
    print(f"✓ Saved 3x3 Synoptic Matrix: {os.path.basename(out_file)}")


def generate_composite_4x3_matrix(data, lang="en", bachelor_mode="intl"):
    """Generate the full publication-grade 12-panel (4x3) synoptic matrix.

    Layout:
    - Row 1: Panels A, B, C (Macro Budgets, Scale, Supervision & Resources per FTE)
    - Row 2: Panels D, E, F (Rankings Profile, Research Efficiency, 2D Production Frontier)
    - Row 3: Bachelor's Degree Lifecycle (Panels G, H, I for Bachelor)
    - Row 4: Master's Domestic Lifecycle (Panels G, H, I for Master Domestic)
    """
    b_tuition_mode = "intl" if bachelor_mode == "intl" else "local"

    fig, axes = plt.subplots(4, 3, figsize=(19, 21.5), dpi=300)
    fig.subplots_adjust(top=0.93, bottom=0.055, left=0.06, right=0.97, hspace=0.46, wspace=0.28)

    # Row 1: Macro Budgets & Denominators
    render_panel_a(axes[0, 0], data, lang=lang, is_standalone=False)
    render_panel_b(axes[0, 1], data, lang=lang, is_standalone=False)
    render_panel_c(axes[0, 2], data, lang=lang, is_standalone=False)

    # Row 2: Research Quality & Rankings
    render_panel_d(axes[1, 0], data, lang=lang, is_standalone=False)
    render_panel_e(axes[1, 1], data, lang=lang, is_standalone=False)
    render_panel_f(axes[1, 2], data, lang=lang, is_standalone=False)

    # Row 3: Bachelor's Degree Lifecycle
    render_panel_g(axes[2, 0], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode=b_tuition_mode)
    render_panel_h(axes[2, 1], data, lang=lang, is_standalone=False, degree_level="Bachelor")
    render_panel_i(axes[2, 2], data, lang=lang, is_standalone=False, degree_level="Bachelor", tuition_mode=b_tuition_mode)

    # Row 4: Master's Domestic Lifecycle
    render_panel_g(axes[3, 0], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="local")
    render_panel_h(axes[3, 1], data, lang=lang, is_standalone=False, degree_level="Master")
    render_panel_i(axes[3, 2], data, lang=lang, is_standalone=False, degree_level="Master", tuition_mode="local")

    b_label = "International" if bachelor_mode == "intl" else "Domestic"
    b_label_de = "International" if bachelor_mode == "intl" else "Inland"

    suptitle_4x3 = (
        "Global Technical Universities Benchmark (2024/2025): Budgets, Research Efficiency & Dual-Cohort 20-Year Career ROI\n"
        f"MIT • Caltech • Georgia Tech • Imperial • ETH Zurich • TUM • Tsinghua • KAIST • NTU Singapore  [Bachelor ({b_label}) & Master Domestic]"
    ) if lang == "en" else (
        "Globaler Vergleich Technischer Universitäten (2024/2025): Budgets, Forschungseffizienz & 20-Jahres-Karriere-ROI\n"
        f"MIT • Caltech • Georgia Tech • Imperial • ETH Zürich • TUM • Tsinghua • KAIST • NTU Singapur  [Bachelor ({b_label_de}) & Master Inland]"
    )
    fig.suptitle(suptitle_4x3, y=0.976, fontsize=14, fontweight="bold", color="#111111", linespacing=1.35)

    footnote = (
        f"Sources: Audited Financial Statements & Aid/HiWi Schedules (MIT OGE/RAS, Caltech, GT GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024); Partner Institutes; "
        f"World Bank ICP (PA.NUS.PPP); Rankings & Bibliometrics (QS 2025, THE 2025, ARWU 2024, US News 2025, GEURS 2025, CWTS Leiden 2024);\n"
        f"Admissions & 1-Yr Attrition (US CDS, UCAS/HESA, BFS/ETH Rectorate, TUM EFV); Career & Age-20–45 No-College Wage Registries (US NSF NSCG/BLS/Payscale, UK DfE LEO/IFS RR1642/ONS ASHE, "
        f"Swiss BFS LSE/KOF 152, German BA Entgeltatlas/Destatis, China NBS/Beijing HRSS/NBER WP29523, Korea MOEL/KOSTAT/STEPI, Singapore MOM CLFS/MOE GES) "
        f"[4x3 Synoptic Matrix: Bachelor ({b_label}) & Master Domestic]."
    ) if lang == "en" else (
        f"Quellen: Geprüfte Jahresabschlüsse & Förder-/HiWi-Statistiken (MIT OGE/RAS, Caltech, GT GRA/GTA, Imperial Bursary, ETH Hilfsassistierende, TUM HiWi/DZHW 22. Sozialerhebung, Tsinghua, KAIST, NTU 2024); Partnerinstitute; "
        f"Weltbank KKP (PA.NUS.PPP); Rankings & Bibliometrie (QS 2025, THE 2025, ARWU 2024, US News 2025, GEURS 2025, CWTS Leiden 2024);\n"
        f"Zulassung & 1.-Jahr-Abbruch (US CDS, UCAS/HESA, BFS/ETH-Rektorat, TUM EFV); Karriere- & Nicht-Akademiker-Lohnregister 20–45 J. (US NSF NSCG/BLS/Payscale, UK DfE LEO/IFS RR1642/ONS ASHE, "
        f"BFS LSE/KOF 152, BA Entgeltatlas/Destatis, China NBS/Beijing HRSS/NBER WP29523, Korea MOEL/KOSTAT/STEPI, Singapur MOM CLFS/MOE GES) "
        f"[4x3 Synoptische Gesamtmatrix: Bachelor ({b_label_de}) & Master Inland]."
    )
    plt.figtext(0.5, 0.004, footnote, ha="center", fontsize=7.0, color="#555555", style="italic")

    suffix = "" if bachelor_mode == "intl" else "_domestic"
    out_file = os.path.join(PLOTS_DIR, f"technical_universities_4x3{suffix}_{lang}.png")
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    if lang == "en" and bachelor_mode == "intl":
        shutil.copyfile(out_file, os.path.join(PLOTS_DIR, "technical_universities_4x3.png"))
    print(f"✓ Saved 4x3 Synoptic Matrix: {os.path.basename(out_file)}")


def generate_standalone_panels(data):
    """Generate high-resolution standalone PNGs for Panels A through I, dual profiles, and waterfall."""
    panels = [
        ("panel_a_budget_tiers_ppp.png", render_panel_a),
        ("panel_b_enrollment_fte_supervision.png", render_panel_b),
        ("panel_c_student_facing_budget_per_fte.png", render_panel_c),
        ("panel_d_rankings_employability_profile.png", render_panel_d),
        ("panel_e_research_efficiency_multidim.png", render_panel_e),
        ("panel_f_2d_efficiency_frontier_surface.png", render_panel_f),
        ("panel_g_masters_cost_lifecycle.png", render_panel_g),
        ("panel_g_masters_cost_lifecycle_v2.png", render_panel_g_v2),
        ("panel_g_bachelors_cost_lifecycle.png", render_panel_g_bachelors),
        ("panel_g_bachelors_cost_lifecycle_v2.png", render_panel_g_bachelors_v2),
        ("panel_h_career_outcome_salaries.png", render_panel_h),
        ("panel_h_career_outcome_salaries_bachelors.png", lambda ax, d, lang, is_standalone: render_panel_h(ax, d, lang=lang, is_standalone=is_standalone, degree_level="Bachelor")),
        ("panel_i_10y_salary_roi_trajectories.png", render_panel_i),
        ("panel_i_10y_salary_roi_trajectories_v2.png", render_panel_i_v2),
        ("panel_i_10y_salary_roi_trajectories_bachelors.png", render_panel_i_bachelors),
        ("panel_i_10y_salary_roi_trajectories_bachelors_v2.png", render_panel_i_bachelors_v2),
        ("panel_shapley_waterfall_decomposition.png", render_waterfall_decomposition),
        ("panel_historical_panel_trajectories.png", render_historical_trajectories),
    ]

    for fname, renderer in panels:
        if fname == "panel_d_rankings_employability_profile.png":
            fig = plt.figure(figsize=(16, 6.2), dpi=300)
            render_panel_d_dual(fig, data, lang="en")
            out_path = os.path.join(PLOTS_DIR, fname)
            plt.savefig(out_path, dpi=300, bbox_inches="tight")
            plt.close()
            print(f"✓ Saved Standalone Panel: {fname} (Dual-Subplot Multi-Ranking Architecture)")
            continue

        fig, ax = plt.subplots(figsize=(8.5, 5.8), dpi=300)
        renderer(ax, data, lang="en", is_standalone=True)
        out_path = os.path.join(PLOTS_DIR, fname)
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"✓ Saved Standalone Panel: {fname}")


def main():
    print("=" * 60)
    print("MODELING & SYNOPTIC VISUALIZATION: 9 TECHNICAL UNIVERSITIES")
    print("=" * 60)
    os.makedirs(PLOTS_DIR, exist_ok=True)

    data = load_datasets_and_benchmarks()
    generate_standalone_panels(data)

    # Generate 4-variant bottom row comparison
    generate_bottom_row_4_variants_comparison(data, lang="en")
    generate_bottom_row_4_variants_comparison(data, lang="de")

    # Generate 4 editions of the 3x3 Synoptic Matrix (EN and DE)
    for ed in ["v1", "v2", "v3", "v4"]:
        generate_composite_3x3_matrix(data, lang="en", edition=ed)
        generate_composite_3x3_matrix(data, lang="de", edition=ed)

    # Generate 4x3 Synoptic Matrix (EN and DE)
    generate_composite_4x3_matrix(data, lang="en", bachelor_mode="intl")
    generate_composite_4x3_matrix(data, lang="de", bachelor_mode="intl")
    generate_composite_4x3_matrix(data, lang="en", bachelor_mode="domestic")
    generate_composite_4x3_matrix(data, lang="de", bachelor_mode="domestic")

    print("=" * 60)
    print("ALL FIGURES DETERMINISTICALLY GENERATED IN plots/")
    print("=" * 60)


if __name__ == "__main__":
    main()
