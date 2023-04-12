"""
Final Project
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import copy

pd.set_option('display.max_columns', None)
ALL_SEASONS = "seasons_data.csv"
CUR_SEASON = "2023_data.csv"


def main():

    # read in our csv's of data
    all_df = pd.read_csv(ALL_SEASONS)
    df_23 = pd.read_csv(CUR_SEASON)

    # concat the data
    df = pd.concat([all_df, df_23], ignore_index=True)

    # drop minutes played and attendance per game
    all_df.drop(['MP', 'Attend./G'], axis=1, inplace=True)
    df_23.drop(['MP', 'Attend./G'], axis=1, inplace=True)

    # split the data using all features
    features = all_df[all_df.columns[1:-2]]
    target = all_df[['Playoff']]

    X = features  # get the input features
    y = target  # get the target

    X_train, X_test, y_train, y_test = train_test_split(X,  # the input features
                                                        y,  # the label
                                                        test_size=0.3,  # set aside 30% of the data as the test set
                                                        random_state=7  # reproduce the results
                                                         )

    # make random forest regressor model with all features
    rf = RandomForestRegressor(random_state=7)
    rf.fit(X_train, y_train)

    # predict the labels for the test set
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Evaluate the Predictions
    print('The mse of the model is: {}'.format(mse))

    # Determine feature importance, identify features
    importances = pd.DataFrame({'stat': features.columns,
                                'value': rf.feature_importances_})
    importances.sort_values('value', ascending=False, inplace=True)
    #print(importances.head(10))

    # split the data with top 10 features
    features = all_df[importances.loc[:11, 'stat']]
    target = all_df[['Playoff']]

    X = features  # get the input features
    y = target  # get the target

    X_train, X_test, y_train, y_test = train_test_split(X,  # the input features
                                                        y,  # the label
                                                        test_size=0.3,  # set aside 30% of the data as the test set
                                                        random_state=7  # reproduce the results
                                                         )

    # make random forest regressor model with top 10 features
    rf = RandomForestRegressor(random_state=7)
    rf.fit(X_train, y_train)

    # predict the labels for the test set
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Evaluate the Predictions
    print('The mse of the model is: {}'.format(mse))

    # split the data using all features
    features = all_df[all_df.columns[1:-2]]
    target = all_df[['Playoff']]

    X = features  # get the input features
    y = target  # get the target

    X_train, X_test, y_train, y_test = train_test_split(X,  # the input features
                                                        y,  # the label
                                                        test_size=0.3,  # set aside 30% of the data as the test set
                                                        random_state=7  # reproduce the results
                                                         )

    # make random forest regressor model with all features
    rf = RandomForestRegressor(random_state=7)
    rf.fit(X_train, y_train)

    # predict the labels for the 2023 teams
    df_23_new = copy.deepcopy(df_23)
    teams = df_23.loc[:, 'Team']

    df_23_new.drop(['Team', 'Year'], axis=1, inplace=True)
    y_pred = rf.predict(df_23_new)

    outcome = pd.DataFrame({'Team': teams,
                            'Playoff': y_pred})
    outcome.sort_values('Playoff', ascending=False, inplace=True, ignore_index=True)
    print(outcome)


main()
