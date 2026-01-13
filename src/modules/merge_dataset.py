"""
merge_dataset.py

This module contains the functions used to clean, transform and merge the
datasets. It standardizes column names, removes unnecessary information,
groups data by academic and demographic variables, and combines both datasets
into a single DataFrame.
"""
import pandas as pd


def rename_abandonment_columns(df):
    """
    Renames the columns of the abandonment dataset so that they match
    the column names used in the performance dataset.

    This step is necessary to homogenize both datasets and make them
    compatible for grouping and merging operations.

    Parameters:
        - df (pandas.DataFrame)

    Returns:
        - pandas.DataFrame: DataFrame with renamed columns.
    """

    # dictionary that maps column names from the abandonment dataset
    # to the equivalent names used in the performance dataset
    names_dict = {
        "Naturalesa universitat responsable": "Tipus universitat",
        "Universitat Responsable": "Universitat",
        "Sexe Alumne": "Sexe",
        "Tipus de centre": "Integrat S/N"
    }
    # apply the renaming and return the new DataFrame
    return df.rename(columns=names_dict)


def remove_columns(df):
    """
    emoves unnecessary columns from the dataset.

    The following columns are always removed :
        - 'Universitat'
        - 'Unitat'

    Additionally, if the dataset corresponds to the performance dataset,
    these columns are also removed:
        - 'Crèdits ordinaris superats'
        - 'Crèdits ordinaris matriculats'

    Parameters:
        - df (pandas.DataFrame)

    Returns:
        - pandas.DataFrame: Dataset without the unnecessary columns.
    """

    # columns to drop in both datasets
    columns_to_remove = ["Universitat", "Unitat"]
    # columns that only appear in the performance dataset
    performance_columns = [
            "Crèdits ordinaris superats",
            "Crèdits ordinaris matriculats"
        ]
    for col in performance_columns:
        if col in df.columns:
            columns_to_remove.append(col)

    # remove columns
    return df.drop(columns=columns_to_remove)


def group_by_branch(df):
    """
    Groups the dataset by academic and demographic variables and computes
    the mean value of the main numerical column.

    The grouping columns are:
        - 'Curs Acadèmic'
        - 'Tipus universitat'
        - 'Sigles'
        - 'Tipus Estudi'
        - 'Branca'
        - 'Sexe'
        - 'Integrat S/N'

    The value column depends on the dataset:
        - '% Abandonament a primer curs' for the abandonment dataset
        - 'Taxa rendiment' for the performance dataset

    The function automatically detects which one exists

    Parameters:
        - df (pandas.DataFrame)

    Returns:
        - pandas.DataFrame: Dataset with mean value.
    """

    # columns used to group the dataset
    group_columns = [
        "Curs Acadèmic",
        "Tipus universitat",
        "Sigles",
        "Tipus Estudi",
        "Branca",
        "Sexe",
        "Integrat S/N"
    ]
    # possible value columns depending on the dataset
    columns = ["% Abandonament a primer curs", "Taxa rendiment"]
    column_value = [c for c in columns if c in df.columns]

    # group the dataset and compute the mean of the detected column
    return (
        df.groupby(group_columns, as_index=False)[column_value[0]].mean()
    )


def merge_datasets(rendiment_df, abandonment_df):
    """
    Merges both datasets keeping only common rows (inner join).

    Parameters:
        - rendiment_df (pandas.DataFrame)
        - abandonment_df (pandas.DataFrame)

    Returns:
        - pandas.DataFrame: 
            Merged dataset containing information from both datasets.
    """

    # columns used as keys to merge both datasets
    merge_columns = [
        "Curs Acadèmic",
        "Tipus universitat",
        "Sigles",
        "Tipus Estudi",
        "Branca",
        "Sexe",
        "Integrat S/N"
    ]

    # perform an inner join so that only common rows are kept
    return pd.merge(
        rendiment_df,
        abandonment_df,
        on=merge_columns,
        how="inner"
    )
