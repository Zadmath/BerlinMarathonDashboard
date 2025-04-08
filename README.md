# Projet de Visualisation du Marathon

## Vue d'ensemble

Ce projet propose des visualisations interactives des données de marathon à l'aide de Plotly. Il permet aux utilisateurs d'explorer les statistiques des marathons, y compris les classements, les temps et les informations démographiques, de 1999 à 2023. Les visualisations sont dynamiques et personnalisables en fonction des filtres sélectionnés par l'utilisateur, tels que le genre, la catégorie d'âge et les coureurs spécifiques.

## Fonctionnalités

- **Graphiques interactifs** : Visualisez les classements et statistiques des marathons avec des graphiques interactifs.
- **Filtres** : Filtrez les données par genre, catégorie d'âge ou coureurs spécifiques.
- **Statistiques des coureurs** : Consultez des statistiques détaillées et l'historique des performances pour les coureurs sélectionnés.
- **Disposition dynamique** : La mise en page s'adapte en fonction des filtres sélectionnés et des données disponibles.

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

1. Assurez-vous que les fichiers de données requis (`marathon_df`, `years`) sont disponibles dans le module `data`.
2. Exécutez le script de visualisation :
   ```bash
   python visualizations_3.py
   ```
3. Utilisez l'interface interactive pour explorer les données :
   - Sélectionnez le genre (`ALL`, `M`, `W`).
   - Choisissez une catégorie d'âge ou affichez toutes les catégories.
   - Cliquez sur un coureur pour voir ses statistiques détaillées et son historique de performances.

## Structure des fichiers

- `visualizations_3.py` : Script principal pour générer les visualisations du marathon.
- `preprocess.py` : Contient les fonctions de prétraitement des données.
- `layout_vis3.py` : Gère la configuration de la mise en page des visualisations.
- `data/` : Répertoire contenant les fichiers de données du marathon.

## Dépendances

- Python 3.x
- Plotly
- Pandas
- NumPy

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Forkez le dépôt.
2. Créez une nouvelle branche pour votre fonctionnalité ou correction de bug :
   ```bash
   git checkout -b nom-de-la-fonctionnalite
   ```
3. Validez vos modifications et poussez-les sur votre fork.
4. Soumettez une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

## Remerciements

- Données du marathon fournies par [source/organisation].
- Visualisation réalisée avec [Plotly](https://plotly.com/).
