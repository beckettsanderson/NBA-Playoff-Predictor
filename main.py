"""
Final Project
"""

import pandas as pd

pd.set_option('display.max_columns', None)
ALL_SEASONS = "seasons_data.csv"
CUR_SEASON = "2023_data.csv"


def main():

    # read in our csv's of data
    all_df = pd.read_csv(ALL_SEASONS)
    df_23 = pd.read_csv(CUR_SEASON)

    # concat the data
    df = pd.concat([all_df, df_23], ignore_index=True)


main()
