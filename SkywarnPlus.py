#!/usr/bin/env python3

"""
SkywarnPlus by Mason Nelson (N5LSN/WRKF394)
==================================================
SkywarnPlus is a utility that retrieves severe weather alerts from the National 
Weather Service and integrates these alerts with an Asterisk/app_rpt based 
radio repeater controller. 

This utility is designed to be highly configurable, allowing users to specify 
particular counties for which to check for alerts, the types of alerts to include 
or block, and how these alerts are integrated into their radio repeater system. 

This includes features such as automatic voice alerts and a tail message feature 
for constant updates. All alerts are sorted by severity and cover a broad range 
of weather conditions such as hurricane warnings, thunderstorms, heat waves, etc. 

Configurable through a .ini file, SkywarnPlus serves as a comprehensive and 
flexible tool for those who need to stay informed about weather conditions 
and disseminate this information through their radio repeater system.
"""

import os
import json
import logging
import requests
import configparser
import shutil
import fnmatch
import subprocess
import time
from datetime import datetime, timezone
from dateutil import parser
from pydub import AudioSegment

# Configuration file handling
baseDir = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(baseDir, "config.ini")
config = configparser.ConfigParser()
config.readfp(open(configPath, "r"))

# Fetch values from configuration file
tmp_dir = config["DEV"].get("TmpDir", fallback="/tmp/SkywarnPlus")
sounds_path = config["Alerting"].get("SoundsPath")
if sounds_path == "./SOUNDS":
    sounds_path = os.path.join(baseDir, "SOUNDS")
countyCodes = config["Alerting"]["CountyCodes"].split(",")

# If temporary directory doesn't exist, create it
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# List of blocked events
blocked_events = config["Blocking"].get("BlockedEvents").split(",")
# Configuration for tailmessage
tailmessage_config = config["Tailmessage"]
# Flag to enable/disable tailmessage
enable_tailmessage = tailmessage_config.getboolean("Enable", fallback=False)
# Path to tailmessage file
tailmessage_file = tailmessage_config.get("TailmessagePath", fallback="./wx-tail.wav")

# Warning and announcement strings
WS = [
    "Hurricane Force Wind Warning",
    "Severe Thunderstorm Warning",
    "Severe Thunderstorm Watch",
    "Winter Weather Advisory",
    "Tropical Storm Warning",
    "Special Marine Warning",
    "Freezing Rain Advisory",
    "Special Weather Statement",
    "Excessive Heat Warning",
    "Coastal Flood Advisory",
    "Coastal Flood Warning",
    "Winter Storm Warning",
    "Tropical Storm Watch",
    "Thunderstorm Warning",
    "Small Craft Advisory",
    "Extreme Wind Warning",
    "Excessive Heat Watch",
    "Wind Chill Advisory",
    "Storm Surge Warning",
    "River Flood Warning",
    "Flash Flood Warning",
    "Coastal Flood Watch",
    "Winter Storm Watch",
    "Wind Chill Warning",
    "Thunderstorm Watch",
    "Fire Weather Watch",
    "Dense Fog Advisory",
    "Storm Surge Watch",
    "River Flood Watch",
    "Ice Storm Warning",
    "Hurricane Warning",
    "High Wind Warning",
    "Flash Flood Watch",
    "Red Flag Warning",
    "Blizzard Warning",
    "Tornado Warning",
    "Hurricane Watch",
    "High Wind Watch",
    "Frost Advisory",
    "Freeze Warning",
    "Wind Advisory",
    "Tornado Watch",
    "Storm Warning",
    "Heat Advisory",
    "Flood Warning",
    "Gale Warning",
    "Freeze Watch",
    "Flood Watch",
    "Flood Advisory",
    "Hurricane Local Statement",
    "Beach Hazards Statement",
    "Air Quality Alert",
]
WA = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
]

# Cleanup flag for testing
CLEANSLATE = config["DEV"].get("CLEANSLATE")
if CLEANSLATE == "True":
    shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

