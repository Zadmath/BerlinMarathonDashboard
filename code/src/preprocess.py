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
    top_10_per_year = my_df.copy()
    
    if selected_category_age == "ALL":
        # Group by year and gender, then select the top 10 by "place"
        top_10_per_year = top_10_per_year.groupby(["year", "gender"], group_keys=False).apply(
            lambda x: x.nsmallest(10, "place")
        )
    else:
        # Appliquer le filtre par catégorie d'âge
        top_10_per_year = top_10_per_year[top_10_per_year["class_age"] == selected_category_age]
        
        # Group by year, gender, and category, then select the top 10 by "place"
        top_10_per_year = top_10_per_year.groupby(["year", "gender", "class_age"], group_keys=False).apply(
            lambda x: x.nsmallest(10, "place")
        )
    
    # Sélectionner les 10 nationalités les plus fréquentes
    top_nations = get_top_nations(top_10_per_year)

    # Remplacer les autres nationalités par "Other"
    top_10_per_year["nation"] = top_10_per_year["nation"].apply(lambda x: x if x in top_nations else "Other")
    # Ensure only 10 runners per year, gender, and category
    top_10_per_year = top_10_per_year.groupby(["year", "gender", "class_age"], group_keys=False).head(10)
    #on affiche pour l'année 2023
    return top_10_per_year

