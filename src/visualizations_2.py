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
    # Vérifier si fig est un dictionnaire et le convertir en Figure si nécessaire
    if isinstance(fig, dict):
        fig = go.Figure(fig)

    # Vérifier si des points ont été sélectionnés
    if not points or not isinstance(points, list) or len(points) == 0:
        return fig

    # Obtenir les intervalles de temps sélectionnés
    selected_times = [time_counts.index[point["pointIndex"]] for point in points]
    if not selected_times:
        return fig

    # Filtrer les coureurs dans cet intervalle de temps
    selected_df = df[df['tps_fin_rounded'].isin(selected_times)]

    # Mettre à jour le pie chart (sexe)
    sex_counts = selected_df['sex'].value_counts()
    sex_dict = {'M': 0, 'W': 0}
    for sex, count in sex_counts.items():
        if sex in sex_dict:
            sex_dict[sex] = count
    sex_values = [sex_dict['M'], sex_dict['W']]
    sex_labels = ["Hommes", "Femmes"]

    # Ajouter un pourcentage au pie chart
    total = sum(sex_values)
    percentages = [f"{(v/total*100):.1f}%" if total > 0 else "0%" for v in sex_values]
    hover_texts = [f"{l}: {v} ({p})" for l, v, p in zip(sex_labels, sex_values, percentages)]

    fig.update_traces(
        values=sex_values,
        labels=sex_labels,
        hoverinfo='text',
        hovertext=hover_texts,
        selector=dict(type='pie')
    )

    # Mettre à jour le bar chart (nationalités)
    nation_counts = selected_df['nation'].value_counts().head(15)
    if nation_counts.empty:
        # Si aucune donnée n'est disponible, afficher un message par défaut
        fig.update_traces(
            x=["Aucune donnée"],
            y=[0],
            hovertemplate='Aucune donnée disponible<extra></extra>',
            selector=dict(type='bar', row=2, col=2)
        )
    else:
        # Mettre à jour les données des nationalités
        fig.update_traces(
            x=nation_counts.index,
            y=nation_counts.values,
            hovertemplate='%{x}: %{y} coureurs<extra></extra>',
            selector=lambda trace: trace.customdata and trace.customdata[0] == "nationality"
        )

    # Mettre à jour le titre avec le nombre de coureurs sélectionnés
    selection_count = len(selected_df)
    formatted_times = [str(td).split('.')[0] for td in selected_times]
    formatted_times = [time.split(' ')[2] for time in formatted_times]
    time_range = f"{formatted_times[0]} - {formatted_times[-1]}"

    # Supprimer explicitement toutes les annotations existantes
    fig.layout.annotations = []

    # Ajouter une nouvelle annotation avec une position ajustée
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.0,  # Ajustement de la position verticale pour éviter la superposition
        showarrow=False,
        text=f"Sélection: {time_range} - {selection_count} coureurs",
        bgcolor="white",
        bordercolor="black",
        font=dict(size=16)
    )
    
    # on ajoute les titres du pie chart et du bar chart
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.15, y=-0.05,
        showarrow=False,
        text="Répartition par sexe",
        font=dict(size=16)
    )
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.85, y=0.35,
        showarrow=False,
        text="Top nationalités",
        font=dict(size=16)
    )
    
    # Mettre à jour le titre bar chart de distribution des temps d'arrivée
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        text="Distribution des temps d'arrivée",
        font=dict(size=16)
    )
        # Verrouiller les dimensions des graphiques pour éviter les changements de taille
    fig.update_layout(
        autosize=False,
        height=800,
        width=1000,
        margin=dict(t=100, b=50, l=50, r=50)  # Maintenir les marges constantes
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
        row_heights=[0.5, 0.5]  # Increased height for the bottom row
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
        margin=dict(t=50, b=50, l=50, r=50)
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

    fig.add_trace(go.Bar(
        x=initial_nation_counts.index,
        y=initial_nation_counts.values,
        name="Top nationalités",
        marker_color='#22AA99',
        textposition='auto',
        customdata=["nationality"] * len(initial_nation_counts)  # Ajout clé
    ), row=2, col=2)

    # Désactiver la sélection sur le graphique des nationalités
    fig.update_traces(
        selector=dict(type='bar', row=2, col=2),
        marker=dict(opacity=0.8),
        hoverinfo='x+y',
        selectedpoints=None  # Désactiver la sélection
    )
    

    # Verrouiller les dimensions des graphiques pour éviter les changements de taille
    fig.update_layout(
        autosize=True,  # Allow the figure to resize dynamically
        height=900,  # Increased height for better visualization
        width=1500,  # Increased width for better visualization
        margin=dict(t=50, b=50, l=50, r=50)  # Adjusted margins for more space
    )

    fig.update_xaxes(title_text="Nationalité", tickangle=45, row=2, col=2)
    fig.update_yaxes(title_text="Nombre de coureurs", row=2, col=2)

    return fig