# Configure logging
log_config = config["Logging"]
enable_debug = log_config.getboolean("Debug", fallback=False)
log_file = log_config.get("LogPath", fallback="{}/SkywarnPlus.log".format(tmp_dir))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if enable_debug else logging.INFO)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_file)
c_format = f_format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.debug("Tailmessage file: {}".format(tailmessage_file))
logger.debug("Sounds path: {}".format(sounds_path))
logger.debug("Blocked events: {}".format(blocked_events))


def getAlerts(countyCodes):
    """
    Retrieve severe weather alerts for specified county codes.

    Args:
        countyCodes (list): List of county codes.

    Returns:
        alerts (list): List of active weather alerts.
    """
    alerts = set()  # Change list to set to automatically avoid duplicate alerts
    current_time = datetime.now(timezone.utc)
    logger.debug("Checking for alerts in {}".format(countyCodes))
    for countyCode in countyCodes:
        logger.debug("Checking for alerts in {}".format(countyCode))
        url = "https://api.weather.gov/alerts/active?zone={}".format(countyCode)
        logger.debug("Requesting {}".format(url))
        response = requests.get(url)
        logger.debug("Response: {}\n\n".format(response.text))

        if response.status_code == 200:
            alert_data = response.json()
            for feature in alert_data["features"]:
                expires = feature["properties"].get("expires")
                if expires:
                    expires_time = parser.isoparse(expires)
                    if expires_time > current_time:
                        event = feature["properties"]["event"]
                        for blocked_event in blocked_events:
                            if fnmatch.fnmatch(event, blocked_event):
                                logger.debug(
                                    "Blocking {} as per configuration".format(event)
                                )
                                break
                        else:
                            alerts.add(event)  # Add event to set
                            logger.debug("{}: {}".format(countyCode, event))
        else:
            logger.error(
                "Failed to retrieve alerts for {}, HTTP status code {}, response: {}".format(
                    countyCode, response.status_code, response.text
                )
            )

    alerts = list(alerts)  # Convert set back to list
    alerts.sort(key=lambda x: WS.index(x) if x in WS else len(WS))
    return alerts


def sayAlert(alerts):
    """
    Generate and broadcast severe weather alert sounds on Asterisk.

    Args:
        alerts (list): List of active weather alerts.
    """
    alert_file = "{}/alert.wav".format(sounds_path)
    combined_sound = AudioSegment.from_wav(
        os.path.join(sounds_path, "ALERTS", "asn97.wav")
    )
    sound_effect = AudioSegment.from_wav(
        os.path.join(sounds_path, "ALERTS", "asn95.wav")
    )

    for alert in alerts:
        try:
            index = WS.index(alert)
            audio_file = AudioSegment.from_wav(
                os.path.join(sounds_path, "ALERTS", "asn{}.wav".format(WA[index]))
            )
            combined_sound += sound_effect + audio_file
            logger.debug("Added {} (asn{}.wav) to alert sound".format(alert, WA[index]))
        except ValueError:
            logger.error("Alert not found: {}".format(alert))
        except FileNotFoundError:
            logger.error(
                "Audio file not found: {}/ALERTS/asn{}.wav".format(
                    sounds_path, WA[index]
                )
            )

    logger.debug("Exporting alert sound to {}".format(alert_file))
    converted_combined_sound = convert_audio(combined_sound)
    converted_combined_sound.export(alert_file, format="wav")

    logger.debug("Replacing tailmessage with silence")
    silence = AudioSegment.silent(duration=100)
    converted_silence = convert_audio(silence)
    converted_silence.export(tailmessage_file, format="wav")
    node_numbers = config["Asterisk"]["Nodes"].split(",")

    for node_number in node_numbers:
        logger.info("Broadcasting alert on node {}".format(node_number))
        command = f'/usr/sbin/asterisk -rx "rpt localplay {node_number.strip()} {os.path.splitext(os.path.abspath(alert_file))[0]}"'
        subprocess.run(command, shell=True)

    logger.info("Waiting 30 seconds for Asterisk to make announcement...")
    time.sleep(30)


