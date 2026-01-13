"""
arg_parser_helper.py

This module defines the command line interface of the project.
It is responsible for creating and parsing the arguments that control:

- How many exercises are executed.
- Whether the datasets are loaded automatically or manually.

It centralizes all argument handling so that main.py only needs to
retrieve the parsed configuration and execute the corresponding logic.
"""
import argparse


def create_arg_parser():
    """
    Creates and parses the command line arguments of the program.

    Supported arguments:
        -ex / --exercise : Execute exercises up to the given number.
        -m / --manual   : Enable manual loading mode for datasets.

    Returns:
        - (argparse.Namespace): Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="PEC4 - Olga Millionna Millionna"
    )

    parser.add_argument(
        "-ex",
        "--exercise",
        type=int,
        choices=[1, 2, 3, 4],
        help=(
            "Execute exercises up to the given number."
            "Example: 'python main.py -ex 2' runs exercise 1 and 2."
        )
    )

    parser.add_argument(
        "-m",
        "--manual",
        action="store_true",
        help=(
            "Enable manual loading mode.\n"
            "If this option is used, datasets are loaded one by one.\n"
            "If not specified, datasets are loaded automatically."
        )
    )
    return parser.parse_args()
