import os
from datetime import datetime
from scipy.stats import pearsonr
from scipy.stats import linregress
import json


# Column names
DROPOUT_COL = "% Abandonament a primer curs"
PERFORMANCE_COL = "Taxa rendiment"
ACADEMIC_YEAR_COL = "Curs Acadèmic"
BRANCH_COL = "Branca"


def analyze_dataset(df, output_path="analisi_estadistic.json"):
    # output folder
    report_dir = "src/report"
    os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(report_dir, output_path)

    # --------------
    # 4.1. Metadata
    # --------------
    print("\n-- Generating metadata... --")
    metadata = build_metadata(df)
    
    # -----------------------
    # 4.2. Global statistics
    # -----------------------
    print("\n-- Generating global statistics... --")
    global_statistics = build_global_statistics(df)
    
    # -----------------------
    # 4.3 Analysis by branch
    # -----------------------
    print("\n-- Generating the branch analysis... --")
    branch_analysis = build_branch_analysis(df)

    print("\n-- Generating the JSON... --")
    analysis = {
        "metadata": metadata,
        "global_statistics": global_statistics,
        "analysis_by_branch": branch_analysis
    }

    print("\n-- Writing the file... --")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)

    return analysis


def build_metadata(df):
    return {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "num_records": int(len(df)),
        "time_period": sorted(df["Curs Acadèmic"].unique())
    }


def build_global_statistics(df):
    dropout_data = df[DROPOUT_COL]
    dropout_mean = round(dropout_data.mean(), 2)
    performance_data = df[PERFORMANCE_COL]
    performance_mean = round(df[PERFORMANCE_COL].mean(), 2)
    corr_val, _ = pearsonr(
            dropout_data.dropna(), 
            performance_data.dropna()
        )
    return {
        "dropout_mean": dropout_mean,
        "performance_mean": performance_mean,
        "dropout_performance_correlation": round(corr_val, 2)
    }


def build_branch_analysis(df):
    branch_analysis = {}
    branches = df[BRANCH_COL].unique()
    # group the data by academic year for each branch
    for branch in branches:
        # filter for the current branch
        branch_data = df[df[BRANCH_COL] == branch]
        branch_analysis[branch] = build_branch_data(branch_data)
    return branch_analysis


def build_branch_data(branch_data):
    # statistics data
    dropout_data = branch_data[DROPOUT_COL]
    dropout_mean_branch = round(dropout_data.mean(), 2)
    dropout_std_branch = round(dropout_data.std(), 2)
    dropout_min_branch = round(dropout_data.min(), 2)
    dropout_max_branch = round(dropout_data.max(), 2)

    performance_data = branch_data[PERFORMANCE_COL]
    performance_mean_branch = round(performance_data.mean(), 2)
    performance_std_branch = round(performance_data.std(), 2)
    performance_min_branch = round(performance_data.min(), 2)
    performance_max_branch = round(performance_data.max(), 2)

    # dropout trend group by year
    branch_by_year = branch_data.groupby(ACADEMIC_YEAR_COL).agg({
        DROPOUT_COL: "mean"
    }).reset_index()
    years = branch_by_year[ACADEMIC_YEAR_COL].tolist()

    dropout_by_year =  branch_by_year[DROPOUT_COL].tolist()

    # linear regression to detect trend
    slope_dropout, _, _, _, _ = linregress(
        range(len(years)),  # Positions: 0, 1, 2, 3...
        dropout_by_year
    )

    # interpretation of the slope
    if slope_dropout > 0.01:
        dropout_trend = "increasing"
    elif slope_dropout < -0.01:
        dropout_trend = "decreasing"
    else:
        dropout_trend = "stable"

    # performance trend group by year
    branch_by_year = branch_data.groupby(ACADEMIC_YEAR_COL).agg({
        PERFORMANCE_COL: "mean"
    }).reset_index()
    years = branch_by_year[ACADEMIC_YEAR_COL].tolist()

    performance_by_year =  branch_by_year[PERFORMANCE_COL].tolist()

    # linear regression to performance trend
    slope_perf, _, _, _, _ = linregress(
        range(len(years)),  # Positions: 0, 1, 2, 3...
        performance_by_year
    )

    # interpretation of the slope
    if slope_perf > 0.01:
        perf_trend = "increasing"
    elif slope_perf < -0.01:
        perf_trend = "decreasing"
    else:
        perf_trend = "stable"

    return {
        "dropout_mean": dropout_mean_branch,
        "dropout_std": dropout_std_branch,
        "dropout_min": dropout_min_branch,
        "dropout_max": dropout_max_branch,
        "performance_mean": performance_mean_branch,
        "performance_std": performance_std_branch,
        "performance_min": performance_min_branch,
        "performance_max": performance_max_branch,
        "dropout_trend": dropout_trend,
        "performance_trend": perf_trend
    }