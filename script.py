import requests

url = "https://geo.api.gouv.fr/communes"
params = {
    "codeRegion": "52",
    "fields": "nom,code,population",
    "format": "json",
    "geometry": "centre"
}

response = requests.get(url, params=params)
communes = response.json()

# print(communes)



import json
import pandas as pd

# Seuils PM10
objectif_qualite = 30
valeur_limite_journaliere = 50
valeur_limite_annuelle = 40
seuil_information_recommandation = 50
seuil_alerte = 80

# Charger les données depuis le fichier JSON
with open('PM10_Horaire_OctobreMars.json', 'r') as file:
    data = json.load(file)

periode_results = data['results']

# Créer un DataFrame à partir des résultats filtrés
df = pd.DataFrame(periode_results)

#TODO garder la valeur de PM10 maximale pour chaque commune
print(df.columns)

columns_to_keep = ['nom_commune', 'valeur', "date_heure_tu"]  # Add the desired column names here

df_max_pm10_idx = df.groupby('nom_commune')['valeur'].idxmax()
df_max_pm10 = df.loc[df_max_pm10_idx.dropna(), columns_to_keep]

# Calculer les statistiques de la période
total_expositions = len(df)
total_depassements_journaliers = df[df['valeur'].gt(valeur_limite_journaliere)].shape[0]
total_depassements_annuels = df[df['valeur'].gt(valeur_limite_annuelle)].shape[0]

# Générer le rapport
rapport = []
rapport.append("Rapport trimestriel d'expositions PM10 des personnes et des territoires")
rapport.append("Période : Octobre 2022 à Mars 2023")
rapport.append("===================================")

rapport.append("\nSeuils PM10 :")
rapport.append(" - Objectif de qualité en moyenne annuelle : " + str(objectif_qualite) + " μg/m³")
rapport.append(" - Valeur limite journalière à ne pas dépasser plus de 35 jours par an : " + str(valeur_limite_journaliere) + " μg/m³")
rapport.append(" - Valeur limite annuelle : " + str(valeur_limite_annuelle) + " μg/m³")
rapport.append(" - Seuil d'information et de recommandation sur 24 heures : " + str(seuil_information_recommandation) + " μg/m³")
rapport.append(" - Seuil d'alerte sur 24 heures : " + str(seuil_alerte) + " μg/m³")

# Convertir la liste en chaîne de caractères
rapport_str = "\n".join(rapport)

# Afficher le rapport
print(rapport_str)



# Perform a left join to include all communes
# df_selected_columns = df[['nom_commune']].merge(df_max_pm10, on='nom_commune', how='left')

# df_selected_columns = df_selected_columns.drop_duplicates(subset='nom_commune')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("\nRésultats détaillés (PM10 maximal par commune) :")
    print(df_max_pm10)
