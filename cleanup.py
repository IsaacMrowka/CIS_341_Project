import os
import tarfile
from datetime import datetime

def cleanup(audit_folder):

    # Does the folder exist?
    if not os.path.isdir(audit_folder):
        print("Audit folder not found")
        return

    # Find all .audit files
    files = []

    for file in os.listdir(audit_folder):
        if file.endswith("audit"):
            path = os.path.join(audit_folder, file)

            if os.path.isfile(path):
                files.append(file)

    if len(files) == 0:
        print("No audit files found")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        print("Backup created successfully")
        print("Original audit files deleted")

    except Exception as error:
        print("Error:", error)

# Run only when the file is started directly
if __name__ == "__main__":
    cleanup("/course_project/audit/")
                    