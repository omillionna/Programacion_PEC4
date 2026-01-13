"""
main.py

Main entry point of the PEC4 project.

This module controls the execution of the different exercises using
command line arguments. By default, all exercises are executed.
The user can choose how many exercises to run and whether datasets
are loaded automatically or manually.
"""
from src.modules.exercises import (
    exercise_1,
    exercise_2,
    exercise_3,
    exercise_4
)
from src.modules.arg_parser_helper import create_arg_parser


def main():
    """
    Main function of the project.

    Parses the command line arguments and executes the exercises in order,
    up to the number specified by the user.

    If no arguments are provided, all exercises are executed by default.

    Examples:
        - python main.py
            -> Executes all exercises (1 to 4)

        - python main.py -e 1
            -> Executes only exercise 1

        - python main.py -e 2
            -> Executes exercises 1 and 2

        - python main.py -m
            -> Executes all exercises using manual dataset loading.
    """
    # create the argument parser
    args = create_arg_parser()
    max_exercise = args.exercise if args.exercise else 4

    rendiment_df = None
    abandonament_df = None
    merged_df = None

    # execute exercises progressively
    if max_exercise >= 1:
        rendiment_df, abandonament_df = exercise_1(args.manual)

    if max_exercise >= 2:
        merged_df = exercise_2(rendiment_df, abandonament_df)

    if max_exercise >= 3:
        exercise_3(merged_df)

    if max_exercise >= 4:
        exercise_4(merged_df)


if __name__ == "__main__":
    main()