def sayAllClear():
    """
    Generate and broadcast 'all clear' message on Asterisk.
    """
    alert_clear = os.path.join(sounds_path, "ALERTS", "asn96.wav")
    node_numbers = config["Asterisk"]["Nodes"].split(",")

    for node_number in node_numbers:
        logger.info("Broadcasting all clear message on node {}".format(node_number))
        command = f'/usr/sbin/asterisk -rx "rpt localplay {node_number.strip()} {os.path.splitext(os.path.abspath(alert_clear))[0]}"'
        subprocess.run(command, shell=True)


def buildTailmessage(alerts):
    """
    Build a tailmessage, which is a short message appended to the end of a
    transmission to update on the weather conditions.

    Args:
        alerts (list): List of active weather alerts.
    """
    if not alerts:
        logger.debug("No alerts, creating silent tailmessage")
        silence = AudioSegment.silent(duration=100)
        converted_silence = convert_audio(silence)
        converted_silence.export(tailmessage_file, format="wav")
        return
    combined_sound = AudioSegment.empty()
    sound_effect = AudioSegment.from_wav(
        os.path.join(sounds_path, "ALERTS", "asn95.wav")
    )
    for alert in alerts:
        try:
            index = WS.index(alert)
            audio_file = AudioSegment.from_wav(
                os.path.join(sounds_path, "ALERTS", "asn{}.wav".format(WA[index]))
            )
            combined_sound += sound_effect + audio_file
            logger.debug("Added {} (asn{}.wav) to tailmessage".format(alert, WA[index]))
        except ValueError:
            logger.error("Alert not found: {}".format(alert))
        except FileNotFoundError:
            logger.error(
                "Audio file not found: {}/ALERTS/asn{}.wav".format(
                    sounds_path, WA[index]
                )
            )
    logger.debug("Exporting tailmessage to {}".format(tailmessage_file))
    converted_combined_sound = convert_audio(combined_sound)
    converted_combined_sound.export(tailmessage_file, format="wav")


def changeCT(ct):
    """
    Change the current Courtesy Tone (CT) to the one specified.
    The function first checks if the specified CT is already in use, and if it is, it returns without making any changes.
    If the CT needs to be changed, it replaces the current CT files with the new ones and updates the state file.
    If no CT is specified, the function logs an error message and returns.

    Args:
        ct (str): The name of the new CT to use. This should be one of the CTs specified in the config file.

    Returns:
        bool: True if the CT was changed, False otherwise.
    """
    tone_dir = config["CourtesyTones"].get("ToneDir")
    local_ct = config["CourtesyTones"].get("LocalCT")
    link_ct = config["CourtesyTones"].get("LinkCT")
    wx_ct = config["CourtesyTones"].get("WXCT")
    rpt_local_ct = config["CourtesyTones"].get("RptLocalCT")
    rpt_link_ct = config["CourtesyTones"].get("RptLinkCT")
    ct_state_file = os.path.join(tmp_dir, "ct_state.txt")

    if not ct:
        logger.error("ChangeCT called with no CT specified")
        return

    current_ct = None
    if os.path.exists(ct_state_file):
        with open(ct_state_file, "r") as file:
            current_ct = file.read().strip()

    if ct == current_ct:
        logger.debug("Courtesy tones are already {}, no changes made.".format(ct))
        return False

    if ct == "NORMAL":
        logger.info("Changing to NORMAL courtesy tones")
        shutil.copyfile(tone_dir + "/" + local_ct, tone_dir + "/" + rpt_local_ct)
        shutil.copyfile(tone_dir + "/" + link_ct, tone_dir + "/" + rpt_link_ct)
    else:
        logger.info("Changing to {} courtesy tone".format(ct))
        shutil.copyfile(tone_dir + "/" + wx_ct, tone_dir + "/" + rpt_local_ct)
        shutil.copyfile(tone_dir + "/" + wx_ct, tone_dir + "/" + rpt_link_ct)

    with open(ct_state_file, "w") as file:
        file.write(ct)
    return True


