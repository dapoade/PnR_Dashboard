import pandas as pd
import numpy as np 

import matplotlib.pyplot as plt
import seaborn as sns


# plot defender versatility vs ppda allowed 
def plot_defenders(df: df):

    x = df['versatility']
    y = df['PPDA']

    ax = sns.regplot(x = x, y =  y, scatter_kws={"color": "black"}, line_kws={"color": "red"}, ci = None )
    ax.set(xlabel = 'Versatility Rating by Player', ylabel= 'Points per Direct Attempt Allowed', title= f"Player Versatility vs Effectiveness -- {df['SeasonType'].iloc[0]} ")
    
    return ax


# plot team versatility vs ppda allowed 
def plot_teams(df: df):

    x = df['versatility']
    y = df['PPDA']

    ax = sns.regplot(x = x, y =  y, scatter_kws={"color": "black"}, line_kws={"color": "red"}, ci = None )
    ax.set(xlabel = 'Versatility Rating by Team', ylabel= 'Points per Direct Attempt Allowed', title= f"Team Versatility vs Effectiveness -- {df['SeasonType'].iloc[0]}")

    return ax 


# plot versatility by team per game vs ppda allowed

def plot_game_versatility(df: df):

    x = df['versatility']
    y = df['PPDA']

    ax = sns.regplot(x = x, y = y, scatter_kws={"color": "black"}, line_kws={"color": "red"} )
    ax.set(xlabel = 'Versatility Rating by Game', ylabel= 'Points per Direct Attempt Allowed', title= f"Versatility vs Effectiveness -- {df['SeasonType'].iloc[0]} ")

    return ax 


