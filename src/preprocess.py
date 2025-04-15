'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

def uniformiser(my_df):

    # TODO : Round the dataframe
    # regrouper "DEU" et "GER" sous "GER"
    my_df["nation"] = my_df["nation"].replace({"DEU": "GER"})
    # regrouper DNK et DEN sous DEN
    my_df["nation"] = my_df["nation"].replace({"DNK": "DEN"})

    # Ajouter une colonne pour différencier hommes et femmes
    my_df["gender"] = my_df["sex"].str.upper()

    return my_df
    

# Sélectionner les 10 nationalités les plus fréquentes
def get_top_nations(my_df):
    nation_counts = my_df["nation"].value_counts()
    top_nations = nation_counts.nlargest(10).index.tolist()
    return top_nations
    
def get_top_10(my_df, selected_category_age="ALL"):
    # Avoid unnecessary DataFrame copies
    if selected_category_age == "ALL":
        # Group by year and gender, then select the top 10 by "place"
        top_10_per_year = my_df.groupby(["year", "gender"], group_keys=False).apply(
            lambda x: x.nsmallest(10, "place")
        )
    else:
        # Filter by category and group by year, gender, and category
        filtered_df = my_df[my_df["class_age"] == selected_category_age]
        top_10_per_year = filtered_df.groupby(["year", "gender", "class_age"], group_keys=False).apply(
            lambda x: x.nsmallest(10, "place")
        )
    
    # Replace other nationalities with "Other" in-place to save memory
    top_nations = get_top_nations(top_10_per_year)
    top_10_per_year.loc[:, "nation"] = top_10_per_year["nation"].where(
        top_10_per_year["nation"].isin(top_nations), "Other"
    )
    # Limit to 10 runners per group
    top_10_per_year = top_10_per_year.groupby(["year", "gender", "class_age"], group_keys=False).head(10)
    return top_10_per_year



