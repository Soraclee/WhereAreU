import os
import time
import zipfile

def delete_build():
    # Delete build folder and dist folder
    if os.path.exists("build"):
        os.system("rd /s /q build")
    if os.path.exists("dist"):
        os.system("rd /s /q dist")

def start_build_WhereAreU_AutoUpdate():
    # Start build for WhereAreU.py and AutoUpdate.py
    os.system("pyinstaller --onefile WhereAreU.py")
    os.system("pyinstaller --onefile AutoUpdate.py")

def create_zip_with_files():
    # Liste des fichiers à ajouter au ZIP
    # Liste des fichiers à ajouter au ZIP
    files_to_zip = ["dist/WhereAreU.exe", "dist/AutoUpdate.exe"]

    # Nom du fichier ZIP de sortie
    zip_filename = "dist/WhereAreU.zip"

    # Vérification si les fichiers sont bien présents
    all_files_exist = all([os.path.exists(file) for file in files_to_zip])

    if all_files_exist:
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_zip:
                # Ajouter chaque fichier au ZIP
                zipf.write(file_path, arcname=os.path.basename(file_path))  # Utilisez uniquement le nom de fichier

        print(f"Le fichier {zip_filename} a été créé avec succès.")
    else:
        print("Erreur : les fichiers nécessaires n'existent pas.")

def main():
    # Delete build folder and dist folder
    delete_build()

    # Start build for WhereAreU.py and AutoUpdate.py
    start_build_WhereAreU_AutoUpdate()

    # Create zip with files
    create_zip_with_files()

if __name__ == "__main__":
    main()
