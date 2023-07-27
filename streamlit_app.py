import streamlit as st
import pandas as pd
import numpy as np


from picks import coverage_by_quarter, get_game_versatility, get_versatile_teams, get_versatile_defenders, league_wide_coverages, player_team_coverages, team_coverages, bigs 
# import z_picks

# coverage_by_quarter(season = 'PO')
st.set_page_config(layout="wide")


def page_one():

    st.title("Pick and Roll Defensive Versatility")
    st.title("Around the League")

    # team table

    rs_team = get_versatile_teams(season = 'RS')[['Team_Def', 'screens_guarded', 'PPDA', 'ppda_Rk', 'versatility', 'vers_Rk']].reset_index(drop= True).set_index('Team_Def')
    po_team = get_versatile_teams(season = 'PO')[['Team_Def', 'screens_guarded', 'PPDA', 'ppda_Rk', 'versatility', 'vers_Rk']].reset_index(drop= True).set_index('Team_Def')



    # player table 

    rs_defenders = get_versatile_defenders(season = 'RS')[['Player_SCR_D', 'screens_guarded', 'PPDA', 'ppda_Rk', 'versatility', 'vers_Rk']].reset_index(drop= True).set_index('Player_SCR_D')
    po_defenders = get_versatile_defenders(season = 'PO')[['Player_SCR_D', 'screens_guarded', 'PPDA', 'ppda_Rk', 'versatility', 'vers_Rk']].reset_index(drop= True).set_index('Player_SCR_D')


    table_selection_team = st.radio("Select Season:", ('Regular Season', 'Playoffs'))

    if table_selection_team == 'Regular Season':
            

            st.header('Team Info')
            rs_team = rs_team.style.background_gradient(subset = ['ppda_Rk', 'vers_Rk'], cmap= 'RdYlGn_r')
            rs_team = rs_team.format(precision = 3)
            st.dataframe(rs_team, width = 2000, column_config = {'PPDA' : 'PPDA Allowed',
                                                                'ppda_Rk': 'PPDA Rank',
                                                                'screens_guarded':'Screens Guarded',
                                                                'Team_Def': 'Def. Team',
                                                                'versatility': 'Versatility',
                                                                'vers_Rk': 'Versatility Rank' } )


            st.header('Player Info')

            rs_defenders = rs_defenders.style.background_gradient(subset = ['ppda_Rk', 'vers_Rk'], cmap= 'RdYlGn')
            rs_defenders = rs_defenders.format(precision = 3)
            st.dataframe(rs_defenders, width = 2000, column_config = {'PPDA' : 'PPDA Allowed',
                                                                      'Player_SCR_D': 'Screener Defender',
                                                                      'screens_guarded':'Screens Guarded',
                                                                      'ppda_Rk' : 'PPDA Percentile Rank',
                                                                      'versatility' : 'Versatility',
                                                                      'vers_Rk': 'Versatilty Percentile Rank'} )
        
    elif table_selection_team == 'Playoffs':
            
            st.header('Team Info')

            po_team = po_team.style.background_gradient(subset = ['ppda_Rk', 'vers_Rk'], cmap= 'RdYlGn_r')
            po_team = po_team.format(precision = 3)
            st.dataframe(po_team, width = 2000, column_config = {'PPDA' : 'PPDA Allowed',
                                                                'ppda_Rk': 'PPDA Rank',
                                                                'screens_guarded':'Screens Guarded',
                                                                'Team_Def': 'Def. Team',
                                                                'versatility': 'Versatility',
                                                                'vers_Rk': 'Versatility Rank' } )
            
            st.header('Player Info')

            po_defenders = po_defenders.style.background_gradient(subset = ['ppda_Rk', 'vers_Rk'], cmap= 'RdYlGn')
            po_defenders = po_defenders.format(precision = 3)
            st.dataframe(po_defenders, width = 2000, column_config = {'PPDA' : 'PPDA Allowed',
                                                                      'Player_SCR_D': 'Screener Defender',
                                                                      'screens_guarded':'Screens Guarded',
                                                                      'ppda_Rk' : 'PPDA Percentile Rank',
                                                                      'versatility' : 'Versatility',
                                                                      'vers_Rk': 'Versatilty Percentile Rank'} )

    st.header("League Level Coverages")
    coverages = league_wide_coverages()
    coverages['Freq'] = coverages['Freq'].astype(str) + '%'
    coverages = coverages.style.background_gradient(subset=['PPDA Allowed'], cmap='RdYlGn_r')
    coverages.format(precision = 3)
    st.dataframe(coverages, column_config = {'CoverageType_SCR_D': ''})

