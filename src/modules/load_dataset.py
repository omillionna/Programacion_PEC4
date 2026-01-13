"""
load_dataset.py

This module provides utility functions to load the project datasets and
perform a basic exploratory data analysis (EDA). It allows loading datasets
either automatically by providing a file path or interactively by letting
the user choose which dataset to load.
"""
import os
import pandas as pd


def load(path=None):
    """
    Loads one of the available datasets.

    If a path is provided, the dataset is loaded directly from that path.
    If no path is provided, the user is asked to choose which dataset to load.

    Parameters:
        - path (str, optional): Path to the dataset file.

    Returns:
        - pandas.DataFrame: Loaded dataset.
        - final_path
    """
    final_path = None
    if path:
        # check if the file exists before attempting to read it.
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file is not located in: {path}")
        final_path = path
    else:
        print("Select dataset to load:")
        print("1 - rendiment_estudiants.xlsx")
        print("2 - taxa_abandonament.xlsx")
        option = input("Option: ")

        base_path = "src/data/"
        datasets = {
            "1": "rendiment_estudiants.xlsx",
            "2": "taxa_abandonament.xlsx"
        }
        if option in datasets:
            final_path = base_path + datasets[option]
        else:
            raise ValueError("Invalid option selected")
    return (pd.read_excel(final_path), final_path)


def explore(df):
    """
    Performs a basic exploratory data analysis (EDA) of the dataset.

    Shows:
    - First 5 rows
    - Column names
    - General information about the DataFrame

    Parameters:
        - df (pandas.DataFrame): Dataset to be explored.
    """
    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    print("\nDataset columns:")
    print(df.columns)

    print("\nDataset info:")
    print(df.info())
