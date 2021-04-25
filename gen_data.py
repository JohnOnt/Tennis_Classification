import pandas as pd
import numpy as np
from tqdm import tqdm

# rankings = pd.read_csv('ATP_Rankings2017.csv')
rankings = pd.read_csv('Elo_Rankings2017.csv')

def gen_outcomes():
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


def gen_elo_win_data():
    wins_matrix = np.array([[0, 1]])

    for year in tqdm(np.arange(2004, 2018)):
        matches = pd.read_csv('tennis_atp-master/atp_matches_' + str(year) + '.csv')

        wins_sub_matrix = np.zeros((np.shape(matches)[0], 2))

        for i, match in matches.iterrows():
            pw = match.winner_name
            pl = match.loser_name

            if ((pw in (rankings.name.values)) == False) | ((pl in (rankings.name.values)) == False):
                # We don't know one of the elo ratings of the players so we pass it off
                wins_sub_matrix[i] = [np.nan, np.nan]
                continue

            pw_elo = rankings.points[rankings.name == pw].values[0]
            pl_elo = rankings.points[rankings.name == pl].values[0]

            # You can add court surface values but that would be a lot more work

            wins_sub_matrix[i] = [(pw_elo - pl_elo), 1]
        
        wins_matrix = np.append(wins_matrix, wins_sub_matrix, axis=0)


    colnames = ['elo_diff', 'winner']
    elo_wins_df = pd.DataFrame(wins_matrix[1:], columns=colnames)
    elo_wins_df = elo_wins_df.dropna()
    elo_wins_df.to_csv('elo_wins.csv', index=False)


def attach_classifications():
    pass