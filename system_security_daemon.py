import os
import configparser
from datetime import datetime
import sys

#from part 8
config = configparser.ConfigParser()
config_file = "/home/imrow/Projects/CIS_341_Project/sysaudit.cfg"

max_limit = 100.0
audit_dir = "/home/imrow/Projects/CIS_341_Project/course_project/audit/"
log_path = "/home/imrow/Projects/CIS_341_Project/course_project/audit/transactions.log"

if os.path.exists(config_file):
    config.read(config_file)
    # Load settings from file into our resolution registers
    max_limit = config.getfloat("AuditSettings", "max_safety_limit_mib")


# Source - https://stackoverflow.com/a/63416492
# Posted by Sameer Ali VP, modified by community. See post 'Timeline' for change history
# Retrieved 2026-11-06, License - CC BY-SA 4.0

#from part 9
for argument in sys.argv[1:]:
    if "=" in argument:

        key, value = argument.split("=", 1)
        
        if key == "max_limit":
            max_limit = float(value)
            print(f"[CLI OVERRIDE] Temporarily setting limit to: {max_limit} MiB")

#part7
def audit_summary_log(audit_dir):

    archives = [
                archive for archive in os.listdir(audit_dir)
                if archive.endswith('.tar.gz')
    ]

    total_archives = len(archives)

    if total_archives == 0:
        print("No audit archives found.")
        return

    largest_file = None
    max_size =0

    for archive in archives:
        file_path = os.path.join(audit_dir, archive)
        file_size = os.path.getsize(file_path)

        if file_size > max_size:
            max_size = file_size
            largest_file = archive

    #find modification time of the largest archive file
    largest_path = os.path.join(audit_dir, largest_file)
    modification_time = os.path.getmtime(largest_path)
    format_mod_time = datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M:%S")
  
    file_summary = (
        f"Total audit archives: {total_archives}\n"
        f"Largest archive: {largest_file} ({max_size} bytes)\n"
        f"Last modified: {format_mod_time}\n"
    )
    print(file_summary)


#for part 8
total_bytes = 0

# Source - https://stackoverflow.com/a/1392549
# Posted by monkut, modified by community. See post 'Timeline' for change history
# Retrieved 2026-11-06, License - CC BY-SA 4.0
if os.path.exists(audit_dir):
    for root, dirs, files in os.walk(audit_dir):
        for file in files:
            file_path = os.path.join(root, file)
    
            if not os.path.islink(file_path):
                total_bytes += os.path.getsize(file_path)

    total_mib = total_bytes / (2**20)
    print(f"Current Size: {total_mib:.2f} MiB (Configured Envelope Limit: {max_limit} MiB)")

    baseline_limit = 100.0

    if total_mib > max_limit:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        warning_flag = f"{timestamp} [WARNING] HIGH-PRIORITY: Envelope limit breached! Size: {total_mib:.2f} MiB\n"
        
        with open(log_path, "a") as f:
            f.write(warning_flag)
        print("[ALERT] High-priority flag dispatched to transaction log.")
else:
    print(f"Directory {audit_dir } defined in config does not exist.")

audit_summary_log(audit_dir)