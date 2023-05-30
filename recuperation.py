import requests
import pandas as pd
import json

#Impossible de recuperer le CSV sur le site web 
#Message 
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

mergeJson()