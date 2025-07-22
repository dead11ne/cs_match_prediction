# imports 
import re
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
pd.options.mode.chained_assignment = None 

start_time = time.time()  # Засекаем начальное время

# functions
# save csv
def export_csv(string):
    df_final.to_csv(string)


# reverse string for maps
def str_reverse(s):
    if '-' in s:
        temp1, temp2 = s.split("-")
        reversed_str = f'{temp2}-{temp1}'
        return reversed_str
    else: 
        return s


# sorting rosters
def sort_roster(s):
    players = re.findall(r'\w+', s)
    players.sort(key=str.lower)
    sorted_players = ' '.join(players)
    return sorted_players


# dataset
df = pd.read_csv('2024-01-01(correct+id).csv')
main_teams = ['Vitality', 'MOUZ', 'The MongolZ', 'Spirit', 
              'Falcons', 'Natus Vincere', 'FaZe', 'FURIA', 'paiN', 
              'G2', 'Astralis', 'Virtus.pro', 'GamerLegion', '3DMAX',
              'Legacy', 'Liquid', 'HEROIC', 'MIBR', 'Lynn Vision'] # 'Aurora'
map_cols = ['map1', 'map2', 'map3', 'map4', 'map5']
map_score_cols = ['map1_score', 'map2_score', 'map3_score', 'map4_score', 'map5_score']

# drop na
df[map_cols] = df[map_cols].fillna('Not played')
df[map_score_cols] = df[map_score_cols].fillna('No score')
df_clear = df.dropna(subset=['team1_roster', 'team2_roster'])

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

            for map_score in map_score_cols:
                if df_temp[map_score].iloc[x] != 'No score':
                    df_temp[map_score].iloc[x] = str_reverse(df_temp[map_score].iloc[x])
    
    df_final = pd.concat([df_final, df_temp], ignore_index=True)

for x in range(len(df_final['team1_roster'])):
    df_final['team1_roster'].iloc[x] = sort_roster(df_final['team1_roster'].iloc[x])
    df_final['team2_roster'].iloc[x] = sort_roster(df_final['team2_roster'].iloc[x])

# label encoding
# for maps 
maps_encoder = LabelEncoder()
maps = pd.concat([df_final['map1'], df_final['map2'], df_final['map3'], df_final['map4'], df_final['map5']]).unique()
maps_encoder.fit(maps)
col_maps_to_encode = ['map1', 'map2', 'map3', 'map4', 'map5']
for col in col_maps_to_encode:
    df_final[col] = maps_encoder.transform(df_final[col])

# for teams 
teams_encoder = LabelEncoder()
teams = pd.concat([df_final['team1'], df_final['team2'], df_final['winner']]).unique()
teams_encoder.fit(teams)
col_teams_to_encode = ['team1', 'team2', 'winner']
for col in col_teams_to_encode:
    df_final[col] = teams_encoder.transform(df_final[col])

# for rosters
rosters_encoder = LabelEncoder()
rosters = pd.concat([df_final['team1_roster'], df_final['team2_roster']]).unique()
re.fit(rosters)
col_rosters_to_encode = ['team1_roster', 'team2_roster']
for col in col_rosters_to_encode:
    df_final[col] = re.transform(df_final[col])

# for scores
scores_encoder = LabelEncoder()
scores = df_final['match_score'].unique()
scores_encoder.fit(scores)
df_final['match_score'] = scores_encoder.transform(df_final['match_score'])

# reser indexes
df_final.reset_index()

# export cleared csv
export_csv('final_cleared.csv')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Время выполнения: {elapsed_time:.4f} секунд")