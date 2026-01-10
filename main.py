"""
main.py

Main entry point of the PEC4 project for the subject
'Programming for Data Science' (UOC).

This script controls the execution of the different exercises of the PEC.
The user can decide from the command line how many exercises to execute.
If no argument is given, all exercises are executed by default.
"""
import argparse
from src.modules.load_dataset import load, explore
from src.modules.clean_merge_dataset import (
    rename_abandonment_columns, 
    remove_columns, 
    group_by_branch, 
    merge_datasets
)


def exercise_1():
    """
    Exercise 1: Load both datasets and perform a basic Exploratory Data Analysis (EDA).

    The function keeps asking the user to load datasets until both required datasets
    are available:
      - taxa_abandonament
      - rendiment_estudiants

    Each time a dataset is loaded:
      - It is identified by checking its file path.
      - The DataFrame is assigned to the correct variable.
      - A basic EDA is performed using the explore() function.

    Returns:
        - rendiment_df (pandas.DataFrame): DataFrame containing the performance dataset.
        - abandonament_df (pandas.DataFrame): DataFrame containing the abandonment dataset.
    """
    print("\n\n******** EXERCISE 1: Dataset loading and EDA ******** ")
    # initialize both DataFrames as None.
    # they will be filled once the corresponding dataset is loaded.
    rendiment_df = None
    abandonament_df = None

    # loop until both datasets are loaded
    while rendiment_df is None or abandonament_df is None:
        print("\n-- Load a dataset... --")
        # load a dataset
        df, path = load()
        # identify which dataset has been loaded using the file name
        if "taxa_abandonament" in path:
            abandonament_df = df
            print("Detected dataset: *taxa_abandonament* successfully loaded.")
        elif "rendiment_estudiants" in path:
            rendiment_df = df
            print("Detected dataset: *rendiment_estudiants* successfully loaded.")
        explore(df)

         # inform the user of the current status
        print("\nCurrent loading status:")
        print(f"  - *taxa_abandonament* loaded: {abandonament_df is not None}")
        print(f"  - *rendiment_estudiants* loaded: {rendiment_df is not None}")

    # when the loop finishes, both datasets are guaranteed to be loaded
    print("\nBoth datasets have been successfully loaded.")
    print("\n ******** EXERCISE 1: DONE ******** ")

    return rendiment_df, abandonament_df

def exercise_2(rendiment_df, abandonament_df):
    """
    Exercise 2: Data cleaning, transformation and merging.

    This exercise applies the following steps:
      2.1. Rename columns in the abandonment dataset to match the performance dataset.
      2.2. Remove unnecessary columns from both datasets.
      2.3. Group both datasets by academic and demographic variables and compute means.
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
    print("\n\n ******** EXERCISE 2: Data cleaning and merging ******** ")
    # check that the dataset is not empty
    if abandonament_df.empty:
        raise ValueError("taxa_abandonament dataset is not loading")
    print("\n-- Exercise 2.1. Renaming columns in the dataset *taxa_abandonament* --")
    abandonament_df = rename_abandonment_columns(abandonament_df)

    # -------------
    # Exercise 2.2
    # -------------
    print("\n-- Exercise 2.2. Removing columns in the dataset *taxa_abandonament* --")
    abandonament_df = remove_columns(abandonament_df)
    print("\n-- Exercise 2.2. Removing columns in the dataset *rendiment_estudiants* --")
    # check that the dataset is not empty
    if rendiment_df.empty:
        raise ValueError("rendiment_estudiants dataset is not loading")
    rendiment_df = remove_columns(rendiment_df)

    # -------------
    # Exercise 2.3
    # -------------
    print("\n-- Exercise 2.3. Grouping rows of the dataset *taxa_abandonament* --")
    abandonament_df = group_by_branch(abandonament_df)
    print("\n-- Exercise 2.3. Grouping rows of the dataset *rendiment_estudiants* --")
    rendiment_df = group_by_branch(rendiment_df)

    # -------------
    # Exercise 2.4
    # -------------
    print("\n-- Exercise 2.4. Merging *taxa_abandonament* and *rendiment_estudiants* --")
    merged_df = merge_datasets(rendiment_df, abandonament_df)
    print("\n ******** EXERCISE 2: DONE ******** ") 

    return merged_df

def main():
    """
    Main function of the project.

    It parses the command line arguments and executes the exercises
    up to the number specified by the user.

    Examples:
        python main.py
            -> Executes all exercises (1 to 4)

        python main.py -e 1
            -> Executes only exercise 1

        python main.py -e 2
            -> Executes exercises 1 and 2
    """
    # create the argument parser
    parser = argparse.ArgumentParser(
        description = "PEC4 - Olga Millionna Millionna"
    )

    parser.add_argument(
        "-e",
        "--exercise",
        type = int,
        choices = [1, 2, 3, 4],
        help = "Execute exercises up to the given number (example: 'python main.py -ex 2' runs exercise 1 and 2)."
    )

    args = parser.parse_args()

    # if no argument is passed, run all exercises
    max_exercise = args.exercise if args.exercise else 4

    rendiment_df = None
    abandonament_df = None
    merged_df = None

    # execute exercises progressively
    if max_exercise >= 1:
        rendiment_df, abandonament_df = exercise_1()

    if max_exercise >= 2:
        merged_df = exercise_2(rendiment_df, abandonament_df)

    if max_exercise >= 3:
        print("\nExercise 3: (to be implemented)")
        # aquí llamarás a tu módulo de visualización

    if max_exercise >= 4:
        print("\nExercise 4: (to be implemented)")
        # aquí llamarás a tu módulo de análisis estadístico

if __name__ == "__main__":
    main()
