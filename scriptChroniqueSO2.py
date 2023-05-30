from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import requests
import smtplib
from datetime import datetime, timedelta

objQualite = 50
valLimiteHorraire = 350
valLimiteJour = 125
nivCritique = 20
seuilInfo = 300
seuilAlerte = 500

sender_email = 'theo.vigneron2@gmail.com'  # adresse e-mail Gmail
receiver_email = 'theo.vigneron2@gmail.com'  # e-mail du destinataire
email_subject = 'Test d\'e-mail'
email_message = ''
email_password = 'pljyqiqzbtjojnod'  # Mot de passe de votre compte Gmail

rapport = []
rapport.append("Rapport trimestriel d'expositions PM10 des personnes et des territoires")
rapport.append("Période : current week")
rapport.append("===================================")

rapport.append("\nSeuils SO2:")
rapport.append(" - Objectif de qualité en moyenne annuelle : " + str(objQualite) + " μg/m³")
rapport.append(" - Valeur limite journalière à ne pas dépasser plus de 35 jours par an : " + str(valLimiteJour) + " μg/m³")
rapport.append(" - Niveau critique de la periode 1er octobre 31 mars : " + str(nivCritique) + " μg/m³")
rapport.append(" - Seuil d'information et de recommandation sur 24 heures : " + str(seuilInfo) + " μg/m³")
rapport.append(" - Seuil d'alerte sur 24 heures : " + str(seuilAlerte) + " μg/m³")

# Convertir la liste en chaîne de caractères
rapport_str = "\n".join(rapport)

# Afficher l'introduction
email_message +=rapport_str+"\n"

def fetchJson(date1, date2):
    url = "https://data.airpl.org/api/v1/mesure/horaire/?code_configuration_de_mesure__code_point_de_prelevement__code_polluant=01&code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in=44%2C49%2C53%2C72%2C85%2C&date_heure_tu__range={}%2C2023-5-30+23%3A00%3A00&export=json&limit=1000".format(date1, date2)

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Une erreur s'est produite lors de la récupération du JSON :", response.status_code)

def mergeWeekJson():
    date_actuelle = datetime.now()
    last_week = date_actuelle - timedelta(weeks=1)
    jsonfetch = fetchJson(last_week, date_actuelle)
    # Convertir le JSON en DataFrame pandas
    df = pd.DataFrame(jsonfetch["results"])
    df_filtre = df[df["validite"] == True]

    # Enregistrer le DataFrame en fichier CSV
    df_filtre.to_csv("Semaine.csv", index=False)

def mergeYearJson():
    date = {
        "2022-4-1": "2022-5-1",
        "2022-5-1": "2022-6-1",
        "2022-6-1": "2022-7-1",
        "2022-7-1": "2022-8-1",
        "2022-8-1": "2022-9-1",
        "2022-9-1": "2022-10-1",
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
    df_filtre = df[df["validite"] == True]
    # Enregistrer le DataFrame en fichier CSV
    df_filtre.to_csv("SO2_Year.csv", index=False)

def mergeSeasonJson():
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
    df_filtre = df[df["validite"] == True]
    # Enregistrer le DataFrame en fichier CSV
    df_filtre.to_csv("SO2_Horaire_OctobreMars.csv", index=False)


def analyse(): 
    global email_message
    # Charger le fichier CSV dans un DataFrame pandas
    df_week = pd.read_csv("Semaine.csv")
    df_year = pd.read_csv("SO2_Year.csv")
    df_season = pd.read_csv("SO2_Horaire_OctobreMars.csv")

    # Commune depassant l'objectif de qualité en moyenne annuelle
    moyennes_par_commune = df_year.groupby("nom_commune")["valeur"].mean()
    commune_sup_objQualite = moyennes_par_commune[moyennes_par_commune > objQualite]
    if commune_sup_objQualite.size == 0:
        email_message += "Aucune commune ne depasse l'objectif de qualité\n"
    else:
        email_message += "commune depassant l'objectif qualité :\n"
        for commune in commune_sup_objQualite.index:
            email_message += "      -"+commune+"\n"
            
    # Commune depassant la valeur limite plus de 3 jours par an
    moyennes_par_commune_jour = df_year.groupby(["nom_commune", "date_heure_tu"])["valeur"].mean()
    moyennes_sup_Lim = moyennes_par_commune_jour[moyennes_par_commune_jour > valLimiteJour]
    jours_depassement_par_commune = moyennes_sup_Lim.groupby("nom_commune").size()
    communes_depassement_VL = jours_depassement_par_commune[jours_depassement_par_commune > 3]
    if communes_depassement_VL.size == 0:
        email_message += "Aucune commune ne depasse la valeur limite plus de 3 jours par an\n"
    else:
        email_message += "commune depassant la valeur limite plus de 3 jours par an :\n"
        for commune in communes_depassement_VL.index:
            email_message += "      -"+commune+"\n"
            
    # Commune ayant depassé le Seuil d’information et de recommandation
    valeurs_max_par_commune_jour = df_year.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_SI = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilInfo]
    communes_depassement_SI = valeurs_sup_SI.index.get_level_values("nom_commune").unique()
    if communes_depassement_SI.size == 0:
        email_message += "Aucune commune ne depasse le Seuil d’information et de recommandation cette année\n"
    else:
        email_message += "commune depassant le Seuil d’information et de recommandation :\n"
        for commune in communes_depassement_SI:
            email_message += "      -"+commune+"\n"

    # Commune ayant depassé Niveau critique pour la protection des écosystèmes
    moyennes_par_commune = df_season.groupby("nom_commune")["valeur"].mean()
    commune_sup_Critique = moyennes_par_commune[moyennes_par_commune > nivCritique]
    if commune_sup_Critique.size == 0:
        email_message += "Aucune commune ne depasse le Niveau critique de la periode octobre mars\n"
    else:
        email_message += "commune depassant l'objectif qualité :\n"
        for commune in commune_sup_Critique.index:
            email_message += "      -"+commune+"\n"


    # Commune ayant depassé le Seuil d’Alerte
    valeurs_max_par_commune_jour = df_week.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_Alerte = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilAlerte]
    communes_depassement_SA = valeurs_sup_Alerte.index.get_level_values("nom_commune").unique()
    if communes_depassement_SA.size == 0:
        email_message += "Aucune commune ne depasse le Seuil d’Alerte sur cette semaine\n"
    else:
        email_message += "commune depassant le Seuil d’Alerte :\n"
        for commune in communes_depassement_SA:
            email_message += "      -"+commune+"\n"


def send_email(sender_email, receiver_email, subject, message, password):
    # Création de l'objet MIMEMultipart pour le message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Ajout du corps du message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connexion au serveur SMTP de Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = sender_email
        smtp_password = password
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Envoi de l'e-mail
        server.send_message(msg)
        server.quit()
        print("L'e-mail a été envoyé avec succès !")
    except Exception as e:
        print("Une erreur s'est produite lors de l'envoi de l'e-mail :", str(e))

def createJson():
    mergeYearJson()
    mergeSeasonJson()
    mergeWeekJson()

createJson()
analyse()
send_email(sender_email, receiver_email, email_subject, email_message, email_password)