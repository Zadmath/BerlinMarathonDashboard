import pandas as pd
import numpy as np
import preprocess

# Load the country abbreviation data
abbreviation_df = pd.read_csv('./src/assets/data/abbreviations.csv')
abbreviation_dict = dict(zip(abbreviation_df['Abbreviation'], abbreviation_df['Country']))

with open('./src/assets/data/MyBerlin_light.csv', encoding='latin1') as data_file:
    marathon_df = pd.read_csv(data_file, low_memory=False)

# Garde uniquement les colonnes utiles
cols_to_keep = ["year", "sex", "nation", "tps_fin", "nom", "prenom", "place", "class_age"]
df = marathon_df[cols_to_keep]

# # Enregistre un fichier allégé
# df.to_csv("MyBerlin_light.csv", index=False)
marathon_df_0 = preprocess.uniformiser(marathon_df)
print(f"Memory used: {marathon_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Update the 'nation' column using the abbreviation dictionary
marathon_df_0['nation'] = marathon_df_0['nation'].map(abbreviation_dict).fillna(marathon_df_0['nation'])

marathon_df = marathon_df_0
marathon_df["tps_fin_p"] = marathon_df["tps_fin"].astype(str).str.extract(r'(\d{2}:\d{2}:\d{2})')[0]

marathon_df["tps_fin_p"] = pd.to_timedelta(marathon_df["tps_fin_p"]).dt.total_seconds()

# Garder les 10 premiers par année et par genre
top_10_per_year = preprocess.get_top_10(marathon_df)

# Mettre à jour la liste triée des nationalités (top 10 + "Other")
nations_sorted = top_10_per_year["nation"].value_counts().index.tolist()

# Lister les années disponibles
years = sorted(top_10_per_year["year"].unique())

df = marathon_df_0
# Convertir les colonnes de temps en timedelta
time_columns = ['km5', 'km10', 'km15', 'km20', 'km25', 'km30', 'km35', 'km40', 'tps_half', 'tps_fin']
for col in time_columns:
    if col in df.columns:
        df[col] = pd.to_timedelta(df[col])

# Filtrer les temps de course valides
# df = df[df['tps_fin_p'] > pd.Timedelta(0)]

# Créer une fonction pour arrondir les temps à l'intervalle de 10 minutes le plus proche
def round_to_10min(seconds):
    if isinstance(seconds, (int, float)):  # Ensure input is numeric
        return pd.Timedelta(seconds=int(seconds // 600) * 600)
    else:
        raise TypeError(f"Invalid type for rounding: {type(seconds)}. Expected int or float.")

# Créer une nouvelle colonne avec les temps arrondis à 10 minutes
df['tps_fin_rounded'] = df['tps_fin_p'].apply(round_to_10min)

# Préparation des données initiales pour les graphiques
# Afficher les données par défaut (tous les coureurs) au démarrage
initial_sex_counts = df['sex'].value_counts()
sex_dict = {'M': 0, 'W': 0}
for sex, count in initial_sex_counts.items():
    if sex in sex_dict:
        sex_dict[sex] = count
initial_sex_values = [sex_dict['M'], sex_dict['W']]

# Top 15 nationalités
initial_nation_counts = df['nation'].value_counts().head(15)

time_counts = df['tps_fin_rounded'].value_counts().sort_index()
    
# Convertir les index en chaînes de caractères pour l'affichage
time_labels = [str(td).split('.')[0] for td in time_counts.index]


