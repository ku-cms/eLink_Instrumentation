#!/usr/bin/env bash
#
# collectResults.sh
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     January 10, 2025
# -------------------------- #

VPN_URL=kuanywhere.ku.edu
SERVER_PATH=smb://resfs.home.ku.edu/GROUPS/PHSX/General/BEAN_GRP
RESULTS_DIR=/Volumes/BEAN_GRP/EyeBERTAutomation/automation_results
BACKUP_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation
TARGET_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation/results_for_database

# Confirm access to the results stored on the R drive.
if [ ! -d "$RESULTS_DIR" ];
then
    echo "ERROR: Cannot access the results directory on the R drive: ${RESULTS_DIR}"
    echo "Please connect to the R drive using this path: ${SERVER_PATH}"
    echo "You need to be connected to the JAYHAWK network, either from campus or using a VPN client."
    echo "You can get a KU VPN using Cisco Secure Client with this URL: ${VPN_URL}"
    exit 1
fi

echo "Collecting e-link results."

# Backup results.
echo "Backing up results..."
echo " - source (R drive): ${RESULTS_DIR}"
echo " - destination (local): ${BACKUP_DIR}"
mkdir -p $BACKUP_DIR
#rsync -az $RESULTS_DIR $BACKUP_DIR

# Copy results.
echo "Copying results..."
python3.10 getElinkResults.py -s $RESULTS_DIR -t $TARGET_DIR

# Create tarball.
echo "Creating tarball..."

# Find newest directory:
NEWEST_DIR=$(ls -t ${TARGET_DIR} | tail -n 1)

echo "Newest directory: ${NEWEST_DIR}"

tar -czf ${TARGET_DIR}/${NEWEST_DIR}.tar.gz ${TARGET_DIR}/${NEWEST_DIR}

echo "Created ${TARGET_DIR}/${NEWEST_DIR}.tar.gz"

echo "Done!"

