# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
'''
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from visualizations_1 import *
from visualizations_2 import create_dashboard, update_plots
from visualizations_3 import generate_marathon_chart
import pandas as pd
from data import df
import preprocess

# Initialisation de l'application Dash
app = dash.Dash(__name__)
app.title = 'Project | INF8808'


df_temp,df_preci=preprocess.preprocess_meteo(pd.read_csv('./src/assets/data/Berlin_Marathon_weather_data_since_1974.csv'))
dict_All_viz1=preprocess.process_data_courreur_viz1(df)
# Ajout de styles CSS globaux
app.css.append_css({
    "external_url": "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
})

# Calculer le temps d'arrivée moyen
avg_finish_time_seconds = df['tps_fin_rounded'].mean().total_seconds()
hours = int(avg_finish_time_seconds // 3600)
minutes = int((avg_finish_time_seconds % 3600) // 60)
seconds = int(avg_finish_time_seconds % 60)
avg_finish_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
# Nombre total de participants
total_participants = 779564

# Layout de l'application
app.layout = html.Div([
    html.Div([
        # Ajout du logo avec fond blanc collé au titre
        html.Img(
            src="./assets/images/logo_dashboard.png",
            style={
                "background-color": "white",
                "padding": "10px",
                "border-radius": "8px",
                "width": "200px",
                "height": "auto",
                "margin-right": "10px",  # Espacement entre le logo et le titre
                "vertical-align": "middle"
            }
        ),
        html.H1(
            "Dashboard Marathon de Berlin",
            style={
                "display": "inline-block",
                "vertical-align": "middle",
                "margin-bottom": "20px",
                "animation": "fadeInDown 1s"
            }
        )
    ], style={"text-align": "center"}),

    # Phrase explicative
    html.P(
        "Explorez les données du Marathon de Berlin (1999-2023) à travers des visualisations interactives. "
        "Sélectionnez des plages de temps, des catégories ou des genres pour analyser les performances des coureurs.",
        style={
            "text-align": "center",
            "font-size": "16px",
            "margin-bottom": "30px",
            "color": "#555",
            "animation": "fadeInUp 1s"
        }
    ),

    # Onglets pour les visualisations
    dcc.Tabs([
        dcc.Tab(label="Temps moyen indexé et météo (Visualisation 1)", children=[
            html.Div([
                html.Div([
                    html.P(
                        [
                            html.Span("Graphique : Temps moyen indexé", style={"font-weight": "bold", "font-size": "18px", "color": "#333"}),
                            html.Br(),
                            html.Span("- Temps moyen indexé : ", style={"font-weight": "bold", "color": "#007BFF"}),
                            "Chaque courbe représente le temps moyen de course d’un groupe de coureurs (Top 10, Pros, Semi-pro, Passionnés, Amateurs), rapporté à une valeur de référence égale à 1.",
                            html.Br(),
                            html.Span("- Ligne pointillée (index 1) : ", style={"font-weight": "bold", "color": "#007BFF"}),
                            "Sert de base de comparaison.",
                            html.Br(),
                            html.Span("  · ", style={"color": "#555"}), 
                            html.Span("Une valeur au-dessus de 1 ", style={"font-weight": "bold", "color": "#FF6347"}), 
                            "indique un temps moyen plus lent que la moyenne globale.",
                            html.Br(),
                            html.Span("  · ", style={"color": "#555"}), 
                            html.Span("Une valeur en dessous de 1 ", style={"font-weight": "bold", "color": "#22AA99"}), 
                            "indique un temps moyen plus rapide que la moyenne globale.",
                            html.Br(),
                            html.Span("- Comparaison par groupe : ", style={"font-weight": "bold", "color": "#007BFF"}),
                            "Plus une courbe est élevée, plus le groupe correspondant met de temps à finir la course, relativement à la moyenne globale.",
                            html.Br(),
                            html.Span("- Évolution temporelle : ", style={"font-weight": "bold", "color": "#007BFF"}),
                            "L’axe horizontal indique les années. L’évolution des courbes montre comment la performance relative de chaque groupe a changé au fil du temps.",
                            html.Br(), html.Br(),
                        ],
                        style={
                            "font-size": "16px",
                            "color": "#555",
                            "margin-bottom": "20px",
                            "line-height": "1.6",
                            "background-color": "#f9f9f9",
                            "padding": "15px",
                            "border-radius": "8px",
                            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                        }
                    )
                ], style={"flex": "1", "padding": "20px"}),

                html.Div([
                    html.H3(
                        "Évolution du temps moyen de courses indexé sur 1999",
                        style={
                            "text-align": "center",
                            "color": "#333",
                            "font-size": "24px",
                            "font-weight": "bold",
                            "margin-bottom": "20px",
                            "font-family": "Arial, sans-serif"
                        }
                    ),
                    html.Label(
                        "Sélectionnez la catégorisation :",
                        style={
                            "font-weight": "bold",
                            "margin-bottom": "10px",
                            "text-align": "left",
                            "display": "block",
                            "font-size": "18px",
                            "color": "#555",
                            "font-family": "Arial, sans-serif"
                        }
                    ),
                    dcc.RadioItems(
                        id='radio-vis1',
                        options=[
                            dict(label='Par niveaux', value='Par niveaux'),
                            dict(label='Par sex', value='Par sex'),
                            dict(label='Par age', value='Par age'),
                            dict(label='Par age & sex', value='Par sex-age'),
                        ],
                        value='Par niveaux',
                        style={
                            "font-size": "16px",
                            "color": "#333",
                            "font-family": "Arial, sans-serif",
                            "margin-bottom": "20px"
                        }
                    ),
                    html.Label(
                        "Sélectionnez les catégories d'âges :",
                        style={
                            "font-weight": "bold",
                            "margin-bottom": "10px",
                            "text-align": "left",
                            "display": "block",
                            "font-size": "18px",
                            "color": "#555",
                            "font-family": "Arial, sans-serif"
                        }
                    ),
                    dcc.Checklist(
                        id='age-checklist',
                        options=[
                            {"label": "20", "value": "20"},
                            {"label": "25", "value": "25"},
                            {"label": "30", "value": "30"},
                            {"label": "35", "value": "35"},
                            {"label": "40", "value": "40"},
                            {"label": "45", "value": "45"},
                            {"label": "50", "value": "50"},
                            {"label": "55", "value": "55"},
                            {"label": "60", "value": "60"},
                            {"label": "65", "value": "65"},
                            {"label": "70", "value": "70"},
                            {"label": "75", "value": "75"},
                            {"label": "80", "value": "80"}
                        ],
                        inline=True,
                        value=["30", "40"],
                        style={
                            "font-size": "16px",
                            "color": "#333",
                            "font-family": "Arial, sans-serif",
                            "margin-bottom": "20px"
                        }
                    ),
                    dcc.Graph(
                        id='vis1',
                        figure=make_viz1_noSelect(dict_All_viz1["Par niveaux"], df_temp, df_preci, 1999),
                        style={
                            "height": "700px",
                            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                            "border-radius": "8px",
                        }
                    ),
                ], style={"flex": "3", "padding": "20px", "background-color": "#f9f9f9", "border-radius": "10px", "margin-left": "20px"})
            ], style={"display": "flex", "flex-direction": "row"})
        ]),

        dcc.Tab(label="Répartition par sexe et nationalité (Visualisation 2)", children=[
            html.Div([
                html.Div([
                    html.P(
                        [
                            html.Span("Visualisation 2 : Répartition par sexe et nationalité", style={"font-weight": "bold", "font-size": "18px", "color": "#333"}),
                            html.Br(), html.Br(),
                            html.Span("Cette visualisation vous permet de ", style={"color": "#555"}),
                            html.Span("sélectionner une plage de temps ", style={"font-weight": "bold", "color": "#007BFF"}),
                            html.Span("dans l'histogramme des temps de course pour explorer :", style={"color": "#555"}),
                            html.Br(),
                            html.Span("1. ", style={"font-weight": "bold", "color": "#FF6347"}), 
                            "La proportion d'hommes et de femmes ayant participé dans cette plage de temps.",
                            html.Br(),
                            html.Span("2. ", style={"font-weight": "bold", "color": "#22AA99"}), 
                            "Les nationalités les plus représentées dans cette plage de temps.",
                            html.Br(), html.Br(),
                            html.Span("Insights clés : ", style={"font-weight": "bold", "font-size": "16px", "color": "#333"}),
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            "Une majorité des meilleurs temps sont réalisés par des ",
                            html.Span("coureurs d'Afrique de l'Est", style={"font-weight": "bold", "color": "#FF6347"}),
                            html.Span(".", style={"color": "#555"}),
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            html.Span("Les hommes dominent généralement les meilleures performances.", style={"color": "#555"}),
                            html.Br(), html.Br(),
                        ],
                        style={
                            "font-size": "16px",
                            "color": "#555",
                            "margin-bottom": "20px",
                            "line-height": "1.6",
                            "background-color": "#f9f9f9",
                            "padding": "15px",
                            "border-radius": "8px",
                            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                        }
                    )
                ], style={"flex": "1", "padding": "20px"}),

                html.Div([
                    html.H3("Répartition des nationalités et du sexe pour une plage de temps", style={"text-align": "center", "color": "#333"}),
                    dcc.Graph(
                        id="vis2",
                        figure=create_dashboard(),
                        style={
                            "height": "1000px",  # Increased height
                            "width": "100%",  # Make the graph occupy the full width
                            "box-shadow": "3px 4px 3px rgba(0, 0, 0, 0.1)",
                            "border-radius": "8px",
                            "margin": "0 auto"  # Center the graph horizontally
                        }
                    )
                ], style={
                    "flex": "3",
                    "padding": "80px",  # Increased padding for better spacing
                    "background-color": "#f9f9f9",
                    "border-radius": "10px",
                    "margin": "0 auto",  # Center the entire box horizontally
                    "width": "90%",  # Increased width of the box
                    "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                })
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "center"})
        ]),

        dcc.Tab(label="Évolution des nationalités dans le Top 10 (Visualisation 3)", children=[
            html.Div([
                html.Div([
                    html.P(
                        [
                            html.Span("Visualisation 3 : Évolution des nationalités dans le Top 10", style={"font-weight": "bold", "font-size": "18px", "color": "#333"}),
                            html.Br(), html.Br(),
                            html.Span("Cette visualisation met en lumière ", style={"color": "#555"}),
                            html.Span("l'évolution des nationalités ", style={"font-weight": "bold", "color": "#007BFF"}),
                            html.Span("dans le Top 10 du Marathon de Berlin, en fonction du genre et de la catégorie d'âge :", style={"color": "#555"}),
                            html.Br(),
                            html.Span("1. ", style={"font-weight": "bold", "color": "#FF6347"}), 
                            "Le Kenya domine largement le Top 10, avec des performances exceptionnelles.",
                            html.Br(),
                            html.Span("2. ", style={"font-weight": "bold", "color": "#22AA99"}), 
                            "L'Éthiopie a réalisé une percée significative, notamment chez les femmes.",
                            html.Br(),
                            html.Span("3. ", style={"font-weight": "bold", "color": "#007BFF"}), 
                            "Les catégories plus âgées sont souvent dominées par des coureurs allemands, bénéficiant de l'avantage d'être à domicile.",
                            html.Br(), html.Br(),
                            html.Span("Insights clés : ", style={"font-weight": "bold", "font-size": "16px", "color": "#333"}),
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            "Les performances des coureurs d'Afrique de l'Est restent inégalées dans les catégories élites.",
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            html.Span("Les coureurs locaux dominent les catégories d'âge plus avancé, montrant une forte participation allemande.", style={"color": "#555"}),
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            "Cliquez sur le point représentant ", 
                            html.Span("Eliud Kipchoge", style={"font-weight": "bold", "color": "#FF6347"}), 
                            " pour observer sa domination depuis 2013.",
                            html.Br(),
                            html.Span("· ", style={"color": "#555"}), 
                            "En sélectionnant la catégorie ", 
                            html.Span("femme", style={"font-weight": "bold", "color": "#22AA99"}), 
                            ", cliquez sur ", 
                            html.Span("Assefa Tigst", style={"font-weight": "bold", "color": "#FF6347"}), 
                            " pour découvrir la nouvelle recordwoman.",
                            html.Br(), html.Br(),
                        ],
                        style={
                            "font-size": "16px",
                            "color": "#555",
                            "margin-bottom": "20px",
                            "line-height": "1.6",
                            "background-color": "#f9f9f9",
                            "padding": "15px",
                            "border-radius": "8px",
                            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                        }
                    )
                ], style={"flex": "1", "padding": "20px"}),  # Reduced flex ratio for the text

                html.Div([
                    html.H3(
                        "Évolution des Nationalités dans le Top 10 du Marathon de Berlin (1999-2023)",
                        style={"text-align": "center", "color": "#333", "margin-bottom": "20px"}
                    ),
                    html.Div([
                        html.Label("Sélectionnez le genre :", style={"font-weight": "bold", "margin-bottom": "5px", "text-align": "center", "display": "block"}),
                        dcc.Dropdown(
                            id="gender-dropdown",
                            options=[
                                {"label": "Tous", "value": "ALL"},
                                {"label": "Hommes", "value": "M"},
                                {"label": "Femmes", "value": "W"}
                            ],
                            value="ALL",
                            style={"width": "50%", "margin": "0 auto 20px auto", "box-shadow": "none", "border-radius": "5px"}
                        ),
                        html.Label("Sélectionnez la catégorie d'âge :", style={"font-weight": "bold", "margin-bottom": "5px", "text-align": "center", "display": "block"}),
                        dcc.Dropdown(
                            id="category-dropdown",
                            options=[
                                {"label": "Tous", "value": "ALL"},
                                {"label": "20", "value": "20"},
                                {"label": "25", "value": "25"},
                                {"label": "30", "value": "30"},
                                {"label": "35", "value": "35"},
                                {"label": "40", "value": "40"},
                                {"label": "45", "value": "45"},
                                {"label": "50", "value": "50"},
                                {"label": "55", "value": "55"},
                                {"label": "60", "value": "60"},
                                {"label": "65", "value": "65"},
                                {"label": "70", "value": "70"},
                                {"label": "75", "value": "75"},
                                {"label": "80", "value": "80"}
                            ],
                            value="ALL",
                            clearable=False,
                            style={"width": "50%", "margin": "0 auto 20px auto", "box-shadow": "none", "border-radius": "5px"}
                        ),
                    ], style={"text-align": "center"}),

                    html.Div([
                        html.Span("● Hommes", style={"color": "blue", "font-size": "16px", "margin-right": "20px"}),
                        html.Span("● Femmes", style={"color": "red", "font-size": "16px"}),
                    ], style={"margin-bottom": "20px", "text-align": "center"}),

                    html.Div([
                        html.Div(id="selected-runner-info", style={"marginTop": "10px", "fontWeight": "bold", "margin-bottom": "10px"}),
                        html.Button(
                            "Désélectionner le coureur",
                            id="deselect-button",
                            n_clicks=0,
                            style={
                                "margin-bottom": "14px",
                                "background-color": "#007BFF",
                                "color": "white",
                                "border": "none",
                                "border-radius": "5px",
                                "padding": "10px 20px",
                                "cursor": "pointer",
                                "transition": "background-color 0.3s, transform 0.3s",
                            },
                            className="hover-button"
                        ),
                        dcc.Graph(
                            id="matrix-chart",
                            config={"displayModeBar": True},
                            clear_on_unhover=True,
                            clickData=None,
                            figure=generate_marathon_chart("ALL", None, "ALL"),
                            style={
                                "height": "70vh",
                                "width": "100%",
                                "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                                "border-radius": "8px",
                            }
                        )
                    ], style={"width": "100%", "display": "flex", "flex-direction": "column", "align-items": "center"})
                ], style={"flex": "4", "padding": "20px", "background-color": "#f9f9f9", "border-radius": "10px", "margin-left": "20px"})  # Increased flex ratio for the visualization
            ], style={"display": "flex", "flex-direction": "row"})
        ])
    ])
])


# --- CALLBACKS POUR METTRE À JOUR LES VISUALISATIONS ---
@app.callback(
    Output('vis1', "figure"),
    Input('radio-vis1', "value"),
    Input("age-checklist","value") # Add a valid input
)
def update_vis1(category,selection):
        #return generate_vis1()
    match category:
        case 'Par niveaux':
            return make_viz1_noSelect(dict_All_viz1[category],df_temp,df_preci,1999)
        case 'Par sex':
            return make_viz1_noSelect(dict_All_viz1[category],df_temp,df_preci,1999)
        case 'Par age':
            return make_viz1_select(dict_All_viz1[category],df_temp,df_preci,1999,selection)
        case 'Par sex-age':
            return make_viz1_select(dict_All_viz1[category],df_temp,df_preci,1999,selection)
        case _:
            return make_viz1_noSelect(dict_All_viz1["Par niveaux"],df_temp,df_preci,1999)


@app.callback(
    Output("vis2", "figure"),
    [Input("vis2", "selectedData") , Input("vis2", "figure")],
    prevent_initial_call=True

)
def update_vis2_from_selection(selectedData, fig):
    # Vérifier si selectedData et selectedData["points"] sont valides
    if selectedData and "points" in selectedData and len(selectedData["points"]) > 0:
        return update_plots(None, selectedData["points"], None, fig)
    return dash.no_update 

@app.callback(
    [Output("matrix-chart", "figure"),
     Output("selected-runner-info", "children")],
    [Input("gender-dropdown", "value"),
     Input("category-dropdown", "value"),
     Input("matrix-chart", "clickData")]
)
def update_chart(selected_gender, selected_category, click_data):
    selected_runner = None
    runner_name = "Aucun coureur sélectionné"
    
    if click_data and "points" in click_data:
        selected_runner = click_data["points"][0]["customdata"]
        runner_name = f"Coureur sélectionné : {selected_runner}"

    fig = generate_marathon_chart(selected_gender, selected_runner, selected_category)
    return fig, runner_name


# si delectionne le coureur selected_runner = None
@app.callback(
    Output("matrix-chart", "clickData"),
    [Input("deselect-button", "n_clicks")]
)
def deselect_runner(n_clicks):
    if n_clicks > 0:
        return None
    return dash.no_update