import pandas as pd
import requests

objQualite = 50
valLimiteHorraire = 350
valLimiteJour = 125
nivCritique = 20
seuilInfo = 300
seuilAlerte = 500

def fetchJson(date1, date2):
    url = "https://data.airpl.org/api/v1/mesure/horaire/?&code_configuration_de_mesure__code_point_de_prelevement__code_polluant=01&date_heure_tu__range={},{}%2023:00:00&code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in=44,49,53,72,85,&export=json".format(date1, date2)

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Une erreur s'est produite lors de la récupération du JSON :", response.status_code)


def mergeJson():
    date = {
        "2022-10-1": "2022-11-1",
        "2022-11-2": "2022-12-1",
        "2022-12-2": "2023-1-1",
        "2023-1-2": "2023-2-1",
        "2023-2-2": "2023-3-1",
    }
    json = []
    for key, value in date.items():
        jsonfetch = fetchJson(key, value)
        json.extend(jsonfetch["results"])

    # Convertir le JSON en DataFrame pandas
    df = pd.DataFrame(json)

    # Enregistrer le DataFrame en fichier CSV
    df.to_csv("SO2_Horaire_OctobreMars.csv", index=False)

def analyse(): 
    # Charger le fichier CSV dans un DataFrame pandas
    df = pd.read_csv("SO2_Horaire_OctobreMars.csv")
    df_filtre = df[df["validite"] == True]
    
    print("Commune depassant l'objectif de qualité en moyenne annuelle")
    moyennes_par_commune = df_filtre.groupby("nom_commune")["valeur"].mean()
    commune_sup_objQualite = moyennes_par_commune[moyennes_par_commune > objQualite]
    if commune_sup_objQualite.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(commune_sup_objQualite)


    print("Commune depassant la valeur limite plus de 3 jours par an")
    moyennes_par_commune_jour = df_filtre.groupby(["nom_commune", "date_heure_tu"])["valeur"].mean()
    moyennes_sup_Lim = moyennes_par_commune_jour[moyennes_par_commune_jour > valLimiteJour]
    jours_depassement_par_commune = moyennes_sup_Lim.groupby("nom_commune").size()
    communes_depassement_VL = jours_depassement_par_commune[jours_depassement_par_commune > 3]
    if communes_depassement_VL.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_VL)

    print("Commune ayant depassé le Seuil d’information et de recommandation")
    valeurs_max_par_commune_jour = df_filtre.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_SI = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilInfo]
    communes_depassement_SI = valeurs_sup_SI.index.get_level_values("nom_commune").unique()
    if communes_depassement_SI.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_SI)


    print("Commune ayant depassé le Seuil d’Alerte")
    valeurs_max_par_commune_jour = df_filtre.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_Alerte = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilAlerte]
    communes_depassement_SI = valeurs_sup_Alerte.index.get_level_values("nom_commune").unique()
    if communes_depassement_SI.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_SI)

mergeJson()
analyse()