def send_pushover_notification(message, title=None, priority=0):
    """
    Send a push notification via Pushover service.
    The function constructs the payload for the request, including the user key, API token, message, title, and priority.
    The payload is then sent to the Pushover API endpoint. If the request fails, an error message is logged.

    Args:
        message (str): The content of the push notification.
        title (str, optional): The title of the push notification. Defaults to None.
        priority (int, optional): The priority of the push notification. Defaults to 0.

    Returns:
        None
    """
    pushover_config = config["Pushover"]
    user_key = pushover_config.get("UserKey")
    token = pushover_config.get("APIToken")

    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": token,
        "user": user_key,
        "message": message,
        "title": title,
        "priority": priority,
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        logger.error("Failed to send Pushover notification: {}".format(response.text))


def convert_audio(audio):
    """
    Convert audio file to 8000Hz mono for compatibility with Asterisk.

    Args:
        audio (AudioSegment): Audio file to be converted.

    Returns:
        AudioSegment: Converted audio file.
    """
    return audio.set_frame_rate(8000).set_channels(1)


def main():
    """
    Main function of the script, that fetches and processes severe weather
    alerts, then integrates these alerts into an Asterisk/app_rpt based radio
    repeater system.
    """
    say_alert_enabled = config["Alerting"].getboolean("SayAlert", fallback=False)
    say_all_clear_enabled = config["Alerting"].getboolean("SayAllClear", fallback=False)
    alerts = getAlerts(countyCodes)
    tmp_file = "{}/alerts.json".format(tmp_dir)

    if os.path.exists(tmp_file):
        with open(tmp_file, "r") as file:
            old_alerts = json.load(file)
    else:
        old_alerts = ["init"]
        logger.info("No previous alerts file found, starting fresh.")

    if old_alerts != alerts:
        with open(tmp_file, "w") as file:
            json.dump(alerts, file)

        ct_alerts = config["CourtesyTones"].get("CTAlerts").split(",")
        enable_ct_auto_change = config["CourtesyTones"].getboolean(
            "Enable", fallback=False
        )

        pushover_enabled = config["Pushover"].getboolean("Enable", fallback=False)
        pushover_debug = config["Pushover"].getboolean("Debug", fallback=False)
        pushover_message = "Alerts changed: {}\n".format(alerts)

        if enable_ct_auto_change:
            for alert in alerts:
                if alert in ct_alerts:
                    if changeCT("WX"):  # If the CT was actually changed
                        if pushover_debug:
                            pushover_message += "Changed courtesy tones to WX\n"
                    break
        else:
            if changeCT("NORMAL"):  # If the CT was actually changed
                if pushover_debug:
                    pushover_message += "Changed courtesy tones to NORMAL\n"

        logger.debug("Alerts: {}".format(alerts))
        if len(alerts) == 0:
            logger.info("No alerts found")
            if not os.path.exists(tmp_file):
                with open(tmp_file, "w") as file:
                    json.dump([], file)
            if say_all_clear_enabled:
                sayAllClear()
        else:
            if say_alert_enabled:
                sayAlert(alerts)

        if enable_tailmessage:
            buildTailmessage(alerts)
            if not alerts:
                pushover_message += "Tailmessage replaced with silence\n"
            else:
                pushover_message += "Built tailmessage with alerts: {}\n".format(alerts)

        if pushover_enabled:
            if enable_debug:
                logger.info(
                    "Sending pushover notification: {}".format(pushover_message)
                )
            send_pushover_notification(pushover_message, title="Alerts Changed")
    else:
        logger.debug("No change in alerts")


if __name__ == "__main__":
    main()
