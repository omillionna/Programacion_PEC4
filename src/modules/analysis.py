"""
statistical_analysis.py

This module performs the statistical analysis required in Exercise 4 of the PEC.
It generates metadata, global statistics, analysis by study branch, rankings of
branches, and exports all results into a JSON report file.
"""
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
    """
    Runs the complete statistical analysis of the merged dataset and exports
    the results to a JSON file.

    It includes:
        - Metadata generation.
        - Global statistics.
        - Analysis by study branch.
        - Branch rankings.

    Parameters:
        df (pandas.DataFrame): Merged dataset.
        output_path (str): Name of the JSON file to be created.

    Returns:
        dict: Dictionary containing all the analysis results.
    """
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

    # -----------------------
    # 4.4 Branch ranking
    # -----------------------

    print("\n-- Generating the branch ranking... --")
    branch_ranking = build_branch_ranking(df)

    print("\n-- Generating the JSON... --")
    analysis = {
        "metadata": metadata,
        "global_statistics": global_statistics,
        "analysis_by_branch": branch_analysis,
        "ranking_branches": branch_ranking
    }
    
    print("\n-- Writing the file... --")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)

    return analysis


def build_metadata(df):
    """
    Builds basic metadata information of the dataset.

    Parameters:
        df (pandas.DataFrame)

    Returns:
        dict: Metadata including current date, number of records and time period.
    """
    return {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "num_records": int(len(df)),
        "time_period": sorted(df[ACADEMIC_YEAR_COL].unique())
    }


def build_global_statistics(df):
    """
    Computes global statistics for the dataset, including:
        - Mean dropout rate.
        - Mean performance rate.
        - Correlation between dropout and performance.

    Parameters:
        df (pandas.DataFrame)

    Returns:
        dict: Global statistical indicators.
    """
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
    """
    Performs a statistical analysis for each study branch.

    For every branch, it computes descriptive statistics and trend analysis
    for both dropout rate and performance rate.

    Parameters:
        df (pandas.DataFrame)

    Returns:
        dict: Analysis results indexed by branch name.
    """
    branch_analysis = {}
    branches = df[BRANCH_COL].unique()
    # group the data by academic year for each branch
    for branch in branches:
        # filter for the current branch
        branch_data = df[df[BRANCH_COL] == branch]
        branch_analysis[branch] = build_branch_data(branch_data)
    return branch_analysis


def build_branch_data(branch_data):
    """
    Computes statistics and trends for a single study branch.

    Parameters:
        branch_data (pandas.DataFrame): Data corresponding to one branch.

    Returns:
        dict: Statistical indicators and trends for the branch.
    """
    # statistics data
    basic_stats_dropout = calculate_basic_stats(branch_data[DROPOUT_COL], "dropout")
    basic_stats_perf = calculate_basic_stats(branch_data[PERFORMANCE_COL], "performance")

    # linear regression to detect trend
    branch_by_year_drop = branch_data.groupby(ACADEMIC_YEAR_COL).agg({
        DROPOUT_COL: 'mean'
    }).reset_index()
    dropout_trend = calculate_trend(branch_by_year_drop[DROPOUT_COL].tolist())

    # linear regression to performance trend
    branch_by_year_perf = branch_data.groupby(ACADEMIC_YEAR_COL).agg({
        PERFORMANCE_COL: 'mean'
    }).reset_index()
    perf_trend = calculate_trend(branch_by_year_perf[PERFORMANCE_COL].tolist())

    return {
        **basic_stats_dropout,
        **basic_stats_perf,
        "dropout_trend": dropout_trend,
        "performance_trend": perf_trend
    }


def calculate_basic_stats(series, prefix):
    """
    Calculates basic descriptive statistics for a numerical series.

    Parameters:
        series (pandas.Series): Data series.
        prefix (str): Prefix used for the output dictionary keys.

    Returns:
        dict: Mean, standard deviation, minimum and maximum values.
    """
    return {
        f"{prefix}_mean": round(series.mean(), 2),
        f"{prefix}_std": round(series.std(), 2),
        f"{prefix}_min": round(series.min(), 2),
        f"{prefix}_max": round(series.max(), 2),
    }


def calculate_trend(series):
    """
    Determines the trend of a time series using linear regression.

    Parameters:
        series (list): Sequence of mean values ordered by academic year.

    Returns:
        str: 'increasing', 'decreasing' or 'stable'.
    """
    # linregress expects (x, y). x is just the index sequence 0, 1, 2...
    slope, _, _, _, _ = linregress(range(len(series)), series)

    if slope > 0.01:
        return "increasing"
    if slope < -0.01:
        return "decreasing"
    return "stable"


def build_branch_ranking(df):
    """
    Builds rankings of study branches according to performance and dropout rates.

    Identifies:
        - Branch with best performance.
        - Branch with worst performance.
        - Branch with highest dropout.
        - Branch with lowest dropout.

    Parameters:
        df (pandas.DataFrame)

    Returns:
        dict: Rankings of branches based on the defined metrics.
    """
    # compute mean values per branch
    grouped = (
        df.groupby(BRANCH_COL)[[PERFORMANCE_COL, DROPOUT_COL]]
        .mean()
        .reset_index()
    )
    # identify the extreme values (max and min) for each metric
    max_perf = grouped[PERFORMANCE_COL].max()
    min_perf = grouped[PERFORMANCE_COL].min()
    max_dropout = grouped[DROPOUT_COL].max()
    min_dropout = grouped[DROPOUT_COL].min()
    # rankings
    best_performance = grouped.loc[grouped[PERFORMANCE_COL] == max_perf, BRANCH_COL].tolist()
    worst_performance = grouped.loc[grouped[PERFORMANCE_COL] == min_perf, BRANCH_COL].tolist()
    highest_dropout = grouped.loc[grouped[DROPOUT_COL] == max_dropout, BRANCH_COL].tolist()
    lowest_dropout = grouped.loc[grouped[DROPOUT_COL] == min_dropout, BRANCH_COL].tolist()
    # build the results dictionary
    return {
        "best_performance": best_performance,
        "worst_performance": worst_performance,
        "highest_dropout": highest_dropout,
        "lowest_dropout": lowest_dropout
    }