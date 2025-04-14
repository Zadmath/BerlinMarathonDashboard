import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data import marathon_df, years
import preprocess
from layout_vis3 import configure_layout
from preprocess import save_top_10_csvs
# Fonction pour générer des coordonnées en cercle
def generate_circle_points(center_x, center_y, count, radius=0.3):
    if center_x == 2019:
        center_x = 2019.5
        
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False)
    # Calcul des coordonnées x et y
    x_points = center_x + radius * np.cos(angles)
    y_points = center_y + radius * np.sin(angles)
    if count == 1:
        x_points = [center_x]
        y_points = [center_y]

    return x_points, y_points

def get_runner_statistics(filtered_df, selected_runner):
    if not selected_runner:
        return "Aucun coureur sélectionné"
    
    runner_data = filtered_df[filtered_df.apply(
        lambda row: f"{row['nom']} {row['prenom']}" == selected_runner, axis=1
    )]
    
    if runner_data.empty:
        return "Coureur non trouvé"

    # Compile statistics across all years
    stats = runner_data.iloc[0]
    best_place = runner_data["place"].min()


    return (
        f"Nom: {stats['nom']} {stats['prenom']}<br>"
        f"Nationalité: {stats['nation']}<br>"
        f"Genre: {'Homme' if stats['gender'] == 'M' else 'Femme'}<br>"
        f"Meilleur Classement: {best_place}<br>"
        f"Catégories d'âge: {', '.join(map(str, runner_data['class_age'].unique()))}<br>"
    )

def get_runner_photo(selected_runner):
    if not selected_runner:
        return None

    # Generate a Google Image search link for the runner
    search_query = selected_runner.replace(" ", "+")
    return f"https://www.google.com/search?tbm=isch&q={search_query}"

