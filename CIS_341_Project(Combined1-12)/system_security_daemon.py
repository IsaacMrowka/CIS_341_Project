import os
import configparser
from datetime import datetime
import sys
import time
import pwd
import re
import subprocess
def load_config(config_file):
    """Part 4: Read runtime settings from sysaudit.cfg."""
    if not os.path.exists(config_file):
        print(f"[ERROR] Configuration file not found: {config_file}", file=sys.stderr)
        return None

    config = configparser.ConfigParser()

    try:
        config.read(config_file)

        settings = {
            "audit_directory": config.get("AuditSettings", "audit_directory"),
            "max_safety_limit_mib": config.getfloat(
                "AuditSettings", "max_safety_limit_mib"
            ),
            "transaction_log_path": config.get(
                "AuditSettings", "transaction_log_path"
            ),
            "archive_retention_days": config.getint(
                "AuditSettings", "archive_retention_days"
            ),
        }

        return settings

    except (configparser.Error, ValueError) as error:
        print(f"[ERROR] Invalid configuration: {error}", file=sys.stderr)
        return None
def write_log(level, message, log_path):
    """Part 5: Append a timestamped INFO, WARN, or ERROR message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} [{level}] {message}\n"

    try:
        with open(log_path, "a") as log_file:
            log_file.write(log_message)
        return True
    except OSError as error:
        print(f"[ERROR] Could not write to log: {error}", file=sys.stderr)
        return False
def delete_old_archives(audit_dir, retention_days, log_path):
    """Part 6: Delete .tar.gz archives older than the configured retention period."""
    if not os.path.isdir(audit_dir):
        print(f"[ERROR] Audit directory does not exist: {audit_dir}", file=sys.stderr)
        return 0

    deleted_count = 0
    current_time = time.time()

    for file_name in os.listdir(audit_dir):
        if file_name.endswith(".tar.gz"):
            file_path = os.path.join(audit_dir, file_name)

            if not os.path.isfile(file_path):
                continue

            try:
                modified_time = os.path.getmtime(file_path)
                age_days = (current_time - modified_time) / 86400

                if age_days > retention_days:
                    os.remove(file_path)
                    deleted_count += 1
                    write_log(
                        "INFO",
                        f"Deleted old archive: {file_name} ({age_days:.1f} days old)",
                        log_path,
                    )
            except OSError as error:
                write_log(
                    "ERROR",
                    f"Could not process archive {file_name}: {error}",
                    log_path,
                )

    return deleted_count
def audit_summary_log(audit_dir, log_path):
    try:
        archives = [
            archive
            for archive in os.listdir(audit_dir)
            if archive.endswith(".tar.gz")
        ]
    except OSError as error:
        write_log("ERROR", f"Could not read audit directory: {error}", log_path)
        return

    total_archives = len(archives)

    if total_archives == 0:
        print("No audit archives found.")
        write_log("INFO", "No audit archives found during summary scan", log_path)
        return

    largest_file = None
    max_size = 0

    for archive in archives:
        file_path = os.path.join(audit_dir, archive)
        file_size = os.path.getsize(file_path)

        if file_size > max_size:
            max_size = file_size
            largest_file = archive

    largest_path = os.path.join(audit_dir, largest_file)
    modification_time = os.path.getmtime(largest_path)
    format_mod_time = datetime.fromtimestamp(modification_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_summary = (
        f"Total audit archives: {total_archives}\n"
        f"Largest archive: {largest_file} ({max_size} bytes)\n"
        f"Last modified: {format_mod_time}\n"
    )

    print(file_summary)
    write_log(
        "INFO",
        f"Archive summary - total: {total_archives}, largest: {largest_file}, "
        f"size: {max_size} bytes, modified: {format_mod_time}",
        log_path,
    )
#error codes, 0-5 are from the project guide
# Source - https://man7.org/linux/man-pages/man3/sysexits.h.3head.html
# Retrieved 2026-11-08
EXIT_MESSAGES = {
    0: "SUCCESS: Task ran to completion",
    1: "GENERIC_ERROR: An unexpected error occurred",
    2: "IDENTITY_VIOLATION: Only auditmanager can run this program",
    3: "CONFIGURATION_MISSING: sysaudit.cfg was not found or is invalid",
    4: "INVALID_WORKSPACE: Audit directory is missing or not a directory",
    5: "DISK_CEILING_REACHED: Workspace is over the storage limit",
    6: "USER_NOT_FOUND: The user to delegate to does not exist",
    7: "DELEGATION_FAILED: Could not give access to the user",
    8: "INVALID_ARGUMENT: A command-line value is missing or invalid",
}
#prints the error to stderr, logs it and gives back the exit code
# Source - https://stackoverflow.com/a/14981125
# Posted by MarcH, modified by community.
# Retrieved 2026-11-08, License - CC BY-SA 4.0
# Source - https://docs.python.org/3/library/sys.html#sys.exit
# Retrieved 2026-11-08
def error_exit(code, detail, log_path=None):
    message = f"{EXIT_MESSAGES[code]} ({detail})"
    print(f"[ERROR] Exit {code} - {message}", file=sys.stderr)

    if log_path:
        write_log("ERROR", f"Exit {code} - {message}", log_path)

    return code

#reads the allowed user and group from sysaudit.cfg
# Source - https://docs.python.org/3/library/configparser.html
# Retrieved 2026-11-08
def load_security_settings(config_file):
    config = configparser.ConfigParser()

    try:
        config.read(config_file)
        return {
            "authorized_user": config.get("SecuritySettings", "authorized_user"),
            "audit_group": config.get("SecuritySettings", "audit_group"),
        }
    except configparser.Error as error:
        print(f"[ERROR] Invalid security settings: {error}", file=sys.stderr)
        return None
def get_effective_user():
    return pwd.getpwuid(os.geteuid()).pw_name


def check_identity(authorized_user, log_path):
    try:
        current_user = get_effective_user()
    except KeyError as error:
        return error_exit(1, f"Could not read user: {error}", log_path)

    if current_user != authorized_user:
        write_log("WARN", f"Access denied for user: {current_user}", log_path)
        return error_exit(2, f"User was {current_user}", log_path)

    write_log("INFO", f"Identity verified: {current_user}", log_path)
    return 0

# Source - https://docs.python.org/3/library/pwd.html#pwd.getpwnam
# Retrieved 2026-11-08
def user_exists(user_name):
    try:
        pwd.getpwnam(user_name)
        return True
    except KeyError:
        return False

# Source - https://man7.org/linux/man-pages/man8/useradd.8.html
# Source - https://docs.python.org/3/library/subprocess.html#subprocess.run
# Source - https://man7.org/linux/man-pages/man8/usermod.8.html
# Source - https://man7.org/linux/man-pages/man1/chmod.1.html
# Retrieved 2026-11-08
def delegate_access(target_user, settings, log_path):
    audit_group = settings["audit_group"]
    audit_dir = settings["audit_directory"]
    if not target_user or not re.fullmatch(r"[a-z_][a-z0-9_-]*", target_user):
        return error_exit(8, f"Invalid username: {target_user}", log_path)

    if target_user == settings["authorized_user"]:
        return error_exit(8, "Cannot delegate to yourself", log_path)

    if not user_exists(target_user):
        return error_exit(6, target_user, log_path)
    try:
        group_check = subprocess.run(["getent", "group", audit_group], capture_output=True)
        if group_check.returncode != 0:
            subprocess.run(["sudo", "groupadd", audit_group], check=True)
        subprocess.run(["sudo", "chgrp", "-R", audit_group, audit_dir], check=True)
        subprocess.run(["sudo", "chmod", "2770", audit_dir], check=True)
        subprocess.run(["sudo", "usermod", "-aG", audit_group, target_user], check=True)

    except (subprocess.CalledProcessError, OSError) as error:
        return error_exit(7, str(error), log_path)

    write_log("INFO", f"Gave {target_user} access to {audit_dir} through group {audit_group}", log_path)
    print(f"Access granted: {target_user} added to group {audit_group}")
    return 0



def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(project_dir, "sysaudit.cfg")

    settings = load_config(config_file)
    if settings is None:
        return error_exit(3, config_file)

    max_limit = settings["max_safety_limit_mib"]
    audit_dir = settings["audit_directory"]
    log_path = settings["transaction_log_path"]
    retention_days = settings["archive_retention_days"]
    if not os.path.isdir(audit_dir):
        return error_exit(4, audit_dir)

    security = load_security_settings(config_file)
    if security is None:
        return error_exit(3, "Missing [SecuritySettings] in sysaudit.cfg")
    settings.update(security)

    result = check_identity(settings["authorized_user"], log_path)
    if result != 0:
        return result

    # Source - https://stackoverflow.com/a/63416492
    # Posted by Sameer Ali VP, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-08, License - CC BY-SA 4.0
    # Source - https://docs.python.org/3/library/sys.html#sys.argv
    # Source - https://docs.python.org/3/library/stdtypes.html#str.startswith
    # Source - https://docs.python.org/3/library/stdtypes.html#str.split
    # Retrieved 2026-11-08
    for argument in sys.argv[1:]:
        if argument.startswith("delegate="):
            target_user = argument.split("=", 1)[1]
            return delegate_access(target_user, settings, log_path)
    # Source - https://stackoverflow.com/a/63416492
    # Posted by Sameer Ali VP, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-06, License - CC BY-SA 4.0
    for argument in sys.argv[1:]:
        if "=" in argument:
            key, value = argument.split("=", 1)

            if key == "max_limit":
                try:
                    max_limit = float(value)
                    print(
                        f"[CLI OVERRIDE] Temporarily setting limit to: "
                        f"{max_limit} MiB"
                    )
                except ValueError:
                    #jaspreet - part 10: exit 8 through error_exit
                    return error_exit(8, "max_limit must be a number", log_path)
    write_log("INFO", "Audit scan started", log_path)
    deleted_count = delete_old_archives(audit_dir, retention_days, log_path)
    write_log(
        "INFO",
        f"Archive cleanup completed. Removed {deleted_count} old archive(s)",
        log_path,
    )
    # Source - https://stackoverflow.com/a/1392549
    # Posted by monkut, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-06, License - CC BY-SA 4.0
    total_bytes = 0

    for root, dirs, files in os.walk(audit_dir):
        for file in files:
            file_path = os.path.join(root, file)

            if not os.path.islink(file_path):
                total_bytes += os.path.getsize(file_path)

    total_mib = total_bytes / (2**20)
    print(
        f"Current Size: {total_mib:.2f} MiB "
        f"(Configured Envelope Limit: {max_limit} MiB)"
    )

    if total_mib > max_limit:
        warning_message = (
            f"HIGH-PRIORITY: Envelope limit breached! Size: {total_mib:.2f} MiB"
        )
        write_log("WARN", warning_message, log_path)
        print("[ALERT] High-priority flag dispatched to transaction log.")
    audit_summary_log(audit_dir, log_path)
    write_log("INFO", "Audit scan completed", log_path)
    return 0
# Source - https://docs.python.org/3/tutorial/errors.html
# Retrieved 2026-11-08
def run():
    try:
        return main()
    except KeyboardInterrupt:
        print("[WARN] Program stopped by user", file=sys.stderr)
        return 1
    except Exception as error:
        return error_exit(1, f"Unexpected error: {error}")
if __name__ == "__main__":
    sys.exit(run())