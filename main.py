"""
Final Project
"""

import pandas as pd

pd.set_option('display.max_columns', None)
MIN_YEAR = 2010
MAX_YEAR = 2023


def get_playoffs():
    """


    """
    # read in the playoff data
    playoff_url = "https://www.basketball-reference.com/playoffs/series.html"
    df_playoffs = pd.read_html(playoff_url, header=1)[0]

    # remove empty rows and rows with labels
    df_playoffs.dropna(axis=0, how='all', inplace=True)
    df_playoffs.drop(df_playoffs[df_playoffs.Yr == 'Yr'].index, inplace=True)

    # drop years below lowest year we're using
    df_playoffs = df_playoffs.astype({'Yr': 'int'})
    df_playoffs = df_playoffs[df_playoffs['Yr'] >= MIN_YEAR]

    # drop the columns we don't care about and rename the columns left
    df_playoffs.dropna(axis=1, how='all', inplace=True)
    df_playoffs.drop(['Lg', 'Unnamed: 3', 'W', 'W.1', 'Favorite', 'Underdog'],
                     inplace=True,
                     axis=1)
    df_playoffs.columns = ['Yr', 'Series', 'Win_Tm', 'Loss_Tm']

    # remove parentheses from team names

    # rename playoff series to round

    print(df_playoffs)
    return df_playoffs


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
    season_url = "https://www.basketball-reference.com/leagues/NBA_{}.html"

    # loop through all the years in the list
    for year in years:

        # adjust the url to each year
        url = season_url.format(year)

        # read in data
        df_p100 = pd.read_html(url, header=0, match='Per 100 Poss Stats')[0]
        df_adv = pd.read_html(url, header=1, match='Advanced Stats')[0]
        df_shoot = pd.read_html(url, header=1, match='Shooting Stats')[0]

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
        # rename columns in dataset
        for i in range(14, 18):
            df_adv.columns.values[i] = 'off_' + df_adv.columns.values[i]
        for i in range(18, 22):
            df_adv.columns.values[i] = 'def_' + df_adv.columns.values[i][:-2]
        df_adv.sort_values("Team", inplace=True)
        df_adv.reset_index(inplace=True, drop=True)

        # clean shooting data
        df_shoot.drop(['Rk', 'G', 'MP'], inplace=True, axis=1)
        df_shoot.drop([30], inplace=True, axis=0)
        df_shoot.dropna(axis=1, inplace=True)
        # rename columns in dataset
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
        # print(cur_df)

    return years_dict


def main():

    # create the list of years we want data for
    years = list(range(MIN_YEAR, MAX_YEAR + 1))

    #temp_years = [2022]
    #scrape_years(temp_years)

    get_playoffs()


main()