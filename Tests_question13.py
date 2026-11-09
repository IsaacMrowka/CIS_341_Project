# Test A - Configuration File

import os
import system_security_daemon as daemon

config_file = os.path.join(os.path.dirname(__file__), "sysaudit.cfg")

settings = daemon.load_config(config_file)

if settings is not None and settings["max_safety_limit_mib"] == 100.0:
    print("PASS: Configuration loaded successfully")
else:
    print("FAIL: Configuration did not load correctly")
