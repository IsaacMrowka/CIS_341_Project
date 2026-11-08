
import os
import tarfile
from datetime import datetime


def cleanup(audit_folder):

    # Check if the folder exists
    if not os.path.isdir(audit_folder):
        print("Audit folder not found.")
        return 1

    # Find all .audit files
    files = []

    for file in os.listdir(audit_folder):
        if file.endswith(".audit"):
            path = os.path.join(audit_folder, file)

            if os.path.isfile(path):
                files.append(file)

    if len(files) == 0:
        print("No audit files found.")
        return 0

    # Create a name for the compressed file
    date = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = os.path.join(audit_folder, "backup_" + date + ".tar.gz")

    # Compress the files
    try:
        with tarfile.open(backup, "w:gz") as archive:
            for file in files:
                path = os.path.join(audit_folder, file)
                archive.add(path, arcname=file)

        # Delete the original files
        for file in files:
            os.remove(os.path.join(audit_folder, file))

        print("Backup created successfully.")
        print("Original audit files deleted.")
        return 0

    except Exception as error:
        print("Error:", error)
        return 1


if __name__ == "__main__":
    exit(cleanup("/course_project/audit/"))