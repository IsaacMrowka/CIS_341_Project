import sys
import argparse

# Dictionary which contains the program's error codes

error_codes = {

0: "SUCCESS - Operational task ran to completion without tracking loops faults.",
1: "GENERIC_ERROR - An unmapped error condition triggered a process escape.",
2: "IDENTITY_VIOLATION - Process call called by an unverified account other than auditmanager.",
3: "CONFIGURATION_MISSING - The explicit target configuration layout file sysaudit.cfg was not found.",
4: "INVALID_WORKSPACE - Target mapping path /course_project/audit missing or is not a directory.",
5: "DISK_CEILING_REACHED - Workspace capacity validation failed critical storage envelope margins.",

}

def show_help_menu():
    print("""

==================================================
    SYSTEM HEALTH MONITOR & SECURITY DAEMON
==================================================

DESCRIPTION:
    This program monitors Linux system health, manages audit files, and performs schedule maintenance.

USAGE:
    python3 main.py [OPTIONS]

COMMAND LINE OPTIONS:
    -h, --help: 
        Displays this help menu

    --config FILE
        Specify the configuration file
        Default: sysaudit.cfg
    
    --cleanup
        Runs the audit cleanup process manually

    --status
        Display audit archive statistics

    --interval SECONDS
        Override the monitoring interval
    
    --max-size MB
        Override the maximum audit storage size
    
    -- delegate USER
        Delegate approved access to another user.

EXAMPLE COMMANDS:

    python3 main.py
    python3 main.py -h or python3 main.py --help
    python3 main.py --config sysaudit.cfg
    python3 main.py --cleanup
    python3 main.py --status
    python3 main.py --interval 60
    python3 main.py --max-size 100
    python3 main.py -- delegate student1

SAMPLE LOG OUTPUT:

    2026-11-06 10:00:00 [INFO] Audit scan started
    2026-11-06 10:00:01 [INFO] Audit report saved
    2026-11-06 10:00:02 [INFO] Sleeping for 60 seconds
    2026-11-09 00:00:00 [INFO] Cleanup started
    2026-11-09 00:00:01 [INFO] Audit files compressed
    2026-11-09 00:00:02 [INFO] Original files deleted

SAMPLE METRICS:
    Total Archive(s): 3
    Largest Archive: audit_2026_11_08.tar.gz
    Largest Archive Size: 2048 bytes
    Last Modified: 2026-11-08 09:30:00
    Disk Usage: 45 MB / 100 MB

SAMPLE WARNING:
    2026-11-06 10:00:03 [WARN] Storage limit reached
    2026-11-06 10:00:04 [ERROR] Configuration file missing
    2026-11-06 10:00:05 [ERROR] Unauthorized user

CONFIGURATION FILE: sysaudit.cfg

    (file information)

CONFIGURATION DICTIONARY STRUCTURE:

CONFIGURATION PRECEDENCE:

    1) Default settings are read by the program from sysaudit.cfg.
    2) Command-lin arguments override matching settings.
    3) Overrides apply only to the current execution

ERROR CODE DICTIONARY:
""")
    
    # Prints each error code in the dictionary and their meanings
    for code, message in error_codes.items():
        print(f"     {code}: {message}")

    print

def main ():

    # Show the USAGE Statement immediately if no args or help flag is used.
    if len (sys.argv) == 1 or "=h" in sys.argv or "--help" in sys.argv:
        show_help_menu()
        return 0 