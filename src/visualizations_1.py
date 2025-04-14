import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data import years



def make_viz1_noSelect(df_courreur,df_temp,df_preci,indexage):

    fig = make_subplots(rows=3, cols=1,row_heights=[0.7, 0.15,0.15])
    result = df_courreur.applymap(lambda td: td.total_seconds() if pd.notnull(td) else None)
    result=result.div(result[indexage], axis=0)
    for indexRes in result.index:
        fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=indexRes),row=1, col=1)


    fig.add_trace(go.Scatter(x=years, y=df_temp.loc['AVG_TEMP_C'], name="Temp. Moy."),row=2, col=1)


    fig.add_trace(go.Bar(x=years, y=df_preci.loc['PRECIP_mm'], name="Precipiation"),row=3, col=1)

    fig.update_layout(
        height=700, 
        margin=dict(l=10, r=10, t=10, b=10),  
    )

    return fig 


def make_viz1_select(df_courreur,df_temp,df_preci,indexage,selection):

    fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, start_cell="bottom-left")

    fig = make_subplots(rows=3, cols=1,row_heights=[0.7, 0.15,0.15])
    result = df_courreur.applymap(lambda td: td.total_seconds() if pd.notnull(td) else None)
    result=result.div(result[indexage], axis=0)
    for indexRes in result.index:
        print(type(indexRes),indexRes)
        if type(indexRes) ==str :
            if indexRes in selection :
                fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=indexRes),row=1, col=1)
        else:
            print(type(indexRes[0]),indexRes[0])
            if indexRes[0] in selection:
                fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=f'{indexRes[0]}-{indexRes[1]}'),row=1, col=1)



    fig.add_trace(go.Scatter(x=years, y=df_temp.loc['AVG_TEMP_C'], name="Temp. Moy."),row=2, col=1)


    fig.add_trace(go.Bar(x=years, y=df_preci.loc['PRECIP_mm'], name="Precipiation"),row=3, col=1)

    fig.update_layout(
        height=700, 
        margin=dict(l=10, r=10, t=10, b=10),  
    )

    return fig