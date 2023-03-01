"""

"""

import pandas as pd

pd.set_option('display.max_columns', None)


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
        df_p100 = pd.read_html(url, header=0, match='Per 100 Poss Stats')[0]
        df_adv = pd.read_html(url, header=1, match='Advanced Stats')[0]
        df_shoot = pd.read_html(url, header=1, match='Shooting Stats')[0]

        # clean per 100 data
        df_p100.drop(['Rk', 'G', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%'],
                     inplace=True,
                     axis=1)

        # clean advanced data
        df_adv.drop(['Rk', 'L', 'Arena', 'Attend.'], inplace=True, axis=1)
        """ Change W to W/L% """
        #df_adv['W'] = df_adv['W'].apply(lambda x: round(x / 82, 2))
        df_adv.dropna(axis=1, inplace=True)

        # clean shooting data
        df_shoot.drop(['Rk', 'G', 'MP'], inplace=True, axis=1)
        df_shoot.dropna(axis=1, inplace=True)

        print(df_p100)
        print(df_adv)
        print(df_shoot)

    return years_dict


def main():

    # create the list of years we want data for
    years = list(range(2000, 2024))

    temp_years = [2023]
    scrape_years(temp_years)


main()