def generate_marathon_chart(selected_gender="ALL", selected_runner=None, selected_category="ALL"):
    fig = go.Figure()
    # on efface le contenu de la figure
    fig.data = []
    top_10_per_year = preprocess.get_top_10(marathon_df, selected_category_age=selected_category)
    # print(f"Top 10 per year: {top_10_per_year}")
    # Appliquer le filtre par genre
    if selected_gender == "ALL":
        filtered_df = top_10_per_year
    else:
        filtered_df = top_10_per_year[top_10_per_year["gender"] == selected_gender]

    # Vérifier s'il y a des données après filtrage
    if filtered_df.empty:
        fig.update_layout(title="Aucune donnée disponible pour ce genre ou catégorie d'âge")
        return fig

    nations_sorted = filtered_df["nation"].value_counts().index.tolist()
    grouped_by_year = filtered_df.groupby("year")
    filtered_df["unique_key"] = filtered_df["nom"] + "_" + filtered_df["prenom"] + "_" + filtered_df["year"].astype(str)
    # print(f"Filtered DataFrame: {filtered_df}")
    for year, group in grouped_by_year:
        # Recalculer le classement relatif pour les femmes uniquement
        group["relative_place"] = group["place"]

        group_woman = group[group["gender"] == "W"].sort_values(by="place").reset_index(drop=True)
        for i, row in group_woman.iterrows():
            group.loc[group["unique_key"] == row["unique_key"], "relative_place"] = i + 1
        if selected_gender == "W":
            group = group[group["gender"] == "W"].sort_values(by="place").reset_index(drop=True)
            group.loc[:, "relative_place"] = group.index + 1
        # Recalculer le classement relatif pour la catégorie d'âge sélectionnée
        if selected_category != "ALL":
            group = group[group["class_age"] == selected_category].sort_values(by="place").reset_index(drop=True)
            group.loc[:, "relative_place"] = group.index + 1
        grouped_by_nation = group.groupby("nation")
        for nation, nation_group in grouped_by_nation:
            point_number = 0
            # print(f"Nation: {nation}, Group: {nation_group}")
            for i, row in nation_group.iterrows():
                # print(f"Row: {row}")
                #si le genre est autre que M ou W, on ne l'affiche pas
                if row["gender"] not in ["M", "W"]:
                    continue
                gender = row["gender"]
                color = "blue" if gender == "M" else "red"
                x_points, y_points = generate_circle_points(
                    year, nations_sorted.index(nation), len(nation_group), radius=0.3
                )
                # Vérifier si le coureur est sélectionné
                full_name = f"{row['nom']} {row['prenom']}"
                is_selected = selected_runner == full_name
                fig.add_trace(go.Scatter(
                    x=[x_points[point_number]], y=[y_points[point_number]], mode="markers",
                    marker=dict(color=color, size=10, opacity=0.1 if selected_runner and not is_selected else 0.7),
                    hoverinfo="text",
                    text=f"{row['nom']} {row['prenom']} (Classement: {row['relative_place']})",
                    customdata=[full_name],  
                    showlegend=False
                ))
                point_number += 1

    # Ajouter des barres verticales pointillées entre chaque année
    for i in years:
        fig.add_shape(
            type="line",
            x0=i - 0.5, y0=-0.5, x1=i - 0.5, y1=len(nations_sorted) - 0.5,
            line=dict(color="gray", width=2, dash="dot"),
            xref="x", yref="y"
        )
    # Ajouter des barres horizontales pointillées pour chaque nationalité
    for i, nation in enumerate(nations_sorted):
        fig.add_shape(
            type="line",
            x0=years[0] - 0.5, y0=i - 0.5, x1=years[-1] + 0.5, y1=i - 0.5,
            line=dict(color="gray", width=2, dash="dot"),
            xref="x", yref="y"
        )

    # Désactiver le quadrillage et les ticks pour éviter les lignes non désirées
    fig.update_xaxes(showgrid=False, zeroline=False)  # Supprime les lignes de référence x
    fig.update_yaxes(showgrid=False, zeroline=False)  # Supprime les lignes de référence y

    # Configuration du graphique
    fig.update_layout(
        title="",
        xaxis=dict(title="Année", tickvals=years, ticktext=[str(y) for y in years]),
        yaxis=dict(title="Nationalité", tickvals=list(range(len(nations_sorted))), ticktext=nations_sorted),
        height=850,
        showlegend=False,
        clickmode="event+select"  # Permet de capturer les clics pour surbrillance
    )

    # Add runner statistics
    runner_statistics = get_runner_statistics(filtered_df, selected_runner)
    runner_photo_url = get_runner_photo(selected_runner)

    if selected_runner:
        runner_data = filtered_df[filtered_df.apply(
            lambda row: f"{row['nom']} {row['prenom']}" == selected_runner, axis=1
        )]
        if "tps_fin_p" in runner_data.columns:
            times_text = "Temps de course de " + selected_runner + ":<br>   "
            times_text += "   ".join(
                f"Année {row.year}: {str(pd.to_timedelta(row.tps_fin_p, unit='s')).split(' ')[2]}" + ("<br>" if i % 2 == 1 else "")  # Ajoute un saut de ligne tous les 2 temps
                for i, row in enumerate(runner_data.itertuples())
            )
        else:
            times_text = "Temps non disponible"
    else:
        if selected_gender == "ALL":
            temps_moyens = filtered_df.groupby("sex")["tps_fin_p"].mean()
            # Convert to timedelta and round to the nearest minute
            temps_moyens = pd.to_timedelta(temps_moyens, unit='s').round('T')
            times_text = "Temps moyen de course du top 10 par sexe" + (" de catégorie d'âge " + selected_category if selected_category != "ALL" else "") + ":<br>"
            temps_homme = temps_moyens.get('M', 'Non disponible')
            temps_homme = str(temps_homme).split(" ")[2]
            temps_femme = temps_moyens.get('W', 'Non disponible')
            temps_femme = str(temps_femme).split(" ")[2]
            times_text += f"   Hommes: {temps_homme}<br>"
            times_text += f"   Femmes: {temps_femme}<br>"
        else:
            temps_moyens = filtered_df["tps_fin_p"].mean()
            # Convert to timedelta and round to the nearest minute
            temps_moyens = pd.to_timedelta(temps_moyens, unit='s').round('T')
            temps_moyens = str(temps_moyens).split(" ")[2]
            times_text = "Temps moyen de course du top 10 pour les " + ("hommes" if selected_gender == "M" else "femmes") + (" de catégorie d'âge " + selected_category if selected_category != "ALL" else "") + ":<br>"
            times_text += f"   {temps_moyens}<br>"
            
        times_text += "<br> (Sélectionnez un coureur pour voir ses temps spécifiques)"

    # Configure layout using the external function
    fig = configure_layout(fig, nations_sorted, years, times_text, runner_statistics, runner_photo_url, selected_category, selected_gender)

    return fig