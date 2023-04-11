"""
File to load in all the data from Basketball Reference
"""

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
MIN_YEAR = 2010
MAX_YEAR = 2022


def get_playoffs(min_year):
    """
    Load in playoff dataset and clean it to apply to our teams data

    Parameters
    ----------
    min_year : int
        the lowest year to collect playoff data from

    Returns
    -------
    df_playoffs : DataFrame
        cleaned df containing the year, round, and teams for each playoff series

    """
    # read in the playoff data
    playoff_url = "https://www.basketball-reference.com/playoffs/series.html"
    df_playoffs = pd.read_html(playoff_url, header=1)[0]

    # remove empty rows and rows with labels
    df_playoffs.dropna(axis=0, how='all', inplace=True)
    df_playoffs.drop(df_playoffs[df_playoffs.Yr == 'Yr'].index, inplace=True)

    # drop years below lowest year we're using
    df_playoffs = df_playoffs.astype({'Yr': 'int'})
    df_playoffs = df_playoffs[df_playoffs['Yr'] >= min_year]

    # drop the columns we don't care about and rename the columns left
    df_playoffs.dropna(axis=1, how='all', inplace=True)
    df_playoffs.drop(['Lg', 'Unnamed: 3', 'W', 'W.1', 'Favorite', 'Underdog'],
                     inplace=True,
                     axis=1)
    df_playoffs.columns = ['Yr', 'Round', 'Win_Tm', 'Loss_Tm']

    # remove parentheses from team names
    df_playoffs['Win_Tm'] = df_playoffs['Win_Tm'].apply(lambda x: x[0:-4])
    df_playoffs['Loss_Tm'] = df_playoffs['Loss_Tm'].apply(lambda x: x[0:-4])

    # rename playoff series to round
    df_playoffs['Round'] = df_playoffs['Round'].replace({
        'Eastern Conf First Round': 0.25,
        'Eastern Conf Semifinals': 0.5,
        'Eastern Conf Finals': 0.75,
        'Finals': 1,
        'Western Conf First Round': 0.25,
        'Western Conf Semifinals': 0.5,
        'Western Conf Finals': 0.75,
    })

    return df_playoffs


def scrape_year(year, playoffs, season_url, cur_year):
    """
    Scrape the years and return a dictionary of dataframes

    Parameters
    ----------
    year : int
        int containing the year to scrape from
    playoffs : DataFrame
        df with playoff data
    season_url : str
        the base url of the basketball reference link
    cur_year : boolean
        if the year is the current one (i.e. no playoffs)

    Return
    ------
    cur_df : DataFrame
        temporary dataframe containing years referencing data frames
    """
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
    cur_df['Year'] = year

    # narrow playoffs down to each year
    playoffs = playoffs[playoffs['Yr'] == year]

    # remove the asterix from the teams with it on the end of their name
    for ind in cur_df.index:
        if cur_df["Team"][ind].endswith("*"):
            cur_df["Team"][ind] = cur_df["Team"][ind].rstrip("*").strip()

    # create playoff column and add values if it's not the current year
    if not cur_year:
        cur_df['Playoff'] = 0
        for p_idx, p_row in playoffs.iterrows():
            for idx, row in cur_df.iterrows():
                if p_row['Loss_Tm'] == row['Team']:
                    cur_df.loc[idx, 'Playoff'] = p_row['Round']
                elif p_row['Round'] == 1 and p_row['Win_Tm'] == row['Team']:
                    cur_df.loc[idx, 'Playoff'] = p_row['Round']

    return cur_df


def scrape_years(years, playoffs, cur_year=False):
    """
    Scrape the years and return a dictionary of dataframes

    Parameters
    ----------
    years : list
        list containing the years to scrape
    playoffs : DataFrame
        df with playoff data
    cur_year : boolean
        if the year is the current one (i.e. no playoffs)

    Return
    ------
    df : DataFrame
        dataframe containing years referencing data frames
    """
    df = pd.DataFrame()
    season_url = "https://www.basketball-reference.com/leagues/NBA_{}.html"

    # loop through all the years in the list
    for year in years:

        # scrape the year's data into a dataframe
        cur_df = scrape_year(year, playoffs, season_url, cur_year)

        # add the current dataframe to our overall df of teams
        df = pd.concat([df, cur_df], ignore_index=True)

    return df


def main():

    # create the list of years we want data for
    years = list(range(MIN_YEAR, MAX_YEAR + 1))
    current_year = [2023]

    # get the playoff data
    df_playoffs = get_playoffs(MIN_YEAR)

    # load in the entirety of the years seasons and save is as a csv
    df = scrape_years(years, df_playoffs)
    df.to_csv("seasons_data.csv", index=False)

    # load in the current year with no playoff column and save as a csv
    df_23 = scrape_year(current_year, df_playoffs)
    df_23.to_csv("2023_data.csv", index=False)


main()
