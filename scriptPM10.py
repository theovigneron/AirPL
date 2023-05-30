import json
import pandas as pd
import requests

# Seuils PM10
objectif_qualite = 30
valeur_limite_journaliere = 50
valeur_limite_annuelle = 40
seuil_information_recommandation = 50
seuil_alerte = 80

# Charger les données depuis le fichier JSON
url = "https://data.airpl.org/api/v1/mesure/journaliere/?&code_configuration_de_mesure__code_point_de_prelevement__code_polluant=24&date_heure_tu__range=2022-5-30,2023-5-30&code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in=44,49,53,72,85,&export=json"

response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()
else:
    print("Une erreur s'est produite lors de la récupération du JSON :", response.status_code)

periode_results = json_data['results']

# Créer un DataFrame à partir des résultats filtrés
df = pd.DataFrame(periode_results)

columns_to_keep = ['nom_commune', 'valeur', "date_heure_tu"]  

df_max_pm10_idx = df.groupby('nom_commune')['valeur'].idxmax()
df_max_pm10 = df.loc[df_max_pm10_idx.dropna(), columns_to_keep]

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

# Afficher l'introduction
print(rapport_str)

# Filtrer les données pour ne garder que les lignes avec des valeurs supérieures au seuil journalier
df_depass_seuil_journalier = df[df['valeur'] > valeur_limite_journaliere]

if not df_depass_seuil_journalier.empty:
    print("\nCommunes ayant dépassé le seuil journalier :")
    print(df_depass_seuil_journalier['nom_commune'].unique())
else:
    print("\nAucune commune n'a dépassé le seuil journalier.")
    
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("\nPM10 maximal enregistré par commune :")
    print(df_max_pm10)
    


# chargement des données depuis un fichier JSON
with open('PM10_Horaire_OctobreMars.json', 'r') as file:
    data = json.load(file)

periode_results = data['results']

df = pd.DataFrame(periode_results)

# Convert 'date_heure_tu' column to datetime type
df['date_heure_tu'] = pd.to_datetime(df['date_heure_tu'])

df.dropna(subset=['nom_commune'], inplace=True)

df['heure'] = df['date_heure_tu'].dt.hour

# Group by commune et calculer la moyenne des émissions de PM10
df_avg_pm10 = df.groupby(['nom_commune', 'heure'])['valeur'].mean().reset_index()

# trouver l'heure avec les émissions moyennes les plus élevées par commune
max_avg_pm10 = df_avg_pm10.groupby('nom_commune')['valeur'].max()

# On garde que les lignes avec les émissions moyennes les plus élevées par commune
df_max_avg_pm10 = df_avg_pm10[df_avg_pm10.groupby('nom_commune')['valeur'].transform(lambda x: x == x.max())]

print("\nHeure avec les émissions moyennes les plus élevées par commune:")
for index, row in df_max_avg_pm10.iterrows():
    commune = row['nom_commune']
    heure = row['heure']
    moyenne_emissions = row['valeur']
    print(f"Commune: {commune}, Heure: {heure}, Emission de PM10 en moyenne: {moyenne_emissions}")
    
    


