"""

"""

import pandas as pd


def scrape_years(years):
    """
    Scrape the years and return a dictionary of dataframes

    Parameters
    ----------
    years : list
        list containing the years to scrape

    Return
    ------
    years_dict : dictionary
        dictionary containing years referencing data frames
    """
    years_dict = {}
    URL = "https://www.basketball-reference.com/leagues/NBA_{}.html"

    # loop through all the years in the list
    for year in years:

        # adjust the url to each year
        url = URL.format(year)

        # read in data
        df_p100 = pd.read_html(url, header=0, match='Per 100 Poss Stats')
        df_adv = pd.read_html(url, header=1, match='Advanced Stats')
        df_shoot = pd.read_html(url, header=1, match='Shooting Stats')

        print(df_p100[0])
        print(df_adv[0])
        print(df_shoot[0])

    return years_dict


def main():

    # create the list of years we want data for
    years = list(range(2000, 2024))

    temp_years = [2023]
    scrape_years(temp_years)


main()