def page_two():

    
    nba_teams = {
    'ATL': 'Atlanta Hawks',
    'BKN': 'Brooklyn Nets',
    'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'LA Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
                                }
    
    selected_team = st.sidebar.selectbox('Select an NBA Team', list(nba_teams.keys()))

    st.title(f'{nba_teams[selected_team]} Team Page')


    st.header("Pick and Roll Coverages by Player")

    selected_season = st.radio("Select Season:", ('Regular Season', 'Playoffs'))

    if selected_season == "Playoffs":


        st.header("Pick and Roll Coverages")

        teams = team_coverages(season = 'PO', team = selected_team)
        teams['Frequency'] = teams['Frequency'].astype(str) + '%'
        teams = teams[['CoverageType_SCR_D', 'Screens Guarded', 'Frequency', 'PPDA Allowed']]
        teams = teams.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r').format(precision = 3)

        st.dataframe(teams, hide_index = True, column_config = {'CoverageType_SCR_D' : 'Coverage'})

        player_search_query = st.text_input("Search by Player:", "")
        coverage_type_search_query = st.text_input("Search by Coverage:", "")

        coverage_by_team = player_team_coverages(season = 'PO', team = selected_team)
        coverage_by_team['Frequency'] = coverage_by_team['Frequency'].astype(str) + '%'
        
        # coverage_by_team = coverage_by_team.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r')

        # Filter the DataFrame based on the search query
        coverage_by_team = coverage_by_team[
                                            (coverage_by_team['Player_SCR_D'].str.contains(player_search_query, case=False)) &
                                            (coverage_by_team['CoverageType_SCR_D'].str.contains(coverage_type_search_query, case=False))
                                            ]
        coverage_by_team = coverage_by_team.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r')
        st.dataframe(coverage_by_team, hide_index = True, column_config = {'Player_SCR_D': 'Def. Player',
                                                        'CoverageType_SCR_D' : 'Coverage'})
        
    
    elif selected_season == 'Regular Season':


        st.header("Pick and Roll Coverages")

        teams = team_coverages(season = 'RS', team = selected_team)
        teams['Frequency'] = teams['Frequency'].astype(str) + '%'
        teams = teams[['CoverageType_SCR_D', 'Screens Guarded', 'Frequency', 'PPDA Allowed']]
        teams = teams.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r').format(precision = 3)

        st.dataframe(teams, hide_index = True, column_config = {'CoverageType_SCR_D' : 'Coverage'})

        player_search_query = st.text_input("Search by Player:", "")
        coverage_type_search_query = st.text_input("Search by Coverage:", "")
         
        coverage_by_team = player_team_coverages(season = 'RS', team = selected_team)
        coverage_by_team['Frequency'] = coverage_by_team['Frequency'].astype(str) + '%'
        
        # coverage_by_team = coverage_by_team.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r')

        # Filter the DataFrame based on the search query
        coverage_by_team = coverage_by_team[
                                            (coverage_by_team['Player_SCR_D'].str.contains(player_search_query, case=False)) &
                                            (coverage_by_team['CoverageType_SCR_D'].str.contains(coverage_type_search_query, case=False))
                                            ]
        coverage_by_team = coverage_by_team.style.background_gradient(subset = 'PPDA Allowed', cmap= 'RdYlGn_r').format(precision = 3)
        st.dataframe(coverage_by_team, hide_index = True, column_config = {'Player_SCR_D': 'Def. Player',
                                                        'CoverageType_SCR_D' : 'Coverage'})
        


st.sidebar.title('Pages:')
selection = st.sidebar.selectbox("Go to:", ("League Page", "Team Page"))

if selection == 'League Page':
    page_one()
elif selection == 'Team Page':
    page_two()

st.sidebar.caption(" *All pick and roll information is calculated using direct pick and rolls*")





