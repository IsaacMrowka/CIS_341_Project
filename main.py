
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

    python3 main.py
    python3 main.py -h
    python3 main.py --help
    python3 main.py max_limit=150
    python3 main.py delegate=student1

SAMPLE LOG OUTPUT:

    2026-11-06 10:00:00 [INFO] Audit scan started
    2026-11-06 10:00:01 [INFO] Archive cleanup completed. Removed 0 old archive(s)
    2026-11-06 10:00:02 [INFO] Audit scan completed

SAMPLE ARCHIVE SUMMARY:

    Total audit archives: 3
    Largest archive: audit_2026_11_08.tar.gz (2048 bytes)
    Last modified: 2026-11-08 09:30:00

SAMPLE STORAGE OUTPUT:

    Current Size: 45.00 MiB (Configured Envelope Limit: 100.0 MiB)

SAMPLE WARNING:

    2026-11-06 10:00:03 [WARN] HIGH-PRIORITY:
    Envelope limit breached! Size: 105.00 MiB

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
