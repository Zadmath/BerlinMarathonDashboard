# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
'''
import json

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from visualizations_1 import generate_vis1
from visualizations_2 import create_dashboard, update_plots
from visualizations_3 import generate_marathon_chart
import pandas as pd

import preprocess

# Initialisation de l'application Dash
app = dash.Dash(__name__)
app.title = 'Project | INF8808'


# Layout de l'application
app.layout = html.Div([
    html.H1("Dashboard Marathon de Berlin", style={"text-align": "center"}),

    # Conteneur pour VISUALISATION 1 et VISUALISATION 2 côte à côte
    html.Div([
        html.Div([
            html.H3("Visualisation 1"),
            dcc.Graph(id="vis1-line-chart", style={"height": "300px"}),
            dcc.Graph(id="vis1-bar1", style={"height": "200px"}),
            dcc.Graph(id="vis1-bar2", style={"height": "200px"})
        ], style={"flex": "1", "padding": "10px"}),

    html.Div([
            html.H3("Visualisation 2"),
            dcc.Graph(id="vis2", figure=create_dashboard(), style={"height": "700px"})
        ], style={"flex": "1", "padding": "10px"}),
    ], style={"display": "flex", "flex-direction": "row", "width": "100%"}),


    # VISUALISATION 3 : Graphique des nationalités du marathon
    html.Div([
        html.H3("Évolution des Nationalités dans le Top 10 du Marathon de Berlin (1999-2023)"),
    
        # Sélecteur pour filtrer par sexe
        html.Label("Sélectionnez le genre :"),
        dcc.Dropdown(
            id="gender-dropdown",
            options=[
                {"label": "Tous", "value": "ALL"},
                {"label": "Hommes", "value": "M"},
                {"label": "Femmes", "value": "W"}
            ],
            value="ALL",  # Valeur par défaut
            clearable=True,
            style={"width": "50%", "margin-bottom": "10px"}
        ),
            #Filter par catégorie 
            html.Label("Sélectionnez la catégorie d'âge:"),
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
                value="ALL",  # Valeur par défaut
                clearable=False,
                style={"width": "50%", "margin-bottom": "10px"}
        ),
            
    
        # Ajout d'une légende manuelle
        html.Div([
            html.Span("● Hommes", style={"color": "blue", "font-size": "16px", "margin-right": "20px"}),
            html.Span("● Femmes", style={"color": "red", "font-size": "16px"}),
        ], style={"margin-bottom": "10px"}),

        # Graphique et bouton dans le même div
        html.Div([
            html.Div(id="selected-runner-info", style={"marginTop": "10px", "fontWeight": "bold"}),
            html.Button("Désélectionner le coureur", id="deselect-button", n_clicks=0, style={"margin-bottom": "14px"}),
            dcc.Graph(
                id="matrix-chart",
                config={"displayModeBar": True},
                clear_on_unhover=True,
                clickData=None,
                figure=generate_marathon_chart("ALL", None, "ALL"),
                style={"height": "70vh", "width": "100%"}
            )
        ], style={"width": "100%", "display": "flex", "flex-direction": "column", "align-items": "center"})
    ], style={"width": "100%", "padding": "20px"})
])


# --- CALLBACKS POUR METTRE À JOUR LES VISUALISATIONS ---
@app.callback(
    [Output("vis1-line-chart", "figure"),
     Output("vis1-bar1", "figure"),
     Output("vis1-bar2", "figure")],
    [Input("gender-dropdown", "value")]  # Add a valid input
)
def update_vis1(selected_gender):
    return generate_vis1()

@app.callback(
    Output("vis2", "figure"),
    [Input("vis2", "selectedData")],
    prevent_initial_call=True
)
def update_vis2_from_selection(selectedData):
    # Vérifier si selectedData et selectedData["points"] sont valides
    if selectedData and "points" in selectedData and len(selectedData["points"]) > 0:
        fig = create_dashboard()  # Créez la figure initiale uniquement si nécessaire
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