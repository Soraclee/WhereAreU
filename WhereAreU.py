import os
import requests
import sys
import zipfile
import win32com.client
import json
import subprocess
import ctypes
import psutil
import time

def main():
    # Définir le nom du référentiel
    maintenance = True

    if maintenance:
        print("The script is currently in maintenance.")
        print("Please try again later.")
        input("Press Enter to exit...")
        sys.exit()

    repo_owner = "R3nzTheCodeGOD"
    repo_name = "R3nzSkin"
    settings_file = "settings_wau.json"
    settings_json_default = { 
        "lol_directory": "C:\\Riot Games\\League of Legends",
        "first_time": True,
        "version": "1.0.0",
        "versionWhereAreU": "1.0.0"
    }

    current_script = sys.argv[0]

    if "WhereAreU.exe" in current_script:
        if "updated" not in sys.argv:
            print("Start AutoUpdate.exe...")
            if os.path.exists("AutoUpdate.exe"):
                os.startfile("AutoUpdate.exe")
                sys.exit()
    
    def find_league_of_legends_on_all_disks():
        def get_all_disks():
            drives = []
            partitions = psutil.disk_partitions(all=False)
            for partition in partitions:
                drives.append(partition.device)
            return drives

        user_preference = input("Do you want to search for the 'League of Legends' folder on all disks automatically? (This technique may take some time - 2~3min) (Y/N) : ")

        if user_preference.lower() in ["y", "yes", ""]:
            available_disks = get_all_disks()
            for drive in available_disks:
                print("Searching for the 'League of Legends' folder from 'Riot Games' on drive: " + drive)
                if os.path.exists(drive):
                    for root_folder, sub_folders, files in os.walk(drive):
                        if "Riot Games" in sub_folders:
                            riot_games_path = os.path.join(root_folder, "Riot Games")
                            league_of_legends_folder = os.path.join(riot_games_path, "League of Legends")
                            if os.path.exists(league_of_legends_folder):
                                league_client_path = os.path.join(league_of_legends_folder, "LeagueClient.exe")
                                if os.path.exists(league_client_path):
                                    return league_of_legends_folder
        else:
            path_lol = input("Please enter the path to the 'League of Legends' folder: ")

            if os.path.exists(path_lol):
                return path_lol
            else:
                print("The specified path does not exist.")
                sys.exit()

    def checkSettings():
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                settings = json.load(f)
                first_time = settings["first_time"]
                if first_time == True:
                    league_of_legends_path = find_league_of_legends_on_all_disks()
                    current_directory = league_of_legends_path

                    settings_json_default["lol_directory"] = current_directory
                    settings_json_default["first_time"] = False
                    with open(settings_file, "w") as f:
                        json.dump(settings_json_default, f, indent=4)

        else:
            print(f"The file '{settings_file}' does not exist.")
            print("File creation...")
            with open(settings_file, "w") as f:
                json.dump(settings_json_default, f, indent=4)
            print(f"The file '{settings_file}' has been created.")
            league_of_legends_path = find_league_of_legends_on_all_disks()
            current_directory = league_of_legends_path

            settings_json_default["lol_directory"] = current_directory
            settings_json_default["first_time"] = False
            with open(settings_file, "w") as f:
                json.dump(settings_json_default, f, indent=4)

    checkSettings()

    def checkVersionR3nSkin():
        # Créer une session pour éviter les limites de taux d'API GitHub
        session = requests.Session()
        session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WhereAreU-GitHub"
        })

        # Obtenir les informations de la dernière version du référentiel
        release_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = session.get(release_url)
        print("Search for the latest script version...")
        if response.status_code == 200:
            release_info = response.json()
            version_app = release_info['tag_name'];
        
            with open(settings_file, "r") as f:
                settings_json = json.load(f)
                version_settings = settings_json.get("version")
                print("Get version in settings_wau.json")
                
                if version_settings != version_app:
                    settings_json["version"] = version_app
                    with open(settings_file, "w") as f:
                        # Modifier la version dans settings_wau.json
                        print("Change version in settings_wau.json by the new version")
                        json.dump(settings_json, f, indent=4)
                    return True
        else:
            print("Unable to retrieve information from the latest version.")
        
        return False

    # Définir le chemin du dossier League of Legends
    lol_directory = "C:\\Riot Games\\League of Legends"

    with open(settings_file, "r") as f:
        settings_json = json.load(f)
        lol_directory = settings_json["lol_directory"]
    
    def find_file_by_description(description, folder_path):
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.NameSpace(folder_path)
        for item in folder.Items():
            if item.Type == "Application" and item.ExtendedProperty("System.FileDescription") == description:
                return os.path.join(folder_path, item.Name)
        return None

    def exec_script():

        print(f"The path to the League of Legends folder is : {lol_directory}")

        # Créer une session pour éviter les limites de taux d'API GitHub
        session = requests.Session()
        session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WhereAreU-GitHub"
        })

        # Obtenir les informations de la dernière version du référentiel
        release_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = session.get(release_url)
        print("Search for the latest script version...")
        if response.status_code == 200:
            release_info = response.json()
            
            checkVersionR3nSkin()
            
            assets = release_info.get("assets", [])
            print("Retrieving information from the latest version...")

            if assets:
                # Trouvez le fichier d'actif avec le bon nom (par exemple, "R3nzSkin.zip")
                asset = next((a for a in assets if a["name"] == "R3nzSkin.zip"), None)
                print("R3nzSkin.zip folder recovery...")

                if asset:
                    download_url = asset["browser_download_url"]

                    # Téléchargez le fichier zip
                    download_path = "temp.zip"
                    response = session.get(download_url)
                    print("Download R3nzSkin.zip folder...")

                    if response.status_code == 200:
                        with open(download_path, 'wb') as f:
                            f.write(response.content)
                        print("Open folder R3nzSkin.zip...")
                        # Extrayez les fichiers zip dans le dossier League of Legends
                        with zipfile.ZipFile(download_path, 'r') as zip_ref:
                            zip_ref.extractall(lol_directory)
                            print("R3nzSkin.zip folder extraction...")

                        # Supprimez le fichier zip temporaire
                        os.remove(download_path)
                        print("Delete folder R3nzSkin.zip...")

                        openGoodFile()
                        print("Opening the R3nSkin DLL Injector file...")
                        sys.exit()
                    else:
                        print("Unable to download file from GitHub.")
                        input("Press Enter to exit...")
                        sys.exit()
                else:
                    print("Asset file not found in latest version assets.")
                    input("Press Enter to exit...")
                    sys.exit()
            else:
                print("No assets found in the latest version.")
                input("Press Enter to exit...")
                sys.exit()
        else:
            print("Unable to retrieve information from the latest version.")
            input("Press Enter to exit...")
            sys.exit()

    def openGoodFile():
        # Recherche du fichier par description (par exemple, "R3nzSkin_Injector.exe")
        description_to_find = "R3nSkin DLL Injector"
        found_file = find_file_by_description(description_to_find, lol_directory)

        if found_file:
            print(f"The file '{description_to_find}' has been found: {found_file}")
            os.system(f'start /D "{lol_directory}" "" "{found_file}"')
            print("Opening the R3nSkin DLL Injector file...")
            sys.exit()
        else:
            print(f"The file '{description_to_find}' was not found.")
            sys.exit()

    description_to_find = "R3nSkin DLL Injector"
    found_file = find_file_by_description(description_to_find, lol_directory)

    if not found_file:
        # Les fichiers n'existent pas, exécutez le script
        exec_script()
        print("Close script...")
        sys.exit()
    else:
        # Les fichiers existent
        # Vérifier si la version de l'application est différente de la version dans settings_wau.json
        if checkVersionR3nSkin():
            # La version de l'application est différente de la version dans settings_wau.json
            # Exécutez le script
            exec_script()
            print("Close script...")
            sys.exit()
        else:
            # La version de l'application est la même que la version dans settings_wau.json
            # Ouvrez le fichier R3nSkin DLL Injector
            openGoodFile()
            print("Close script...")
            sys.exit()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "WhereAreU.py", None, 1)
            sys.exit()
        except Exception as e:
            print(f"Error when elevating privileges : {e}")
            sys.exit()

if not is_admin():
    # Vérifier si l'élévation de privilèges est déjà en cours
    if len(sys.argv) > 1 and sys.argv[1] == "elevated":
        main()
    else:
        # Demander des privilèges d'administrateur dès le début du script
        run_as_admin()
else:
    main()

if __name__ == "__main__":
    main()
    sys.exit()