#!/usr/bin/env bash

run=false
[ $run == true ] || exit

# ============================================================================ #
# NONINTERACTIVE COMMANDS ==================================================== #
# ============================================================================ #

# APT COMMANDS =============================================================== #
install_packages=(libpam-cracklib vim sed auditd ufw nmap lsof rkhunter libapache2-mod-security2 chrootkit mysql-client mysql-common php clamav tiger)
purge_packages=(medusa nikto hashcat arp-scan braa dnsrecon dnstracer aircrack-ng john john-data hydra hydra-gtk corkscrew crunch crack crack-common crack-md5 patator polenum cmospwd)

echo "updating and upgrading..."
sudo apt-get update -y && sudo apt-get upgrade -y
echo "finished updating and upgrading"

echo "installing needed packages..."
sudo apt-get --ignore-missing install -y $install_packages
echo "finished updating and upgrading"

echo "purging packages..."
sudo apt-get --ignore-missing purge -y $purge_packages
echo "finished purging packages"

# POLICIES COMMANDS ========================================================== #




# ============================================================================ #
# INTERACTIVE COMMANDS - PROMPT USER ========================================= #
# ============================================================================ #
