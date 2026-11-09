# Configuration File
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


# Missing Configuration File
original = daemon.load_config
daemon.load_config = lambda file: None
result = daemon.main()
daemon.load_config = original
if result == 3:
    print("PASS: Missing configuration detected")
else:
    print("FAIL: Missing configuration not detected")


#Invalid Directory
original = daemon.load_config
settings = original("sysaudit.cfg")
settings["audit_directory"] = "/invalid_directory"
daemon.load_config = lambda file: settings
result = daemon.main()
daemon.load_config = original
print("PASS: Invalid directory detected" if result == 4 else "FAIL: invalid directory not detected")


#Malformed Configuration
config = open("sysaudit.cfg").read()
open("bad.cfg", "w").write(config.replace("100.0", "wrong"))
settings = daemon.load_config("bad.cfg")
if settings is None:
    print("PASS: malformed config detected")
else:
    print("FAIL: Malformed config not detected")


#Storage Limit
import sys
original = daemon.get_effective_user
daemon.get_effective_user = lambda: "auditmanager"
sys.argv = ["test", "max_limit=0.0000001"]
result = daemon.main()
daemon.get_effective_user = original
sys.argv = ["test"]
print("PASS: storage limit warning" if result == 0 else "FAIL: storage limit warning")


#Unauthorized User
result = daemon.check_identity("auditmanager", "/tmp/test_f.log")
if result == 2:
    print("Pass: Unauthorized user Blocked")
else:
    print("FAIL: Unauthorized user not blocked")
