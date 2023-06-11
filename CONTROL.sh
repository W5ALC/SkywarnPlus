#!/bin/bash

# CONTROL.sh
# A Control Script for SkywarnPlus
# 
# This script allows you to change the value of specific keys in the SkywarnPlus config.ini file.
# It's designed to enable or disable certain features of SkywarnPlus from the command line.
# It is case-insensitive, accepting both upper and lower case parameters.
#
# Usage: ./CONTROL.sh <key> <value>
# Example: ./CONTROL.sh sayalert false
# This will set 'SayAlert' to 'False' in the config.ini file.
# 
# Supported keys:
# - enable: Enable or disable SkywarnPlus entirely. (Section: SKYWARNPLUS)
# - sayalert: Enable or disable instant alerting when weather alerts change. (Section: Alerting)
# - sayallclear: Enable or disable instant alerting when weather alerts are cleared. (Section: Alerting)
# - tailmessage: Enable or disable building of tail message. (Section: Tailmessage)
# - courtesytone: Enable or disable automatic courtesy tones. (Section: CourtesyTones)
# 
# All changes will be made in the config.ini file located in the same directory as the script.

# First, we need to check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Incorrect number of arguments. Please provide the key and the new value."
    echo "Usage: $0 <key> <value>"
    exit 1
fi

# Get the directory of the script
SCRIPT_DIR=$(dirname $(readlink -f $0))

# Convert the input key and value into lowercase
KEY=$(echo "$1" | tr '[:upper:]' '[:lower:]')
VALUE=$(echo "$2" | tr '[:upper:]' '[:lower:]')

# Define the sections and the keys they contain
declare -A SECTIONS=( ["skywarnplus"]="enable" ["alerting"]="sayalert sayallclear" ["tailmessage"]="enable" ["courtesytones"]="enable")

# Iterate over the sections and their keys
for SECTION in "${!SECTIONS[@]}"; do
    KEYS="${SECTIONS[$SECTION]}"
    for ITEM in $KEYS; do
        # If the item matches the provided key, update the value
        if [ "$ITEM" = "$KEY" ]; then
            # Convert the section and item back to proper case before modifying the file
            SECTION=$(echo "$SECTION" | tr '[:lower:]' '[:upper:]')
            ITEM=$(echo "$ITEM" | tr '[:lower:]' '[:upper:]')
            sed -i "/\[$SECTION\]/,/^\[/s/^$ITEM = .*\$/$ITEM = $VALUE/g" $SCRIPT_DIR/config.ini
            echo "$ITEM set to $VALUE in the [$SECTION] section."
            exit 0
        fi
    done
done

echo "The provided key does not match any configurable item."
