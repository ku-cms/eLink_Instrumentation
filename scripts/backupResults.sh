#!/usr/bin/env bash
#
# backupResults.sh
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     January 12, 2025
# -------------------------- #

VPN_URL=kuanywhere.ku.edu
SERVER_PATH=smb://resfs.home.ku.edu/GROUPS/PHSX/General/BEAN_GRP
RESULTS_DIR=/Volumes/BEAN_GRP/EyeBERTAutomation/automation_results
BACKUP_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation

# Confirm access to the results stored on the R drive.
if [ ! -d "$RESULTS_DIR" ];
then
    echo "ERROR: Cannot access the results directory on the R drive: ${RESULTS_DIR}"
    echo "Please connect to the R drive using this path: ${SERVER_PATH}"
    echo "You need to be connected to the JAYHAWK network, either from campus or using a VPN client."
    echo "You can get a KU VPN using Cisco Secure Client with this URL: ${VPN_URL}"
    exit 1
fi

# Backup results.
echo "Backing up results..."
echo " - source (R drive): ${RESULTS_DIR}"
echo " - destination (local): ${BACKUP_DIR}"

mkdir -p $BACKUP_DIR
rsync -az $RESULTS_DIR $BACKUP_DIR

echo "Finished backing up results."

