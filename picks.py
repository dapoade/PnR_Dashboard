import pandas as pd
import numpy as np 

import matplotlib.pyplot as plt




df = pd.read_csv("z_Picks_22_23.csv")

# filter for when the person guarding the screen is a 4 or 5

bigs = (df.query("Position_NBA_SCR_D == 4 or Position_NBA_SCR_D == 5")[[
    "GameDate"
    , "SeasonType"
    , "ChanceId"
    , "Period"
    , "Team_Off"
    , "Team_Def"
    , "Player_BHR_O"
    , "Position_NBA_BHR_O"
    , "Player_BHR_D"
    , "Position_NBA_BHR_D"
    , "Player_SCR_O"
    , "Position_NBA_SCR_O"
    , "Player_SCR_D"
    , "Position_NBA_SCR_D"
    , "IsDirect"
    , "CoverageType_BHR_D"
    , "CoverageType_SCR_D"
    , "ChancePoints"

]]) 

# get dummy variables for screener defense type 

big_defenders = pd.get_dummies(bigs,
                columns = ['CoverageType_SCR_D'])

# rename columns 
big_defenders.rename(columns={
    'CoverageType_SCR_D_blitz': 'blitz',
    'CoverageType_SCR_D_ice': 'ice',
    'CoverageType_SCR_D_none': 'none',
    'CoverageType_SCR_D_show': 'show',
    'CoverageType_SCR_D_soft': 'soft',
    'CoverageType_SCR_D_switch': 'switch',
}, inplace=True) 

# get versatility rating by defender
def get_versatile_defenders(df: df = big_defenders, season : str = 'RS'):

    """
    Function that returns a dataframe of Screener defenders with percent of time spent in each coverage,
    their PPDA allowed, and their versatility rating. 

    Args:
        - df: original dataframe of each pick and roll 
        - season: regular season or playoffs 
    """

    versatile_defenders = (df
                       .query("IsDirect == 1")
                       .groupby(['SeasonType', 'Player_SCR_D'])
                       .apply(lambda x: pd.DataFrame({
                           'screens_guarded' : [x.shape[0]],
                           'blitz' : x['blitz'].sum() / len(x),
                           'ice' : x['ice'].sum() / len(x),
                           'none' : x['none'].sum() / len(x),
                           'show' : x['show'].sum() / len(x),
                           'soft' : x['soft'].sum() / len(x),
                           'switch' : x['switch'].sum() / len(x),
                            'PPDA' : x['ChancePoints'].sum() / len(x) })
                       ) ).reset_index().drop('level_2', axis=1)
    
    # calculate versatility index, drop level 2 column, 
    versatile_defenders['versatility'] = (versatile_defenders[['blitz',
                                                'ice',
                                                'none',
                                                'show',
                                                'soft',
                                                'switch']].apply(lambda row: (row ** 2).sum(), axis = 1))
    
    versatile_defenders['versatility'] = 1 - versatile_defenders['versatility']

    defenders = versatile_defenders.query(f"SeasonType == '{season}' and screens_guarded >= 40").sort_values(by = 'versatility', ascending = False)

    # calculate rank for 
    defenders['ppda_Rk'] = round(100 - defenders['PPDA'].rank(ascending = True, method = 'min', pct = True) * 100, 0).astype('int')
    defenders['vers_Rk'] = round(100 - defenders['versatility'].rank(ascending = False, method = 'min', pct = True) * 100, 0).astype('int')

    return defenders




# calculate  versatility rating by team
def get_versatile_teams(df: df = big_defenders, season: str = 'RS'):
    """
    Function that returns a dataframe of teams with percent of time spent in each coverage,
    their PPDA allowed, and their versatility rating. 

    Args:
        - df: original dataframe of each pick and roll 
        - season: regular season or playoffs 
    """

    versatile_teams = (df
                       .query("IsDirect == 1")
                       .groupby(['SeasonType', 'Team_Def'])
                       .apply(lambda x: pd.DataFrame({
                           'screens_guarded' : [x.shape[0]],
                           'blitz' : x['blitz'].sum() / len(x),
                           'ice' : x['ice'].sum() / len(x),
                           'none' : x['none'].sum() / len(x),
                           'show' : x['show'].sum() / len(x),
                           'soft' : x['soft'].sum() / len(x),
                           'switch' : x['switch'].sum() / len(x),
                           'PPDA' : x['ChancePoints'].sum() / len(x) })) 
                            ).reset_index().drop('level_2', axis=1)

    versatile_teams['versatility'] = (versatile_teams[['blitz',
                                                    'ice',
                                                    'none',
                                                    'show',
                                                    'soft',
                                                    'switch']].apply(lambda row: (row ** 2).sum(), axis = 1))

    versatile_teams['versatility'] = 1 - versatile_teams['versatility']

    teams = versatile_teams.query(f"SeasonType == '{season}' ").sort_values(by = 'versatility', ascending = False)

    teams['ppda_Rk'] = round(teams['PPDA'].rank(ascending = True, method = 'min'), 0).astype('int')
    teams['vers_Rk'] = round(teams['versatility'].rank(ascending = False, method = 'min'), 0).astype('int')

    return teams 






# get versatility by team per game 

