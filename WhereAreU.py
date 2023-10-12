import os
import requests
import sys
import zipfile
import win32com.client
from subprocess import call

# Définir le nom du référentiel
repo_owner = "R3nzTheCodeGOD"
repo_name = "R3nzSkin"

# Définir le chemin du dossier League of Legends
lol_directory = "C:\\Riot Games\\League of Legends"


def find_file_by_description(description):
    shell = win32com.client.Dispatch("Shell.Application")
    folder = shell.NameSpace(lol_directory)  # Remplacez par votre chemin
    for item in folder.Items():
        if item.Type == "Application" and item.ExtendedProperty("System.FileDescription") == description:
            return os.path.join(lol_directory, item.Name)
    return None

def exec_script():
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
