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


# Test B Missing Configuration File

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

print("PASS: Test C" if result == 4 else "FAIL: Test C")
