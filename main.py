"""
Final Project
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
        #df_playoffs = pd.read_html(url, header=None, match='Playoff Series')

        # clean per 100 data
        df_p100.drop(['Rk', 'G', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%'],
                     inplace=True,
                     axis=1)
        df_p100.sort_values("Team", inplace=True)
        df_p100.reset_index(inplace=True, drop=True)

        # clean advanced data
        df_adv['win_perc'] = round(df_adv['W'] / (df_adv['W'] + df_adv['L']), 3)
        df_adv.drop(['Rk', 'W', 'L', 'Arena', 'Attend.'], inplace=True, axis=1)
        df_adv.drop([30], inplace=True, axis=0)
        df_adv.dropna(axis=1, inplace=True)
        for i in range(15, 19):
            df_adv.columns.values[i] = 'off_' + df_adv.columns.values[i]
        for i in range(19, 23):
            df_adv.columns.values[i] = 'def_' + df_adv.columns.values[i][:-2]
        df_adv.sort_values("Team", inplace=True)
        df_adv.reset_index(inplace=True, drop=True)

        # clean shooting data
        # clean shooting data
        df_shoot.drop(['Rk', 'G', 'MP'], inplace=True, axis=1)
        df_shoot.drop([30], inplace=True, axis=0)
        df_shoot.dropna(axis=1, inplace=True)
        for i in range(3, 9):
            df_shoot.columns.values[i] = 'fga_perc_' + df_shoot.columns.values[i]
        for i in range(9, 15):
            df_shoot.columns.values[i] = 'fg_perc_' + df_shoot.columns.values[i][:-2]
        for i in range(15, 17):
            df_shoot.columns.values[i] = 'fg_ast_perc_' + df_shoot.columns.values[i][:-2]
        for i in range(17, 19):
            df_shoot.columns.values[i] = 'dunks_' + df_shoot.columns.values[i]
        for i in range(19, 21):
            df_shoot.columns.values[i] = 'layups_' + df_shoot.columns.values[i][:-2]
        for i in range(21, 23):
            df_shoot.columns.values[i] = 'corner_' + df_shoot.columns.values[i]
        df_shoot.columns.values[23] = 'heave_' + df_shoot.columns.values[23]
        df_shoot.columns.values[24] = 'heave_' + df_shoot.columns.values[24][:-2]
        df_shoot.sort_values("Team", inplace=True)

        # merge all the dataframes into one larger one with all the stats per team
        cur_df = pd.merge(pd.merge(df_p100, df_adv, on='Team'), df_shoot, on='Team')
        print(cur_df)
        #print(df_playoffs)

    return years_dict


def main():

    # create the list of years we want data for
    years = list(range(2010, 2024))

    temp_years = [2023]
    scrape_years(temp_years)


main()