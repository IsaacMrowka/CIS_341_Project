# Test A - Configuration File
import system_security_daemon as daemon

settings = daemon.load_config("sysaudit.cfg")

if settings is not None:
    print("PASS: Configuration loaded")
else:
    print("FAIL: Configuration not loaded")

for limit in [0, 1, 100]:
    config = open("sysaudit.cfg").read()
    open("test.cfg", "w").write(config.replace("100.0", str(limit)))
    settings = daemon.load_config("test.cfg")
    print("PASS" if settings and settings["max_safety_limit_mib"] == limit else "FAIL", limit)


# Test B - Missing Configuration File

settings = daemon.load_config("missing.cfg")

if settings is None:
    print("PASS: Missing configuration file detected")
else:
    print("FAIL: Missing configuration file not detected")
