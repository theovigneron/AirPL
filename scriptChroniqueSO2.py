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

sender_email = 'theo.vigneron2@gmail.com'  # Votre adresse e-mail Gmail
receiver_email = 'theo.vigneron2@gmail.com'  # Adresse e-mail du destinataire
email_subject = 'Test d\'e-mail'
email_message = 'Ceci est un test d\'e-mail envoyé depuis Python.'
email_password = 'pljyqiqzbtjojnod'  # Mot de passe de votre compte Gmail


def fetchJson(date1, date2):
    url = "https://data.airpl.org/api/v1/mesure/horaire/?&code_configuration_de_mesure__code_point_de_prelevement__code_polluant=01&date_heure_tu__range={},{}%2023:00:00&code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in=44,49,53,72,85,&export=json".format(date1, date2)

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Une erreur s'est produite lors de la récupération du JSON :", response.status_code)

def mergeJson():

    date_actuelle = datetime.now().strftime("%Y-%m-%d")
    last_week = date_actuelle - timedelta(weeks=1)
    last_week_format = last_week.strftime("%Y-%m-%d")

    print(date_actuelle)
    print(last_week_format)

    jsonfetch = fetchJson(last_week, date_actuelle)

    # Convertir le JSON en DataFrame pandas
    df = pd.DataFrame(jsonfetch["results"])
    df_filtre = df[df["validite"] == True]

    # Enregistrer le DataFrame en fichier CSV
    df_filtre.to_csv("SO2_Horaire_OctobreMars.csv", index=False)


def analyse(): 
    # Charger le fichier CSV dans un DataFrame pandas
    df = pd.read_csv("SO2_Horaire_OctobreMars.csv")
    
    print("Commune depassant l'objectif de qualité en moyenne annuelle")
    moyennes_par_commune = df.groupby("nom_commune")["valeur"].mean()
    commune_sup_objQualite = moyennes_par_commune[moyennes_par_commune > objQualite]
    if commune_sup_objQualite.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(commune_sup_objQualite)


    print("Commune depassant la valeur limite plus de 3 jours par an")
    moyennes_par_commune_jour = df.groupby(["nom_commune", "date_heure_tu"])["valeur"].mean()
    moyennes_sup_Lim = moyennes_par_commune_jour[moyennes_par_commune_jour > valLimiteJour]
    jours_depassement_par_commune = moyennes_sup_Lim.groupby("nom_commune").size()
    communes_depassement_VL = jours_depassement_par_commune[jours_depassement_par_commune > 3]
    if communes_depassement_VL.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_VL)

    print("Commune ayant depassé le Seuil d’information et de recommandation")
    valeurs_max_par_commune_jour = df.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_SI = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilInfo]
    communes_depassement_SI = valeurs_sup_SI.index.get_level_values("nom_commune").unique()
    if communes_depassement_SI.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_SI)


    print("Commune ayant depassé le Seuil d’Alerte")
    valeurs_max_par_commune_jour = df.groupby(["nom_commune", "date_heure_tu"])["valeur"].max()
    valeurs_sup_Alerte = valeurs_max_par_commune_jour[valeurs_max_par_commune_jour > seuilAlerte]
    communes_depassement_SI = valeurs_sup_Alerte.index.get_level_values("nom_commune").unique()
    if communes_depassement_SI.size == 0:
        print("Aucune commune ne depasse le seuil")
    else:
        print(communes_depassement_SI)


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


mergeJson()
analyse()
send_email(sender_email, receiver_email, email_subject, email_message, email_password)