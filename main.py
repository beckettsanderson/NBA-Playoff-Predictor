"""
Final Project
"""

import pandas as pd
import load_data as ld

pd.set_option('display.max_columns', None)
MIN_YEAR = 2010
MAX_YEAR = 2022


def main():

    # create the list of years we want data for
    years = list(range(MIN_YEAR, MAX_YEAR + 1))

    # get the playoff data
    df_playoffs = ld.get_playoffs(MIN_YEAR)

    # load in the entirety of the
    df = ld.scrape_years(years, df_playoffs)
    print(df)
    print(df.describe)


main()
