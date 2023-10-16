import ctypes
import json
import os
import subprocess
import sys
import zipfile
import psutil
import requests

def main():
    settings_file = "settings_wau.json"
    settings_json_default = {
        "lol_directory": "C:\\Riot Games\\League of Legends",
        "first_time": True,
        "version": "1.0.0",
        "versionWhereAreU": "1.0.0"
    }

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
                if first_time:
                    league_of_legends_path = find_league_of_legends_on_all_disks()
                    current_directory = league_of_legends_path

                    settings_json_default["lol_directory"] = current_directory
                    settings_json_default["first_time"] = False
                    with open(settings_file, "w") as f:
                        json.dump(settings_json_default, f, indent=4)
        else:
            print(f"The file '{settings_file}' does not exist.")
            print("Creating the file...")
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

    def checkVersionWhereAreU():
        # Create a session to avoid GitHub API rate limits
        session = requests.Session()
        session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WhereAreU-GitHub"
        })

        # Get information about the latest repository version
        release_url = "https://api.github.com/repos/Soraclee/WhereAreU/releases/latest"
        response = session.get(release_url)
        print("Checking for the latest script version...")

        if response.status_code == 200:
            print("Retrieving information about the latest version...")
            release_info = response.json()
            print(f"The latest script version is: {release_info['tag_name']}")
            version_app = release_info['tag_name']

            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    settings_json = json.load(f)
                    version_settings = settings_json.get("versionWhereAreU")

                settings_json["versionWhereAreU"] = version_app

                if version_settings != version_app:
                    print(f"Version in settings_wau.json: {version_settings} | GitHub version: {version_app}")
                    print("The script version is different from the version in settings_wau.json")
                    
                    with open(settings_file, "w") as f:
                        print("Updating the version in settings_wau.json with the new version")
                        json.dump(settings_json, f, indent=4)

                    print("Downloading the new version and installing it in the WhereAreU.exe folder")
                    download_url = release_info["assets"][0]["browser_download_url"]
                    print("Download URL: " + download_url)
                    download_path = "temp.zip"
                    whereAreU_path = "WhereAreU.exe"
                    response = session.get(download_url)
                    print("Downloading the WhereAreU.zip folder...")

                    if response.status_code == 200:
                        with open(download_path, 'wb') as f:
                            print("Opening the WhereAreU.zip folder...")
                            f.write(response.content)

                        if os.path.exists(whereAreU_path):
                            print("Closing the script...")
                            os.system(f'taskkill /F /IM {whereAreU_path}')
                            print("Closing the WhereAreU.exe file...")
                            os.remove(whereAreU_path)

                        with zipfile.ZipFile(download_path, 'r') as zip_ref:
                            print("In the zip...")
                            zip_ref.extractall(os.getcwd())
                            print("Extracting the WhereAreU.zip folder")

                        os.remove(download_path)
                        print("Deleting the WhereAreU.zip folder")
                    else:
                        print("Unable to download the file from GitHub.")
                        input("Press Enter to exit...")
                        sys.exit()

                    print("Restarting the script...")
                    os.startfile("WhereAreU.exe")
                    sys.exit()
                else:
                    print("The script version is identical to the version in settings_wau.json")
                    print("Restarting the script...")
                    os.startfile("WhereAreU.exe")
                    sys.exit()
            else:
                print(f"The file '{settings_file}' does not exist.")
                print("Creating the file...")
                with open(settings_file, "w") as f:
                    json.dump(settings_json_default, f, indent=4)
                print(f"The file '{settings_file}' has been created.")
                print("Restarting the script...")
                os.startfile("WhereAreU.exe")
                sys.exit()
        else:
            print("Unable to retrieve information about the latest version.")
        return False

    checkVersionWhereAreU()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "AutoUpdate.py", None, 1)
            sys.exit()
        except Exception as e:
            print(f"Error when elevating privileges: {e}")
            sys.exit()

if not is_admin():
    # Check if privilege elevation is already in progress
    if len(sys.argv) > 1 and sys.argv[1] == "elevated":
        main()
    else:
        # Request administrator privileges from the beginning of the script
        run_as_admin()
else:
    main()

if __name__ == "__main__":
    main()
    sys.exit()