def get_game_versatility(df: df = big_defenders, season: str = 'RS'):

    game_agg = (df
        .query("IsDirect == 1 ")
        .groupby(['SeasonType', 'Team_Def', 'GameDate'])
        .apply(lambda x: pd.DataFrame({
            'screens_guarded' : [x.shape[0]],
            'blitz' : x['blitz'].sum() / len(x),
            'ice' : x['ice'].sum() / len(x),
            'none' : x['none'].sum() / len(x),
            'show' : x['show'].sum() / len(x),
            'soft' : x['soft'].sum() / len(x),
            'switch' : x['switch'].sum() / len(x),
            'PPDA' : x['ChancePoints'].sum() / len(x) })) 
        .reset_index()
        )

    # versatility rating by game, based on coverage type 
    game_agg['versatility'] = (game_agg[['blitz',
                                        'ice',
                                        'none',
                                        'show',
                                        'soft',
                                        'switch']].apply(lambda row: (row ** 2).sum(), axis = 1))
    # make higher versatility better by subtracting 1 
    game_agg['versatility'] = 1 - game_agg['versatility']

    final_df = game_agg.query(f"SeasonType == '{season}' ")

    return final_df




def coverage_by_quarter(df: df = big_defenders, season : str = 'RS'):

    """Returns league level pick and roll coverage frequency and points per direct attempt allowed by season tyoe"""

    vers_quarter = (df
    .query("IsDirect == 1 ")
    .groupby(['SeasonType', 'Period' ])
    .apply(lambda x: pd.DataFrame({
        'screens_guarded' : [x.shape[0]],
        'blitz' : x['blitz'].sum() / len(x),
        'ice' : x['ice'].sum() / len(x),
        'none' : x['none'].sum() / len(x),
        'show' : x['show'].sum() / len(x),
        'soft' : x['soft'].sum() / len(x),
        'switch' : x['switch'].sum() / len(x),
        'PPDA' : x['ChancePoints'].sum() / len(x) })) 
    .reset_index().drop('level_2', axis = 1)
    )

    vers_quarter = vers_quarter.query(f"SeasonType == '{season}' and screens_guarded > 500 ")

    return vers_quarter

def league_wide_coverages(df: df = bigs):
    """ Returns data frame of the frequency and points allowed for each coverage on the league level"""

    coverage_types = (bigs
        .query("IsDirect == 1")
        .groupby(['SeasonType', 'CoverageType_SCR_D'])
        .apply(lambda x: pd.DataFrame({
            'PPDA Allowed' : [x['ChancePoints'].sum() / len(x)],
        }))
        ).reset_index().drop('level_2', axis = 1)

    freq = bigs.query("IsDirect == 1").groupby(['SeasonType', 'CoverageType_SCR_D']).size().reset_index(name='Frequency')
    freq['Freq'] = round((freq['Frequency'] / freq.groupby('SeasonType')['Frequency'].transform('sum')) * 100, 0)
    freq = freq.drop(columns=['Frequency'])

    coverages = pd.merge(freq, coverage_types, on = ['SeasonType', 'CoverageType_SCR_D'])
    final_coverages = coverages.set_index(['CoverageType_SCR_D', 'SeasonType']).sort_index(ascending = False)
    # final_coverages['Freq'] = final_coverages['Freq'] + '%'

    return final_coverages

def player_team_coverages(df: df = bigs, season: str = 'RS', team: str = 'MEM'):

    """ Returns a dataframe of pick and roll coverage type frequency and points per direct attempt allowed by player on a specified team"""

    coverage_types = (df
            .query(f"IsDirect == 1 and Team_Def == '{team}' and SeasonType == '{season}'")
            .groupby(['SeasonType', 'CoverageType_SCR_D', 'Player_SCR_D'])
            .apply(lambda x: pd.DataFrame({
                'Screens Guarded' : [x.shape[0]],
                'PPDA Allowed' : [x['ChancePoints'].sum() / len(x)],
            }))
            ).reset_index().drop('level_3', axis = 1 )
    
    coverage_types['Frequency'] = round(coverage_types['Screens Guarded'] / coverage_types.groupby(['SeasonType', 'Player_SCR_D'])['Screens Guarded'].transform('sum') * 100, 0)
    coverage_types_final = coverage_types[['Player_SCR_D', 'CoverageType_SCR_D', 'Screens Guarded','Frequency', 'PPDA Allowed']]

    return coverage_types_final


def team_coverages(df: df = bigs, season: str = 'RS', team: str = 'MEM'):

    """ Returns a dataframe of pick and roll coverage type frequency and points per direct attempt allowed by a specified team"""

    coverage_types = (df
            .query(f"IsDirect == 1 and Team_Def == '{team}' and SeasonType == '{season}'")
            .groupby(['SeasonType', 'CoverageType_SCR_D'])
            .apply(lambda x: pd.DataFrame({
                'Screens Guarded' : [x.shape[0]],
                'PPDA Allowed' : [x['ChancePoints'].sum() / len(x)],
            }))
            ).reset_index().drop('level_2', axis = 1 )
    
    coverage_types['Frequency'] = round(coverage_types['Screens Guarded'] / coverage_types.groupby(['SeasonType'])['Screens Guarded'].transform('sum') * 100, 0)
    coverage_types_final = coverage_types[['CoverageType_SCR_D', 'Screens Guarded','Frequency', 'PPDA Allowed']]

    return coverage_types_final





    








    