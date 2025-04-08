# Projet de Visualisation du Marathon de Berlin

## Vue d'ensemble

Ce projet propose des visualisations interactives des données du Marathon de Berlin à l'aide de Dash et Plotly. Il permet d'explorer les performances des coureurs, les répartitions par sexe et nationalité, ainsi que les tendances sur plusieurs années. Les utilisateurs peuvent interagir avec les graphiques pour filtrer les données et obtenir des informations détaillées.

## Fonctionnalités

- **Visualisation 1** : Analyse l'évolution des performances en fonctions des performances météo avec des graphes indéxés
- **Visualisation 2** : Dashboard interactif pour explorer les répartitions par sexe et nationalité en fonction des temps d'arrivée.
- **Visualisation 3** : Évolution des nationalités dans le top 10 du marathon, avec des filtres par genre et catégorie d'âge.
- **Interactivité** : Sélectionnez des plages de temps ou des coureurs spécifiques pour afficher des détails personnalisés.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <repository-url>
   ```
2. Accédez au répertoire du projet :
   ```bash
   cd code/src
   ```
3. Installez les dépendances Python nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Assurez-vous que les fichiers de données nécessaires (`marathon_df`, `years`) sont disponibles dans le module `data`.
2. Lancez l'application Dash :
   ```bash
   python server.py
   ```
3. Ouvrez votre navigateur et accédez à `http://localhost:8050` pour interagir avec le tableau de bord.

## Structure des fichiers

- `app.py` : Contient la logique principale de l'application Dash.
- `server.py` : Configure et exécute le serveur Flask pour l'application.
- `visualizations_1.py`, `visualizations_2.py`, `visualizations_3.py` : Scripts pour générer les différentes visualisations.
- `preprocess.py` : Fonctions de prétraitement des données.
- `layout_vis3.py` : Configure la mise en page pour la visualisation 3.
- `data/` : Répertoire contenant les fichiers de données du marathon.

## Dépendances

- Python 3.8 ou supérieur
- Dash
- Plotly
- Pandas
- NumPy


## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

## Remerciements

- Données du marathon fournies par [bmw-berlin-marathon.com].
- Visualisations réalisées avec [Plotly](https://plotly.com/).
