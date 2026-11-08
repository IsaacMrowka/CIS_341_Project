import system_security_daemon as daemon

passed = 0
log = "/tmp/test.log"
settings = {
    "authorized_user": "auditmanager",
    "audit_group": "auditteam",
    "audit_directory": "/tmp",
}

def fake_crash():
    return 1 / 0


def fake_hacker():
    return "hacker"


def fake_auditmanager():
    return "auditmanager"

if daemon.error_exit(3, "test", log) == 3:
    print("PASS: Part 10 error gives exit 3")
    passed += 1
else:
    print("FAIL: Part 10 error gives exit 3")


real_main = daemon.main
daemon.main = fake_crash
if daemon.run() == 1:
    print("PASS: Part 10 crash is caught (exit 1)")
    passed += 1
else:
    print("FAIL: Part 10 crash is caught (exit 1)")
daemon.main = real_main

real_user = daemon.get_effective_user
daemon.get_effective_user = fake_hacker
if daemon.check_identity("auditmanager", log) == 2:
    print("PASS: Part 11 other users are blocked (exit 2)")
    passed += 1
else:
    print("FAIL: Part 11 other users are blocked (exit 2)")

daemon.get_effective_user = fake_auditmanager
if daemon.check_identity("auditmanager", log) == 0:
    print("PASS: Part 11 auditmanager is allowed (exit 0)")
    passed += 1
else:
    print("FAIL: Part 11 auditmanager is allowed (exit 0)")
daemon.get_effective_user = real_user

if daemon.delegate_access("fakeuser999", settings, log) == 6:
    print("PASS: Part 12 fake user is rejected (exit 6)")
    passed += 1
else:
    print("FAIL: Part 12 fake user is rejected (exit 6)")

print(f"\n{passed}/5 tests passed.")


