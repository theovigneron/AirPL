# AirPL
Projet Master 2 Miage 2023

Pour pourvoir executer ScriptChroniqueSO2.py / scriptPM10 / scriptSO2
il vous faudra installer plusieur biblioteche python. 

**Installation python sur windows**

1. Rendez-vous sur le site officiel de Python à l'adresse https://www.python.org/downloads/ et téléchargez la dernière version stable de Python pour Windows

2. Une fois le fichier d'installation téléchargé, double-cliquez dessus pour lancer l'installateur.

3. Cochez la case "Add Python to PATH" (Ajouter Python au PATH) et assurez-vous qu'elle est sélectionnée. Cela permettra d'ajouter automatiquement Python à votre variable d'environnement PATH, ce qui facilitera l'accès à Python depuis n'importe quel répertoire dans l'invite de commandes.

4. Cliquez sur "Customize installation" (Personnaliser l'installation) si vous souhaitez modifier les options d'installation par défaut, telles que le répertoire d'installation.

5. Cliquez sur "Install" (Installer) pour démarrer l'installation. L'installateur copiera les fichiers nécessaires sur votre système.

**Installation des librairies** 

1. Ouvrez une fenêtre de commande en appuyant sur la touche Windows, en tapant "cmd" et en appuyant sur Entrée.

2. Dans la fenêtre de commande, vous pouvez utiliser le gestionnaire de packages Python appelé pip pour installer des bibliothèques externes. Pip est généralement installé automatiquement avec Python.

3. Tapez la commande suivante et appuyez sur Entrée pour installer les librairies :
```
pip install pandas
pip install json
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install requests
pip install smtplib
```

**Execution du code**

1. Ouvrez une fenêtre de commande (appuyez sur la touche Windows, tapez "cmd" et appuyez sur Entrée).

2. Utilisez la commande cd pour naviguer vers le répertoire où se trouve votre script Python. Par exemple, si votre fichier est dans le dossier "Documents", vous pouvez utiliser la commande suivante :
```cd C:\Users\VotreNom\Documents```
Assurez-vous de remplacer "VotreNom" par votre nom d'utilisateur Windows.

3. Une fois que vous êtes dans le bon répertoire, vous pouvez exécuter le script en utilisant la commande python suivie du nom de votre fichier Python. Par exemple :
```py mon_script.py```

ici les script seront : 
    - ScriptChroniqueSO2.py 
    - scriptPM10
    - scriptSO2