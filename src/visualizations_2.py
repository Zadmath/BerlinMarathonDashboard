import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import timedelta
from data import df, initial_sex_values, initial_nation_counts, time_counts, time_labels


def update_plots(trace, points, selector, fig):
    # Ensure fig is a valid Plotly figure
    if isinstance(fig, dict):
        fig = go.Figure(fig)

    # Check if points are selected
    if not points or not isinstance(points, list) or len(points) == 0:
        return fig

    # Get selected time intervals
    selected_times = [time_counts.index[point["pointIndex"]] for point in points]
    if not selected_times:
        return fig

    # Filter runners based on selected times
    selected_df = df[df['tps_fin_rounded'].isin(selected_times)]

    # Update pie chart (sex distribution)
    sex_counts = selected_df['sex'].value_counts()
    sex_values = [sex_counts.get('M', 0), sex_counts.get('W', 0)]
    sex_labels = ["Hommes", "Femmes"]

    # Add percentages and hover text for the pie chart
    total = sum(sex_values)
    percentages = [f"{(v / total * 100):.1f}%" if total > 0 else "0%" for v in sex_values]
    hover_texts = [f"{l}: {v} ({p})" for l, v, p in zip(sex_labels, sex_values, percentages)]

    fig.update_traces(
        values=sex_values,
        labels=sex_labels,
        hoverinfo='text',
        hovertext=hover_texts,
        selector=dict(type='pie')
    )

    # Update bar chart (nationalities)
    nation_counts = selected_df['nation'].value_counts().head(15)
    if nation_counts.empty:
        fig.update_traces(
            x=["Aucune donnée"],
            y=[0],
            hovertemplate='Aucune donnée disponible<extra></extra>',
            selector=dict(name="Top nationalités")
        )
    else:
        hover_texts = [f"{nation}: {count} coureurs" for nation, count in zip(nation_counts.index, nation_counts.values)]
        fig.update_traces(
            x=nation_counts.index,
            y=nation_counts.values,
            hovertext=hover_texts,
            hoverinfo='text',
            marker=dict(color='#22AA99'),
            selector=dict(name="Top nationalités")
        )

    # Format the time range to remove "0 days"
    formatted_times = [str(td).split(' ')[-1] for td in selected_times]
    time_range = f"{formatted_times[0]} - {formatted_times[-1]}"

    # Update annotations
    selection_count = len(selected_df)
    fig.layout.annotations = []  # Clear existing annotations
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.0,
        showarrow=False,
        text=f"Sélection: {time_range} - {selection_count} coureurs",
        font=dict(size=16)
    )

    return fig

def create_dashboard():
    # Convertir les chaînes de caractères en timedelta
    time_labels_converted = pd.to_timedelta(time_labels)

    # Convertir les temps en minutes
    time_in_minutes = [int(t.total_seconds() // 60) for t in time_labels_converted]

    # Fonction pour formater les minutes en HH:MM
    def format_minutes(minutes):
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02}:{mins:02}"
    formatted_time_labels = [format_minutes(t) for t in time_in_minutes]


    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"colspan": 2}, None],
               [{"type": "domain"}, {}]],
        subplot_titles=("Distribution des temps d'arrivée", 
                        "Répartition par sexe", 
                        "Top nationalités"),
        vertical_spacing=0.1,  # Reduced spacing for better use of space
        horizontal_spacing=0.2,
        row_heights=[0.7, 0.3]  # Increased height for the bottom row
    )

    histogram = go.Bar(
        x=[format_minutes(t) for t in time_in_minutes],  # Formater les temps en HH:MM
        y=time_counts.values,
        name="",
        marker_color='royalblue',
        hovertemplate='Temps: %{x}<br>Nombre de coureurs: %{y}',
    )

    fig.add_trace(histogram, row=1, col=1)

    fig.add_annotation(
    text=(
        '<span style="line-height:1.5;">'
        'Sélectionnez une plage de temps sur le graphique<br>'
        'pour voir la répartition par sexe et nationalité'
        '</span>'
    ),
    xref="paper", yref="paper",
    x=0.5, y=0.95,
    showarrow=False,
    font=dict(size=13.5, family="Arial", color="black"),
    bgcolor="white",
    align="center"
)

    fig.update_layout(
        autosize=True,
        height=1000,  # Increased overall height for better visualization
        width=1500,
        margin=dict(t=50, b=50, l=50, r=50),
        dragmode="select",  # Enable selection mode
        selectdirection="h",  # Restrict selection to horizontal direction
        hovermode="closest",
        showlegend=False  # Remove the legend
    )

    fig.update_xaxes(
        title_text="Temps d'arrivée (HH:MM)",
        tickvals=formatted_time_labels[::5],  # Adjusted tick frequency
        ticktext=formatted_time_labels[::5],
        row=1, col=1,
        tickangle=45
    )
    fig.update_yaxes(title_text="Nombre de coureurs", row=1, col=1)

    fig.add_trace(go.Pie(
        labels=["Hommes", "Femmes"],
        values=initial_sex_values,
        name="Répartition par sexe",
        marker_colors=['#3366CC', '#FF6347'],
        textinfo='percent+label',
        hole=0.2,
    ), row=2, col=1)
    fig.update_layout(
        autosize=True,
        height=1000,  # Increased overall height for better visualization
        width=1500,
        margin=dict(t=50, b=50, l=50, r=50),
        dragmode="select",  # Enable selection mode
        selectdirection="h",  # Restrict selection to horizontal direction
        hovermode="closest"
    )
    fig.add_trace(go.Bar(
        x=initial_nation_counts.index,
        y=initial_nation_counts.values,
        name="Top nationalités",  # Use name for identification
        marker_color='#22AA99',
        textposition='auto',
        hovertemplate='%{x}: %{y} coureurs<extra></extra>',
        customdata=["nationality"] * len(initial_nation_counts)  # Ajout clé
    ), row=2, col=2)

    # Désactiver la sélection sur le graphique des nationalités
    fig.update_traces(
        selector=dict(name="Top nationalités"),
        marker=dict(opacity=0.8),
        hoverinfo='x+y',
        selectedpoints=None  # Désactiver la sélection
    )
    

    # Verrouiller les dimensions des graphiques pour éviter les changements de taille
    fig.update_layout(
        autosize=True,  # Allow the figure to resize dynamically
        height=800,  # Increased height for better visualization
        width=1300,  # Increased width for better visualization
        margin=dict(t=50, b=50, l=0, r=50)  # Adjusted margins for more space
    )

    fig.update_xaxes(title_text="Nationalité", tickangle=45, row=2, col=2)
    fig.update_yaxes(title_text="Nombre de coureurs", row=2, col=2)

    return fig