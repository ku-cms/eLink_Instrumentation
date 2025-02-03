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

# Results paths (remote)
RESULTS_DIR=/Volumes/BEAN_GRP/EyeBERTAutomation
RESULTS_PLOTS_DIR=$RESULTS_DIR/automation_results

# Backup paths (local)
BACKUP_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation
BACKUP_DATA_DIR=$BACKUP_DIR/automation_data

# Network paths
SERVER_PATH=smb://resfs.home.ku.edu/GROUPS/PHSX/General/BEAN_GRP
VPN_URL=kuanywhere.ku.edu

# Confirm access to the results stored on the R drive.
if [ ! -d "$RESULTS_DIR" ];
then
    echo "ERROR: Cannot access the results directory on the R drive: ${RESULTS_DIR}"
    echo "Please connect to the R drive using this path: ${SERVER_PATH}"
    echo "You need to be connected to the JAYHAWK network, either from campus or using a VPN client."
    echo "You can get a KU VPN using Cisco Secure Client with this URL: ${VPN_URL}"
    exit 1
fi

# Create backup directories
mkdir -p $BACKUP_DIR
mkdir -p $BACKUP_DATA_DIR

# Backup data
echo "Backing up data..."
echo " - source (R drive): ${RESULTS_DIR}/*.xlsx"
echo " - destination (local): ${BACKUP_DATA_DIR}"

rsync -az $RESULTS_DIR/*.xlsx $BACKUP_DATA_DIR

# Backup plots
echo "Backing up plots..."
echo " - source (R drive): ${RESULTS_PLOTS_DIR}"
echo " - destination (local): ${BACKUP_DIR}"

rsync -az $RESULTS_PLOTS_DIR $BACKUP_DIR

echo "Finished backing up results!"

