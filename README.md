**CIS 341 – System Health Monitor & Security Auditing Daemon**

**About the Project:**

This project is a Linux system monitoring and security auditing program developed using Python. The program monitors audit files, checks storage usage, manages old archives, and automatically compresses .audit files every three days at midnight. It uses systemd to run in the background and schedule cleanup tasks.

**Requirements:**

Before starting, make sure you have:

1) A Linux computer with systemd (we used Kali Linux)

2) Python 3

3) Git

4) Administrator (sudo) access

5) acl package 

**Setup Instructions:**

These steps explain how to set up the project on another Linux computer.

**Step 1: Download the Project:**

Clone the GitHub repository in your Home folder and open the project folder.

1) cd ~

2) git clone https://github.com/IsaacMrowka/CIS_341_Project

3) cd CIS_341_Project

**Step 2: Create the Required User and Group**

The program runs under a Linux user called auditmanager and uses a group called auditteam.

Run these commands to create them:

1) sudo groupadd -f auditteam

2) getent group auditteam >/dev/null || sudo groupadd auditteam

3) sudo usermod -aG auditteam auditmanager

**Step 3: Create the Audit Folder**

The program stores its audit files in /course_project/audit.

Create the folder and give auditmanager access to it.

1) sudo mkdir -p /course_project/audit

2) sudo chown auditmanager:auditteam /course_project/audit

3) sudo chmod 750 /course_project/audit

**Step 4: Update the File Paths**
The systemd service files contain paths to the project folder. These paths will be different depending on where the project is saved.

First, find your project folder path: pwd

Open sysaudit.service and sysaudit-cleanup.service.

Replace _Working Directory_ = "INSTER PWD HERE" with your own project folder path.

For example, if your project is saved in /home/student/CIS_341_Project, the paths should look like this:

**In sysaudit.service:**

WorkingDirectory=/home/student/CIS_341_Project

ExecStart=/usr/bin/python3 -u /home/student/CIS_341_Project/daemon_runner.py

**In sysaudit-cleanup.service:**

WorkingDirectory=/home/student/CIS_341_Project

ExecStart=/usr/bin/python3 /home/student/CIS_341_Project/cleanup.py

Leave the other settings unchanged.

**Step 5: Give auditmanager Access to the Project**

Since the program runs as auditmanager, this user needs permission to read the project files.

Replace /home/student in the commands below with your own Linux home directory.

1) sudo setfacl -m u:auditmanager:--x /home/student

2) sudo setfacl -m u:auditmanager:r-x /home/student/CIS_341_Project

3) sudo setfacl -m u:auditmanager:r-- /home/student/CIS_341_Project/*.py

4) sudo setfacl -m u:auditmanager:r-- /home/student/CIS_341_Project/sysaudit.cfg

If setfacl is not available, install it using:

sudo apt install acl

**Step 6: Install the systemd Files**

From the project folder, copy the service files and timer to the systemd directory.

1) sudo cp sysaudit.service /etc/systemd/system/

2) sudo cp sysaudit-cleanup.service /etc/systemd/system/

3) sudo cp sysaudit-cleanup.timer /etc/systemd/system/

Then reload systemd:

4) sudo systemctl daemon-reload

**Step 7: Start the Services**

Enable and start the monitoring service and cleanup timer.

1) sudo systemctl enable --now sysaudit.service

2) sudo systemctl enable --now sysaudit-cleanup.timer

This allows the monitoring service and cleanup timer to start automatically when the computer boots.

**Running the Program Manually**

The monitoring program must run as auditmanager. If another user tries to run a monitoring command, the program will return an identity error (exit code 2).

To run commands as auditmanager, add sudo -u auditmanager before python3.

**Display the Help Menu**

1) python3 main.py

2) python3 main.py -h

3) python3 main.py --help

These commands display the help menu. You do not need to use auditmanager for this.

**Run a Monitoring Scan**

The program uses a default storage limit of 100 MiB, which can be changed using the max_limit argument.

Run a scan with a 100 MiB limit:

4) sudo -u auditmanager python3 main.py max_limit=100

Run a scan with a 150 MiB limit:

5) sudo -u auditmanager python3 main.py max_limit=150

The storage limit override only applies to that execution. It does not permanently change sysaudit.cfg.

Delegate Access to Another User

The delegate argument can be used to grant an existing Linux user access to the audit group.

6) sudo visudo

7) auditmanager ALL=(root) NOPASSWD: /usr/sbin/usermod, /usr/sbin/groupadd, /usr/bin/chgrp, /usr/bin/chmod

8) sudo -u auditmanager python3 main.py delegate=student1

Replace student1 with an existing username.

This operation may require additional Linux permissions.

Run the Cleanup Script

To manually compress and remove .audit files, run:

9) sudo -u auditmanager python3 cleanup.py

The program creates a compressed .tar.gz archive and deletes the original .audit files after successful compression.

Note: When using systemctl, you do not need to specify auditmanager. The systemd services are already configured to run under this account.

**Testing the Project**

**1. Check the Monitoring Service**

sudo systemctl status sysaudit.service

The service should show active (running).

**2. Check the Cleanup Timer**

sudo systemctl status sysaudit-cleanup.timer

The timer should show active (waiting).

**3. Test the Help Menu**

python3 main.py --help

This should display the program's usage instructions, available arguments, configuration settings, sample logs, and error codes.

**4. Test an Invalid Argument**

python3 main.py --wrong

echo $?

The program should display an invalid argument error and return exit code 8.

**5. Test the Cleanup Service**

sudo systemctl start sysaudit-cleanup.service

sudo systemctl status sysaudit-cleanup.service

The service should complete successfully. It may show inactive (dead) afterward because it only runs when needed.

**6. View the Audit Logs**

**7. Automated Functionality Tests**

Run automated tests using:
python3 Tests_question13.py

The tests check configuration loading, boundary values, missing configuration files, invalid directories, malformed configurations, storage limit warnings, and unauthorized user access.

The program should display PASS messages when the tests succeed. Some ERROR messages are expected because the tests intentionally check invalid conditions.




sudo tail -n 20 /course_project/audit/sysaudit_daemon.log

This displays recent audit activity, including monitoring scans and archive information.

**Additional Notes:**

•	The main configuration file is sysaudit.cfg.

•	Audit files are stored in /course_project/audit.

•	The monitoring program runs under the auditmanager account.

•	The cleanup timer runs at midnight on the 1st, 4th, 7th, 10th, and so on of each month.

•	Make sure the project files are accessible to auditmanager.

•	The program was developed and tested on Kali Linux. Other Linux systems may require small changes during setup.

