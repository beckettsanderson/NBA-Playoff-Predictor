# NBA-Playoff-Predictor

The purpose of this project is to identify which NBA teams have the highest chances of winning the championship during the 2022-2023 season. We compare the current teams’ 
statistics to historical NBA data from Basketball-Reference and the success of those respective teams in the postseason. 

We prepared this data by scraping the per_100, advanced, and shooting statistics tables. The models we compared are multiple regression, K-Nearest Neighbors, 
and Random Forest Regression. For our target variable we created a playoff score from zero to one, where zero represents not making the Playoffs, and
one represents the team played in the championship that year. The numbers between that (0.25, 0.50, 0.75) signify how
far in the playoffs that specific team reached. Therefore, if our model gives a team in the 2023 season a higher number, they are
more likely to make it to the championship. We filled out our brackets with the initial seeding of this playoffs, but then
filled out the rest based on which team has the highest “playoff” number based on the model. The team with the
highest number would eventually go on to win the 2023 NBA Finals.
