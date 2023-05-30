import json
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Seuils PM10
objectif_qualite = 30
valeur_limite_journaliere = 50
valeur_limite_annuelle = 40
seuil_information_recommandation = 50
seuil_alerte = 80

sender_email = 'theo.vigneron2@gmail.com'  # adresse e-mail Gmail
receiver_email = 'theo.vigneron2@gmail.com'  # e-mail du destinataire
email_subject = 'Test d\'e-mail'
email_message = ''
email_password = 'pljyqiqzbtjojnod'  # Mot de passe de votre compte Gmail

# Charger les données depuis le fichier JSON
with open('PM10_Horaire_OctobreMars.json', 'r') as file:
    data = json.load(file)

periode_results = data['results']

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
email_message +=rapport_str+"\n"

# Filtrer les données pour ne garder que les lignes avec des valeurs supérieures au seuil journalier
df_depass_seuil_journalier = df[df['valeur'] > valeur_limite_journaliere]

if not df_depass_seuil_journalier.empty:
    email_message += "Communes ayant dépassé le seuil journalier :\n"
    for commune in df_depass_seuil_journalier['nom_commune'].unique():
        email_message += "      -"+commune+"\n"
else:
    email_message += "Aucune commune n'a dépassé le seuil journalier.\n"
    
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    email_message +="PM10 maximal enregistré par commune :\n"
    for max in df_max_pm10:
        email_message += max+"\n"
    


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

email_message +="Heure avec les émissions moyennes les plus élevées par commune:\n"
for index, row in df_max_avg_pm10.iterrows():
    commune = row['nom_commune']
    heure = row['heure']
    moyenne_emissions = row['valeur']
    email_message +=f"Commune: {commune}, Heure: {heure}, Emission de PM10 en moyenne: {moyenne_emissions}\n"


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

send_email(sender_email, receiver_email, email_subject, email_message, email_password)