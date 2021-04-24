import pandas as pd
import numpy as np
from tqdm import tqdm

rankings = pd.read_csv('ATP_Rankings2017.csv')
players = rankings.name.values

colnames = ['Player1', 'Player2', 'Outcome']
Outcomes = pd.DataFrame(index=[''], columns=colnames)

ind = 0
for year in tqdm(np.arange(2004, 2018)):
    matches = pd.read_csv('tennis_atp-master/atp_matches_' + str(year) + '.csv')

    #tour_players = list(set(np.append(matches.winner_name.values, matches.loser_name.values)))

    # Go through tournament players only in the top 100 (avoids NaN values)
    # for player in [x for x in tour_players if x in players]:
    for _, match in matches.iterrows():

        if (match.winner_name in players) & (match.loser_name in players):
            Outcomes.loc[ind] = [match.winner_name, match.loser_name, 1]
            ind += 1


Outcomes = Outcomes.dropna()
Outcomes.to_csv('ATP_Outcomes.csv')

# Now a contingency tableee
matchups = pd.DataFrame(0, index = players, columns= players)
matchups.head()

n = np.size(players)
for i in range(0,n):
    p1 = Outcomes.iloc[i].Player1
    p2 = Outcomes.iloc[i].Player2

    if Outcomes.iloc[i].Outcome == 1:
        matchups.loc[p2, p1] = matchups.loc[p2, p1] + 1
    else:
        matchups.loc[p1, p2] = matchups.loc[p1, p2] + 1


print(matchups.head())

matchups.to_csv('ATP_Cont_Table.csv')