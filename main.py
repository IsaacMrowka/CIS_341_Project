
import sys
import subprocess

# Dictionary containing the program's error codes
error_codes = {
    0: "SUCCESS - Program completed successfully.",
    1: "GENERIC_ERROR - Unexpected error occurred.",
    2: "IDENTITY_VIOLATION - User is not auditmanager.",
    3: "CONFIGURATION_MISSING - Configuration file missing or invalid.",
    4: "INVALID_WORKSPACE - Audit directory is missing.",
    5: "DISK_CEILING_REACHED - Storage limit exceeded.",
    6: "USER_NOT_FOUND - Delegation user does not exist.",
    7: "DELEGATION_FAILED - Could not grant user access.",
    8: "INVALID_ARGUMENT - Invalid command-line argument."
}


def show_help_menu():
    print("""
==================================================
    SYSTEM HEALTH MONITOR & SECURITY DAEMON
==================================================

DESCRIPTION:
    This program monitors Linux system health, manages
    audit files, and performs scheduled maintenance.

USAGE:
    python3 main.py [OPTIONS]

COMMAND LINE OPTIONS:

    -h, --help
        Display this help menu.

    max_limit=NUMBER
        Override the maximum storage limit in MiB.
        Example: max_limit=150

    delegate=USERNAME
        Grant an existing user access to the audit group.
        Example: delegate=student1

EXAMPLE COMMANDS:

    Display the help menu:
        python3 main.py
        python3 main.py -h
        python3 main.py --help

    Run a monitoring scan with a 150 MiB limit:
        sudo -u auditmanager python3 main.py max_limit=150

    Run a monitoring scan with a 100 MiB limit:
        sudo -u auditmanager python3 main.py max_limit=100

    Delegate access to an existing user:
        sudo -u auditmanager python3 main.py delegate=student1

    Run the cleanup script manually:
        sudo -u auditmanager python3 cleanup.py

IMPORTANT:
    Monitoring commands must run as auditmanager.
    Running them as another user will return exit code 2.

    The systemd services already run as auditmanager,
    so sudo -u auditmanager is not needed for systemctl.

SAMPLE LOG OUTPUT (sysaudit_daemon.log):

    2026-11-08 14:47:50 [INFO] Identity verified: auditmanager
    2026-11-08 14:47:50 [INFO] Audit scan started
    2026-11-08 14:47:50 [INFO] Archive cleanup completed. Removed 0 old archive(s)
    2026-11-08 14:47:50 [INFO] Archive summary - total: 1, largest: backup_20261108_141902_630922.tar.gz, size: 255 bytes, modified: 2026-11-08 14:19:02
    2026-11-08 14:47:50 [INFO] Audit scan completed

SAMPLE MONITORING OUTPUT:

    Starting audit scan...
    Current Size: 0.01 MiB (Configured Envelope Limit: 100.0 MiB)
    Total audit archives: 1
    Largest archive: backup_20261108_141902_630922.tar.gz (255 bytes)
    Last modified: 2026-11-08 14:19:02
    Waiting 60 seconds...

SAMPLE ARCHIVE METRICS:

    Total audit archives: 1
    Largest archive: backup_20261108_141902_630922.tar.gz (255 bytes)
    Last modified: 2026-11-08 14:19:02

SAMPLE STORAGE METRICS:

    Current Size: 0.02 MiB (Configured Envelope Limit: 100.0 MiB)

SAMPLE WARNING (from storage limit testing):

    2026-11-06 20:49:36 [WARNING] HIGH-PRIORITY:
    Envelope limit breached! Size: 173.79 MiB

CONFIGURATION FILE: sysaudit.cfg

    [AuditSettings]
    audit_directory = /course_project/audit
    max_safety_limit_mib = 100.0
    transaction_log_path = /course_project/audit/sysaudit_daemon.log
    archive_retention_days = 14

    [SecuritySettings]
    authorized_user = auditmanager
    audit_group = auditteam

CONFIGURATION DICTIONARY STRUCTURE:

    {
        "audit_directory": "/course_project/audit",
        "max_safety_limit_mib": 100.0,
        "transaction_log_path": "/course_project/audit/sysaudit_daemon.log",
        "archive_retention_days": 14,
        "authorized_user": "auditmanager",
        "audit_group": "auditteam"
    }

CONFIGURATION PRECEDENCE:

    1. Settings are read from sysaudit.cfg.
    2. Command-line overrides replace matching settings.
    3. Overrides apply only to the current execution.

    Example:
        python3 main.py max_limit=150

ERROR CODE DICTIONARY:
""")

    # Print all error codes
    for code, message in error_codes.items():
        print(f"    {code}: {message}")

    print("==================================================")

# https://www.w3schools.com/python/ref_module_argparse.asp 
def main():

    # Show help when no arguments are given
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        show_help_menu()
        return 0

    # Check if the user entered a supported argument
    for argument in sys.argv[1:]:
        if not (argument.startswith("max_limit=") or
                argument.startswith("delegate=")):
            print("ERROR: Invalid command-line argument.", file=sys.stderr)
            return 8

    # Run the teammates' program
    result = subprocess.run(
        [sys.executable, "system_security_daemon.py"] + sys.argv[1:]
    )

    return result.returncode


# Start the program
if __name__ == "__main__":
    sys.exit(main())
