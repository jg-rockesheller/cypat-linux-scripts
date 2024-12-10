import subprocess
import os
import re


# script for states round 2024-2025 season


packages = ["ufw", "clamav", "libpam-cracklib", "rkhunter", "gpasswd"]


os.system("apt update -y && apt upgrade -y")
os.system("apt install -y " + " ".join(packages))


# pam password settings
## /etc/pam.d/common-password
new_common_password = []
pam_configs = {
    "cracklib": {
        "found": False,
        "line": "password requisite pam_cracklib.so retry=3 minlen=8 difok=3 reject_username minclass=3 maxrepeat=2 dcredit=1 ucredit=1 lcredit=1 ocredit=0"
    },
    "pwhistory": {
        "found": False,
        "line": "password requisite pam_pwhistory.so use_authok remember=24 enforce_for_root"
    },
    "unix": {
        "found": False,
        "line": "password [success=1 default=ignore] pam_unix.so obscure use_authok sha512 shadow"
    }
}
for line in subprocess.check_output("cat /etc/pam.d/common-password", shell = True, text = True).split("\n"):
    if re.search("^.*pam_cracklib.so.*$", line):
        new_common_password += [pam_configs["cracklib"]["line"]]
        pam_configs["cracklib"]["found"] = True
    elif re.search("^.*pam_pwhistory.so.*$", line):
        new_common_password += [pam_configs["pwhistory"]["line"]]
        pam_configs["pwhistory"]["found"] = True
    elif re.search("^.*pam_unix.so.*$", line):
        new_common_password += [pam_configs["unix"]["line"]]
        pam_configs["unix"]["found"] = True
    else:
        new_common_password += [line]
for config in pam_configs:
    if pam_configs[config]["found"] == True: continue
    new_common_password += [pam_configs[config]["line"]]
with open("common-password", "w") as file:
    for line in new_common_password: file.write(line + "\n")
os.system("cp --no-preserve=mode,ownership ./common-password /etc/pam.d/common-password")
os.system("rm ./common-password")
## /etc/login.defs
new_login_defs = []
for line in subprocess.check_output("cat /etc/login.defs", shell = True, text = True).split("\n"):
    if re.search("^PASS_MAX_DAYS.*$", line): new_login_defs += ["PASS_MAX_DAYS   90"]
    elif re.search("^PASS_MIN_DAYS.*$", line): new_login_defs += ["PASS_MIN_DAYS   7"]
    elif re.search("^PASS_WARN_AGE.*$", line): new_login_defs += ["PASS_WARN_AGE   14"]
    else: new_login_defs += [line]
with open("login.defs", "w") as file:
    for line in new_login_defs: file.write(line + "\n")
os.system("cp --no-preserve=mode,ownership ./login.defs /etc/login.defs")
os.system("rm ./login.defs")


# user/group mamagement
users = []
for line in subprocess.check_output("cat /etc/passwd", shell = True, text = True).split("\n"):
    if not re.search(".+:.+:.+", line): continue
    if int(re.split(":", line)[2]) >= 1000 and int(re.split(":", line)[2]) <= 2000:
        users += [re.split(":", line)[0]]
for user in users:
    if input("should " + user + " have access to the computer? [Y/n] ").lower() in ["n", "no"]:
        os.system("userdel -r " + user)
        continue
    if input("should " + user + " have sudo privleges? [Y/n] ").lower() in ["n", "no"]:
        os.system("gpasswd --delete " + user + " adm")
        os.system("gpasswd --delete " + user + " sudo")


# remove hacking tools
def remove_hacking_tools():
    remove_pkg_terms = ["hack", "crack", "password"]
    pkgs_to_remove = []
    for pkg_term in remove_pkg_terms:
        try:
            for pkg in subprocess.check_output("dpkg -l | grep " + pkg_term, shell = True, text = True).split("\n"):
                if pkg == "": continue
                print("keep the following package? [Y/n]")
                print(re.split(r"\s", pkg)[2])
                if input().lower() in ["n", "no"]: pkgs_to_remove += [re.split(r"\s", pkg)[2]]
        except:
            print("no " + pkg_term + "ing tools found")

        pkgs_to_remove = list(set(pkgs_to_remove))
        print("\nremove the following packages: [y/N]")
        print(pkgs_to_remove)
        if input().lower() in ["yes", "y", "ye"]:
            os.system("apt purge -y" + " ".join(pkgs_to_remove))
        else:
            if not input("redo? [y/N]").lower() not in ["yes", "ye", "y"]: return


# check for uncessary files
def remove_unnecessary_files():
    remove_file_extensions = ["mp3", "mp4", "mkv", "mov", "png", "jpg", "jpeg"]
    files_to_remove = []
    for file_ext in remove_file_extensions:
        try:
            for file in subprocess.check_output("find /home -name \"*" + file + "\"", shell = True, text = True).split("\n"):
                if file_ext == "": continue
                print("keep the following file? [Y/n]")
                print(file)
                if input().lower() in ["n", "no"]: files_to_remove += [file]
        except:
            print("no ." + file_ext + " files found")

    files_to_remove = list(set(files_to_remove))
    print("\nremove the following files: [y/N]")
    print(files_to_remove)
    if input().lower() in ["yes", "y", "ye"]:
        os.system("rm" + " ".join(files_to_remove))
    else:
        if not input("redo? [y/N]").lower() not in ["yes", "ye", "y"]: return


# enable ufw / clamav / rkhunter
os.system("ufw enable")
os.system("sudo freshclam")
os.system("sudo clamscan")
os.system("rkhunter --update")
os.system("rkhunter -c > rkhunter.log")
