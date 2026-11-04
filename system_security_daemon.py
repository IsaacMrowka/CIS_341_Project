import os

#part7
def audit_summary_log():
    
    #list of all archive files in the directory
    archives = [
                archive for archive in os.listdir(audit)
                if archive.endswith('.tar.gz')
    ]

    total_archives = len(archives)

    #check for archived files
    if total_archives == 0:
        print("No audit archives found.")
        return

    largest_file = None
    max_size =0

    #find the largest archive file
    for archive in archives:
        file_path = os.path.join(audit, archive)
        file_size = os.path.getsize(file_path)

        if file_size > max_size:
            max_size = file_size
            largest_file = archive

    #find modification time of the largest archive file
    largest_path = os.path.join(audit, largest_file)
    modification_time = os.path.getmtime(largest_path)

    file_summary = (
        f"Total audit archives: {total_archives}\n"
        f"Largest archive: {largest_file} ({max_size} bytes)\n"
        f"Last modified: {modification_time}\n"
    )

    print(file_summary)
    # TODO: Append file_summary to your /var/log/sysaudit_daemon.log tracking path

    #part8