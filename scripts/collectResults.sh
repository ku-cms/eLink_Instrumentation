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

SOURCE_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation/automation_results
TARGET_DIR=~/CMS/Tracker/e-links/EyeBERTAutomation/results_for_database

echo "Collecting e-link results."

# Copy results.
echo "Copying results..."
python3.10 getElinkResults.py -s $SOURCE_DIR -t $TARGET_DIR

# Create tarball.
echo "Creating tarball..."

echo "Going to target directory:"
echo ${TARGET_DIR}
cd ${TARGET_DIR}

echo "Finding the newest directory in the target directory..."

# Find newest directory:
# See https://stackoverflow.com/questions/9275964/get-the-newest-directory-to-a-variable-in-bash
NEWEST_DIR=$(ls -td ./*/ | head -1)

# Remove "/" from the end:
# See https://unix.stackexchange.com/questions/144298/delete-the-last-character-of-a-string-using-string-manipulation-in-shell-script
NEWEST_DIR=${NEWEST_DIR::-1}

echo "Creating a tarball of this directory: ${NEWEST_DIR}" 
tar -czf ${NEWEST_DIR}.tar.gz ${NEWEST_DIR}
echo "Created ${NEWEST_DIR}.tar.gz"

echo "Finished collecting e-link results!"

