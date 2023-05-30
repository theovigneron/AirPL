import pandas as pd

# Seuils PM10
objectif_qualite = 30
valeur_limite_journaliere = 50
valeur_limite_annuelle = 40
seuil_information_recommandation = 50
seuil_alerte = 80

# Charger les données depuis le fichier CSV
df = pd.read_csv('SO2_Horaire_OctobreMars.csv')

columns_to_keep = ['nom_com', 'valeur', 'date_heure_tu']

df_max_pm10_idx = df.groupby('nom_commune')['valeur'].idxmax()
df_max_pm10 = df.loc[df_max_pm10_idx.dropna(), columns_to_keep]

# Générer le rapport
rapport = []
rapport.append("Rapport trimestriel d'expositions PM10 des personnes et des territoires")
rapport.append("Période : Octobre 2022 à Mars 2023")
rapport.append("===================================")

rapport.append("\nSeuils PM10 :")
rapport.append(" - Objectif de qualité en moyenne annuelle : " + str(objectif_qualite) + " μg/m³")
rapport.append(" - Valeur limite journalière à ne pas dépasser plus de 35 jours par an : " + str(
    valeur_limite_journaliere) + " μg/m³")
rapport.append(" - Valeur limite annuelle : " + str(valeur_limite_annuelle) + " μg/m³")
rapport.append(" - Seuil d'information et de recommandation sur 24 heures : " + str(
    seuil_information_recommandation) + " μg/m³")
rapport.append(" - Seuil d'alerte sur 24 heures : " + str(seuil_alerte) + " μg/m³")

# Convertir la liste en chaîne de caractères
rapport_str = "\n".join(rapport)

# Afficher l'introduction
print(rapport_str)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("\nPM10 maximal enregistré par commune :")
    print(df_max_pm10)

df['date_heure_tu'] = pd.to_datetime(df['date_heure_tu'])

df.dropna(subset=['nom_commune'], inplace=True)

df['heure'] = df['date_heure_tu'].dt.hour

df_avg_pm10 = df.groupby(['nom_commune', 'heure'])['valeur'].mean().reset_index()

max_avg_pm10 = df_avg_pm10.groupby('nom_commune')['valeur'].max()

df_max_avg_pm10 = df_avg_pm10[df_avg_pm10.groupby('nom_commune')['valeur'].transform(lambda x: x == x.max())]

print("Heure avec les émissions moyennes les plus élevées par commune:")
for index, row in df_max_avg_pm10.iterrows():
    commune = row['nom_commune']
    heure = row['heure']
    moyenne_emissions = row['valeur']
    print(f"Commune: {commune}, Heure: {heure}, Emission de PM10 en moyenne: {moyenne_emissions}")
