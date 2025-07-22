# imports 
import re
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
pd.options.mode.chained_assignment = None 

start_time = time.time()

# functions
# save csv
def export_csv(string):
    df_final.to_csv(string)


# reverse string for maps
def str_reverse(s: str) -> str:
    if '-' in s:
        temp1, temp2 = s.split("-")
        reversed_str = f'{temp2}-{temp1}'
        return reversed_str
    else: 
        return s


# sorting rosters
def sort_roster(s: str) -> str:
    players = re.findall(r'\w+', s)
    players.sort(key=str.lower)
    sorted_players = ' '.join(players)
    return sorted_players


def label_encode(list_values: list):
    encoder = LabelEncoder()
    unique_values_for_encode = pd.concat([df_final[col] for col in list_values]).unique()
    encoder.fit(unique_values_for_encode)

    for col in list_values: 
        df_final[col] = encoder.transform(df_final[col])


# dataset
df = pd.read_csv('2024-01-01(correct+id).csv')
column_groups = {
    'teams': ['team1', 'team2', 'winner'],
    'rosters': ['team1_roster', 'team2_roster'],
    'maps': ['map1', 'map2', 'map3', 'map4', 'map5'],
    'map_scores': ['map1_score', 'map2_score', 'map3_score', 'map4_score', 'map5_score'],
    'score': ['match_score']
}
main_teams = ['Vitality', 'MOUZ', 'The MongolZ', 'Spirit', 
              'Falcons', 'Natus Vincere', 'FaZe', 'FURIA', 'paiN', 
              'G2', 'Astralis', 'Virtus.pro', 'GamerLegion', '3DMAX',
              'Legacy', 'Liquid', 'HEROIC', 'MIBR', 'Lynn Vision'] # 'Aurora'

# drop na
df[column_groups['maps']] = df[column_groups['maps']].fillna('Not played')
df[column_groups['map_scores']] = df[column_groups['map_scores']].fillna('No score')
df_clear = df.dropna(subset=column_groups['rosters'])

# dataset restructuring
df_final = pd.DataFrame([])

for team in main_teams: 
    df_temp = pd.concat([df_clear[df_clear['team1'] == team], 
                          df_clear[df_clear['team2'] == team]])

    for x in range(len(df_temp)):
        if df_temp['team1'].iloc[x] != team:
            df_temp['team1'].iloc[x], df_temp['team2'].iloc[x] = df_temp['team2'].iloc[x], df_temp['team1'].iloc[x]
            df_temp['team1_roster'].iloc[x], df_temp['team2_roster'].iloc[x] = df_temp['team2_roster'].iloc[x], df_temp['team1_roster'].iloc[x]
            df_temp['match_score'].iloc[x] = str_reverse(df_temp['match_score'].iloc[x])

            for map_score in column_groups['map_scores']:
                if df_temp[map_score].iloc[x] != 'No score':
                    df_temp[map_score].iloc[x] = str_reverse(df_temp[map_score].iloc[x])
   
    df_final = pd.concat([df_final, df_temp], ignore_index=True)

for x in range(len(df_final['team1_roster'])):
    for team_roster in column_groups['rosters']:
        df_final[team_roster].iloc[x] = sort_roster(df_final[team_roster].iloc[x])

# label encoding
label_encode(column_groups['rosters'])
label_encode(column_groups['maps'])
label_encode(column_groups['teams'])
label_encode(column_groups['score'])
label_encode(column_groups['map_scores'])

# reser indexes
df_final.reset_index()

# export cleared csv
export_csv('final_cleared.csv')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Время выполнения: {elapsed_time:.4f} секунд")