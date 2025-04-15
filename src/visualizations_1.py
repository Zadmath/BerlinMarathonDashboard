import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data import years




def initSubplot(df_temp,df_preci):

    fig = make_subplots(rows=3, cols=1,vertical_spacing=0.09,row_heights=[0.6, 0.2,0.2],subplot_titles=("Temps moyen indexé", "Température en °C", "Précipitation en mm"))
    fig.update_layout(
        height=700, 
        margin=dict(l=10, r=10, t=30, b=10),
        
    )
    fig.add_shape(
    type="line",
    x0=0, x1=1,  # en coordonnées relatives pour tout l'axe X
    y0=1, y1=1,  # valeur de référence Y
    xref="paper", yref="y",
    line=dict(
        color="grey",
        width=2,
        dash="dashdot"  # options : 'dash', 'dot', 'dashdot'
    ),
    )
    #fig.update_yaxes(title_text="Temps moyen indexé", row=1, col=1)

    fig.add_trace(go.Scatter(x=years, y=df_temp.loc['AVG_TEMP_C'], name="Temp. Moy.",showlegend=False,line_color='red'),row=2, col=1)
    #fig.update_yaxes(title_text="Température en °C", row=2, col=1)

    fig.add_trace(go.Bar(x=years, y=df_preci.loc['PRECIP_mm'], name="Precipiation",showlegend=False,marker_color='blue'),row=3, col=1)
    #fig.update_yaxes(title_text===="Précipitation en mm", row=3, col=1)

    return fig 
def make_viz1_noSelect(df_courreur,df_temp,df_preci,indexage):

    fig = initSubplot(df_temp,df_preci)
    result = df_courreur.applymap(lambda td: td.total_seconds() if pd.notnull(td) else None)
    result=result.div(result[indexage], axis=0)
    for indexRes in result.index:
        fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=indexRes),row=1, col=1)


    return fig 


def make_viz1_select(df_courreur,df_temp,df_preci,indexage,selection):

    fig = initSubplot(df_temp,df_preci)
    result = df_courreur.applymap(lambda td: td.total_seconds() if pd.notnull(td) else None)
    result=result.div(result[indexage], axis=0)
    for indexRes in result.index:
        if type(indexRes) ==str :
            if indexRes in selection :
                fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=indexRes),row=1, col=1)
        else:
            if indexRes[0] in selection:
                fig.add_trace(go.Scatter(x=result.columns, y=result.loc[indexRes],name=f'{indexRes[0]}-{indexRes[1]}'),row=1, col=1)
    

    return fig
