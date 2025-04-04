import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data import marathon_df, top_10_per_year, nations_sorted, years

def generate_vis1():
    years = sorted(marathon_df["year"].unique())
    values_line = np.random.randint(50, 200, len(years))
    values_bar1 = np.random.randint(10, 100, len(years))
    values_bar2 = np.random.randint(20, 120, len(years))

    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=years, y=values_line, mode="lines+markers", name="Tendance annuelle"))
    fig_line.update_layout(
        height=300,  
        margin=dict(l=10, r=10, t=10, b=10),  
    )

    fig_bar1 = go.Figure()
    fig_bar1.add_trace(go.Bar(x=years, y=values_bar1, name="Catégorie 1", opacity=0.6))
    fig_bar1.update_layout(
        height=200,  
        margin=dict(l=10, r=10, t=10, b=10),  
    )

    fig_bar2 = go.Figure()
    fig_bar2.add_trace(go.Bar(x=years, y=values_bar2, name="Catégorie 2", opacity=0.6))
    fig_bar2.update_layout(
        height=200,  
        margin=dict(l=10, r=10, t=10, b=10),  
    )

    return fig_line, fig_bar1, fig_bar2
