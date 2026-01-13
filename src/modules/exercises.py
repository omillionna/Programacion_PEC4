"""
exercises.py

This module implements the main exercises of the PEC4 project:
dataset loading and EDA, data cleaning and merging, and data visualization.
"""
from src.modules.load_dataset import load, explore
from src.modules.merge_dataset import (
    rename_abandonment_columns,
    remove_columns,
    group_by_branch,
    merge_datasets
)
from src.modules.visualization import plot_evolution
from src.modules.analysis import analyze_dataset


def exercise_1(manual=False):
    """
    Exercise 1: Dataset loading and Exploratory Data Analysis (EDA).

    Loads the two required datasets:
        - taxa_abandonament
        - rendiment_estudiants

    Two loading modes are supported:
        - Automatic mode (default): datasets are loaded from predefined paths.
        - Manual mode (-m): the user selects and loads the datasets one by one.

    Each loaded dataset is identified by its file path and assigned to the
    corresponding variable. A basic exploratory analysis is performed using
    the explore() function.

    Parameters:
        - manual (bool, optional):
            If True, datasets are loaded manually by the user.
            If False, datasets are loaded automatically. Default is False.

    Returns:
        - rendiment_df (pandas.DataFrame):
            DataFrame containing the performance dataset.
        - abandonament_df (pandas.DataFrame):
            DataFrame containing the abandonment dataset.
    """
    print("\n\n******** EXERCISE 1: Dataset loading and EDA ******** ")
    # initialize both DataFrames as None.
    # they will be filled once the corresponding dataset is loaded.
    rendiment_df = None
    abandonament_df = None

    if manual:
        print("\nManual loading mode enabled.")
        # loop until both datasets are loaded
        while rendiment_df is None or abandonament_df is None:
            print("\n-- Load a dataset... --")
            # load a dataset
            df, path = load()
            # identify which dataset has been loaded using the file name
            if "taxa_abandonament" in path:
                abandonament_df = df
                print(
                    "Detected dataset: *taxa_abandonament* "
                    "successfully loaded.")
            elif "rendiment_estudiants" in path:
                rendiment_df = df
                print(
                    "Detected dataset: *rendiment_estudiants* "
                    "successfully loaded."
                    )
            explore(df)

            # inform the user of the current status
            print("\nCurrent loading status:")
            print(
                    f"\t- *taxa_abandonament* loaded: "
                    f"{abandonament_df is not None}"
                )
            print(
                    f"\t- *rendiment_estudiants* loaded: "
                    f"{rendiment_df is not None}"
                )

        # when the loop finishes, both datasets are guaranteed to be loaded
        print("\nBoth datasets have been successfully loaded.")
        print("\n******** EXERCISE 1: DONE ******** ")
    else:
        print("\nAutomatic loading mode enabled.")

        abandonament_df, _ = load("src/data/taxa_abandonament.xlsx")
        print("Loaded dataset: *taxa_abandonament*")
        explore(abandonament_df)

        rendiment_df, _ = load("src/data/rendiment_estudiants.xlsx")
        print("Loaded dataset: *rendiment_estudiants*")
        explore(rendiment_df)

    return rendiment_df, abandonament_df


def exercise_2(rendiment_df, abandonament_df):
    """
    Exercise 2: Data cleaning, transformation and merging.

    This exercise applies the following steps:
      2.1. Rename columns in the abandonment dataset.
      2.2. Remove unnecessary columns from both datasets.
      2.3. Group both datasets by academic and demographic variables.
      2.4. Merge both datasets into a single DataFrame.

    Parameters:
        - rendiment_df (pandas.DataFrame): Performance dataset.
        - abandonament_df (pandas.DataFrame): Abandonment dataset.

    Returns:
        - merged_df (pandas.DataFrame): Final merged dataset.
    """
    # -------------
    # Exercise 2.1
    # -------------
    print("\n\n******** EXERCISE 2: Data cleaning and merging ******** ")
    # check that the dataset is not empty
    if abandonament_df.empty:
        raise ValueError("taxa_abandonament dataset is not loading")
    print(
        "\n-- Exercise 2.1. Renaming columns in the dataset "
        "*taxa_abandonament* --"
        )
    abandonament_df = rename_abandonment_columns(abandonament_df)

    # -------------
    # Exercise 2.2
    # -------------
    print(
        "\n-- Exercise 2.2. Removing columns in the dataset "
        "*taxa_abandonament* --"
        )
    abandonament_df = remove_columns(abandonament_df)
    print(
        "\n-- Exercise 2.2. Removing columns in the dataset "
        "*rendiment_estudiants* --"
        )
    # check that the dataset is not empty
    if rendiment_df.empty:
        raise ValueError("rendiment_estudiants dataset is not loading")
    rendiment_df = remove_columns(rendiment_df)

    # -------------
    # Exercise 2.3
    # -------------
    print(
        "\n-- Exercise 2.3. Grouping rows of the dataset "
        "*taxa_abandonament* --"
        )
    abandonament_df = group_by_branch(abandonament_df)
    print(
        "\n-- Exercise 2.3. Grouping rows of the dataset "
        "*rendiment_estudiants* --"
        )
    rendiment_df = group_by_branch(rendiment_df)

    # -------------
    # Exercise 2.4
    # -------------
    print(
        "\n-- Exercise 2.4. Merging *taxa_abandonament* "
        "and *rendiment_estudiants* --"
        )
    merged_df = merge_datasets(rendiment_df, abandonament_df)
    print("\n******** EXERCISE 2: DONE ******** ")

    return merged_df


def exercise_3(df):
    """
    Exercise 3: Data visualization.

    Generates a figure with two subplots:
        - Evolution of the dropout rate by academic year.
        - Evolution of the performance rate by academic year.

    Each subplot includes one line per study branch (Branca), with legend,
    grid, descriptive titles and appropriate axis labels. The figure is saved
    as an image file in the project directory.

    Parameters:
        - df (pandas.DataFrame): Merged dataset produced in Exercise 2.
    """
    print("\n\n******** EXERCISE 3: Data visualization ********")
    plot_evolution(df)
    print("\n******** EXERCISE 3: DONE ********")


def exercise_4(df):
    print("\n\n******** EXERCISE 4: Automated statistical analysis ********")
    analyze_dataset(df)
    print("\n******** EXERCISE 4: DONE ********")