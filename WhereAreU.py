import os
import requests
import sys
import zipfile
import win32com.client
import json
from subprocess import call

# Définir le nom du référentiel
repo_owner = "R3nzTheCodeGOD"
repo_name = "R3nzSkin"
settings_file = "settings_wau.json"
settings_json_default = { "lol_directory": "C:\\Riot Games\\League of Legends", "first_time": True }

def checkSettings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            settings = json.load(f)
            first_time = settings["first_time"]
            if first_time == True:
                lol_directory_preference = input("Please enter your League of Legends installation folder (default: C:\\Riot Games\\League of Legends) : ")

                if(lol_directory_preference != ""):
                    settings_json_default["lol_directory"] = lol_directory_preference
                    settings_json_default["first_time"] = False
                    with open(settings_file, "w") as f:
                        json.dump(settings_json_default, f)
                else:
                    settings_json_default["first_time"] = False
                    with open(settings_file, "w") as f:
                        json.dump(settings_json_default, f)
    else:
        print(f"Le fichier '{settings_file}' n'existe pas.")
        print("Création du fichier...")
        with open(settings_file, "w") as f:
            json.dump(settings_json_default, f)
        print(f"Le fichier '{settings_file}' a été créé.")
        lol_directory_preference = input("Please enter your League of Legends installation folder (default: C:\\Riot Games\\League of Legends) : ")

        if(lol_directory_preference != ""):
            settings_json_default["lol_directory"] = lol_directory_preference
            settings_json_default["first_time"] = False
            with open(settings_file, "w") as f:
                json.dump(settings_json_default, f)
        else:
            settings_json_default["first_time"] = False
            with open(settings_file, "w") as f:
                json.dump(settings_json_default, f)

checkSettings()

# Définir le chemin du dossier League of Legends
lol_directory = "C:\\Riot Games\\League of Legends"

with open(settings_file, "r") as f:
    settings_json = json.load(f)
    lol_directory = settings_json["lol_directory"]

def find_file_by_description(description):
    shell = win32com.client.Dispatch("Shell.Application")
    folder = shell.NameSpace(lol_directory)  # Remplacez par votre chemin
    for item in folder.Items():
        if item.Type == "Application" and item.ExtendedProperty("System.FileDescription") == description:
            return os.path.join(lol_directory, item.Name)
    return None

def exec_script():

    print(f"Le chemin du dossier League of Legends est : {lol_directory}")

    # Créer une session pour éviter les limites de taux d'API GitHub
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "FindOrOpen-GitHub"
    })

    # Obtenir les informations de la dernière version du référentiel
    release_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = session.get(release_url)
    print("Recherche de la dernière version du script...")
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info.get("assets", [])
        print("Récupération des informations de la dernière version...")

        if assets:
            # Trouvez le fichier d'actif avec le bon nom (par exemple, "R3nzSkin.zip")
            asset = next((a for a in assets if a["name"] == "R3nzSkin.zip"), None)
            print("Récupération du dossier R3nzSkin.zip...")

            if asset:
                download_url = asset["browser_download_url"]

                # Téléchargez le fichier zip
                download_path = "temp.zip"
                response = session.get(download_url)
                print("Téléchargement du dossier R3nzSkin.zip...")

                if response.status_code == 200:
                    with open(download_path, 'wb') as f:
                        f.write(response.content)
                    print("Ouverture du dossier R3nzSkin.zip...")
                    # Extrayez les fichiers zip dans le dossier League of Legends
                    with zipfile.ZipFile(download_path, 'r') as zip_ref:
                        zip_ref.extractall(lol_directory)
                        print("Extraction du dossier R3nzSkin.zip...")

                    # Supprimez le fichier zip temporaire
                    os.remove(download_path)
                    print("Suppression du dossier R3nzSkin.zip...")

                    openGoodFile()
                    print("Ouverture du fichier R3nSkin DLL Injector...")
                else:
                    print("Impossible de télécharger le fichier depuis GitHub.")
            else:
                print("Fichier d'actif introuvable dans les actifs de la dernière version.")
        else:
            print("Aucun actif trouvé dans la dernière version.")
    else:
        print("Impossible de récupérer les informations de la dernière version.")

def openGoodFile():
    # Recherche du fichier par description (par exemple, "R3nzSkin_Injector.exe")
    description_to_find = "R3nSkin DLL Injector"
    found_file = find_file_by_description(description_to_find)

    if found_file:
        print(f"Le fichier '{description_to_find}' a été trouvé : {found_file}")
        call([found_file])
    else:
        print(f"Le fichier '{description_to_find}' n'a pas été trouvé.")

description_to_find = "R3nSkin DLL Injector"
found_file = find_file_by_description(description_to_find)

if not found_file:
    # Les fichiers n'existent pas, exécutez le script
    exec_script()
    sys.exit()
else:
    # Les fichiers existent, ouvrez scriptLOL.exe
    openGoodFile()
    sys.exit()