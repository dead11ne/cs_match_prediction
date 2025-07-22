# imports 
import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings

COLUMN_GROUPS = {
    'teams': ['team1', 'team2', 'winner'],
    'rosters': ['team1_roster', 'team2_roster'],
    'maps': ['map1', 'map2', 'map3', 'map4', 'map5'],
    'map_scores': ['map1_score', 'map2_score', 'map3_score', 'map4_score', 'map5_score'],
    'score': ['match_score']
    }
MAIN_TEAMS = ['Vitality', 'MOUZ', 'The MongolZ', 'Spirit', 
              'Falcons', 'Natus Vincere', 'FaZe', 'FURIA', 'paiN', 
              'G2', 'Astralis', 'Virtus.pro', 'GamerLegion', '3DMAX',
              'Legacy', 'Liquid', 'HEROIC', 'MIBR', 'Lynn Vision'] # 'Aurora'

# Configure warnings and pandas options
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
pd.options.mode.chained_assignment = None 


# functions
def export_csv(filename: str) -> None:
    """Save DataFrame to CSV file."""
    df_final.to_csv(filename)


def str_reverse(s: str) -> str:
    """Reverse string parts separated by hyphen."""
    if '-' in s:
        temp1, temp2 = s.split("-")
        reversed_str = f'{temp2}-{temp1}'
        return reversed_str
    else: 
        return s


def sort_roster(roster_str: str) -> str:
    """Sort player names in roster string alphabetically."""    
    players = re.findall(r'\w+', roster_str)
    players.sort(key=str.lower)
    sorted_players = ' '.join(players)
    return sorted_players


def label_encode(list_values: list) -> None:
    """Apply label encoding to specified columns in DataFrame."""    
    encoder = LabelEncoder()
    unique_values_for_encode = pd.concat([df_final[col] for col in list_values]).unique()
    encoder.fit(unique_values_for_encode)

    for col in list_values: 
        df_final[col] = encoder.transform(df_final[col])


# dataset
df = pd.read_csv('2024-01-01(correct+id).csv')

# drop na
df[COLUMN_GROUPS['maps']] = df[COLUMN_GROUPS['maps']].fillna('Not played')
df[COLUMN_GROUPS['map_scores']] = df[COLUMN_GROUPS['map_scores']].fillna('No score')
df_clear = df.dropna(subset=COLUMN_GROUPS['rosters'])

# dataset restructuring
df_final = pd.DataFrame([])
for team in MAIN_TEAMS: 
    df_temp = pd.concat([df_clear[df_clear['team1'] == team], df_clear[df_clear['team2'] == team]])

    for x in range(len(df_temp)):
        if df_temp['team1'].iloc[x] != team:
            df_temp['team1'].iloc[x], df_temp['team2'].iloc[x] = df_temp['team2'].iloc[x], df_temp['team1'].iloc[x]
            df_temp['team1_roster'].iloc[x], df_temp['team2_roster'].iloc[x] = df_temp['team2_roster'].iloc[x], df_temp['team1_roster'].iloc[x]
            df_temp['match_score'].iloc[x] = str_reverse(df_temp['match_score'].iloc[x])

            for map_score in COLUMN_GROUPS['map_scores']:
                if df_temp[map_score].iloc[x] != 'No score':
                    df_temp[map_score].iloc[x] = str_reverse(df_temp[map_score].iloc[x])
   
    df_final = pd.concat([df_final, df_temp], ignore_index=True)

# sorting rosters
for x in range(len(df_final['team1_roster'])):
    for team_roster in COLUMN_GROUPS['rosters']:
        df_final[team_roster].iloc[x] = sort_roster(df_final[team_roster].iloc[x])

# label encoding
for key in COLUMN_GROUPS.keys():
    label_encode(COLUMN_GROUPS[key])

# export cleared csv
export_csv('final_cleared.csv')