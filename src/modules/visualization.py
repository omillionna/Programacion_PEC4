"""
visualization.py

This module contains the functions responsible for generating the graphical
visualizations of the project. It creates the plots required in Exercise 3 to
analyze the evolution of dropout and performance rates by academic year and
study branch.
"""
import os
import matplotlib.pyplot as plt


def plot_evolution(df, output_path="src/img"):
    """
    Creates a figure with two subplots showing the evolution of:
    - Dropout rate (% Abandonament a primer curs)
    - Performance rate (Taxa rendiment)

    Each subplot includes one line per study branch (Branca),
    with different colors, legend, grid, axis labels and descriptive title.

    The figure is saved as 'evolution_olga_millionna.png'
    in the given output path.

    Parameters:
        - df (pandas.DataFrame)
        - output_dir (str): Directory where the figure will be saved.
    """
    # ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # create a figure
    _, axes = plt.subplots(1, 2, figsize=(14, 10))

    # get unique branches
    branches = sorted(df["Branca"].unique())
    # generate colors (one per branch)
    cmap = plt.get_cmap("tab10")
    colors = cmap(range(len(branches)))

    print("\n-- Exercise 3.1. Generating the graph... --")
    # -- first subplot: dropout rate --
    for branch, color in zip(branches, colors):
        branch_data = df[df["Branca"] == branch]
        grouped_df = (
            branch_data
            .groupby("Curs Acadèmic")["% Abandonament a primer curs"]
            .mean()
            .reset_index()
        )
        axes[0].plot(
            grouped_df["Curs Acadèmic"],
            grouped_df["% Abandonament a primer curs"],
            label=branch,
            color=color,
            marker="o"
        )
    axes[0].set_title("Evolution of dropout rate by academic year")
    axes[0].set_xlabel("Academic year")
    axes[0].set_ylabel("Dropout rate")
    axes[0].grid(True)
    axes[0].legend(title="Branca", fontsize=8)
    axes[0].tick_params(axis="x", rotation=45)

    # -- second subplot: theperformance rate --
    for branch, color in zip(branches, colors):
        branch_data = df[df["Branca"] == branch]
        grouped_df = (
            branch_data
            .groupby("Curs Acadèmic")["Taxa rendiment"]
            .mean()
            .reset_index()
        )
        axes[1].plot(
            grouped_df["Curs Acadèmic"],
            grouped_df["Taxa rendiment"],
            label=branch,
            color=color,
            marker="o"
        )
    axes[1].set_title("Evolution of performance rate by academic year")
    axes[1].set_xlabel("Academic year")
    axes[1].set_ylabel("Performance rate")
    axes[1].grid(True)

    # adjust X-axis rotation if necessary
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save the image
    print("\n-- Exercise 3.2. Saving the image... --")
    filename = "evolution_olga_millionna.png"
    save_path = os.path.join(output_path, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