def process_data_courreur_viz1(df_courreur):
    year=list(df_courreur['year'].unique())
    dict_All_Data={}

    # Chaque data du dictionnaire est de la forme : index = Catégorie , colonne  = Année
    # Exemple sex:  index =['Femme','Homme'], colonnes=[1999,2001,2002,...,2023]  df['Femme',1999] = tps moyen pour les femmes en 1999 
    # Par niveaux 
    
    df_top10_per_year = df_courreur.groupby('year').apply(lambda x: x.nsmallest(10, 'tps_fin')['tps_fin'].mean()).reset_index()
    df_top10_per_year.columns = ['year', 'mean_tps_fin']
    df_top10_per_year=df_top10_per_year.set_index('year')
    df_top10_per_year=df_top10_per_year.T
    df_top10_per_year = df_top10_per_year.rename(index={'mean_tps_fin': 'Top 10'})

    df_top25_per_year = df_courreur.groupby('year').apply(lambda x: x.nsmallest(int(len(x) * 0.25), 'tps_fin')['tps_fin'].mean()).reset_index()
    df_top25_per_year.columns = ['year', 'mean_tps_fin']
    df_top25_per_year=df_top25_per_year.set_index('year')
    df_top25_per_year=df_top25_per_year.T
    df_top25_per_year = df_top25_per_year.rename(index={'mean_tps_fin': 'Pros'})

    df_top50_per_year = df_courreur.groupby('year').apply(lambda x: x.nsmallest(int(len(x) * 0.5), 'tps_fin').nlargest(int(len(x)*0.25),'tps_fin')['tps_fin'].mean()).reset_index()
    df_top50_per_year.columns = ['year', 'mean_tps_fin']
    df_top50_per_year=df_top50_per_year.set_index('year')
    df_top50_per_year=df_top50_per_year.T
    df_top50_per_year = df_top50_per_year.rename(index={'mean_tps_fin': 'Semi-pro'})

    df_top75_per_year = df_courreur.groupby('year').apply(lambda x: x.nsmallest(int(len(x) * 0.75), 'tps_fin').nlargest(int(len(x)*0.25),'tps_fin')['tps_fin'].mean()).reset_index()
    df_top75_per_year.columns = ['year', 'mean_tps_fin']
    df_top75_per_year=df_top75_per_year.set_index('year')
    df_top75_per_year=df_top75_per_year.T
    df_top75_per_year = df_top75_per_year.rename(index={'mean_tps_fin': 'Passionnés'})

    df_top100_per_year = df_courreur.groupby('year').apply(lambda x: x.nlargest(int(len(x)*0.25),'tps_fin')['tps_fin'].mean()).reset_index()
    df_top100_per_year.columns = ['year', 'mean_tps_fin']
    df_top100_per_year=df_top100_per_year.set_index('year')
    df_top100_per_year=df_top100_per_year.T
    df_top100_per_year = df_top100_per_year.rename(index={'mean_tps_fin': 'Amateurs'})

    dict_All_Data["Par niveaux"]=pd.concat([df_top10_per_year,df_top25_per_year,df_top50_per_year,df_top75_per_year,df_top100_per_year])

    #Par sex
    data={}
    df_homme=df_courreur.loc[df_courreur['sex']=='M']
    df_homme=df_homme.groupby('year')['tps_fin'].mean().reset_index()
    df_homme.columns = ['year', 'mean_tps_fin']
    df_homme=df_homme.set_index('year')
    df_homme=df_homme.T
    df_homme = df_homme.rename(index={'mean_tps_fin': 'Homme'})

    df_femme=df_courreur.loc[df_courreur['sex']=='W']
    df_femme=df_femme.groupby('year')['tps_fin'].mean().reset_index()
    df_femme.columns = ['year', 'mean_tps_fin']
    df_femme=df_femme.set_index('year')
    df_femme=df_femme.T
    df_femme = df_femme.rename(index={'mean_tps_fin': 'Femme'})

    dict_All_Data["Par sex"] = pd.concat([df_femme,df_homme])

    #Par age
    df_age=df_courreur.groupby('year')[['class_age','tps_fin']]
    result = pd.DataFrame() 
    for x,y in df_age:
        df_year=y.groupby('class_age')['tps_fin'].mean().reset_index()
       
        # On renomme la colonne pour qu'elle corresponde à l'année    
        df_year= df_year.rename(columns={'tps_fin': int(x)})
        # On utilse class_age comme index 
        df_tmp = df_year.set_index('class_age')

        # On fusionne tout sur l'index class_age
        if result.index.names == [None]:
            result =df_tmp.copy()
        else:
            result = pd.merge(result, df_tmp, left_index=True, right_index=True, how='outer')
    # Résultat : un DataFrame avec class_age en index et les années en colonnes
    dict_All_Data["Par age"]=result

    #Par age sex
    df_age=df_courreur.groupby('year')[['class_age','sex','tps_fin']]
    result_age_sex = pd.DataFrame() 
    for x,y in df_age:
        df_year=y.groupby(by=['class_age','sex'])['tps_fin'].mean().reset_index()
        
        # On renomme la colonne pour qu'elle corresponde à l'année    
        df_year= df_year.rename(columns={'tps_fin': int(x)})
        # On utilse class_age comme index 
        df_tmp = df_year.set_index(['class_age','sex'])
        # On fusionne tout sur l'index class_age

        if result_age_sex.index.names == [None]:
            result_age_sex =df_tmp.copy()
        else:
            result_age_sex = pd.merge(result_age_sex, df_tmp, left_index=True, right_index=True, how='outer')
    # Résultat : un DataFrame avec class_age en index et les années en colonnes
    dict_All_Data["Par sex-age"]=result_age_sex


 
    return dict_All_Data

def preprocess_meteo(df_meteo):
    df_avgTemp=df_meteo.loc[df_meteo['YEAR']>1998][['YEAR','AVG_TEMP_C']]
    df_avgTemp=df_avgTemp.set_index('YEAR')
    df_avgTemp=df_avgTemp.T
    df_avgTemp[2021]=[22.3]
    df_avgTemp[2022]=[17.4]
    df_avgTemp[2023]=[18.2]

    df_Preci=df_meteo.loc[df_meteo['YEAR']>1998][['YEAR','PRECIP_mm']]
    df_Preci=df_Preci.set_index('YEAR')
    df_Preci=df_Preci.T
    df_Preci[2021]=[0]
    df_Preci[2022]=[0]
    df_Preci[2023]=[0]
    return df_avgTemp,df_Preci

def save_top_10_csvs(my_df, output_dir="./top_10_csvs"):
    """
    Generate and save CSV files for the top 10 runners by year, gender, and category.

    Args:
        my_df (pd.DataFrame): The preprocessed marathon DataFrame.
        output_dir (str): The directory where the CSV files will be saved.
    """
    import os

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Group by year, gender, and category
    grouped = my_df.groupby(["year", "gender", "class_age"], group_keys=False)

    # Iterate through each group and save the top 10 to a CSV
    for (year, gender, class_age), group in grouped:
        top_10 = group.nsmallest(10, "place")
        filename = f"{output_dir}/top_10_{year}_{gender}_{class_age}.csv"
        top_10.to_csv(filename, index=False)
        print(f"Saved: {filename}")

# Example usage (uncomment to run):
