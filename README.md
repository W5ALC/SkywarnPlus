# SkywarnPlus

SkywarnPlus is an optimized, powerful weather alert system designed for Asterisk/app_rpt repeater controller systems such as [AllStarLink](https://allstarlink.org/) and [HAMVOIP](https://hamvoip.org/). It's written in Python and utilizes the new [NWS CAP v1.2 JSON API](https://www.weather.gov/documentation/services-web-api). SkywarnPlus is optimized to be resource-efficient and offers customization options to suit various user needs.

## Features

* **Human Speech Alerts**: Provides a library of recorded human speech for clearer, more understandable alerts.
* **Performance**: Designed for minimal impact on internet bandwidth and storage, reducing unnecessary I/O operations.
* **Alert Coverage**: Allows specifying multiple counties or zones for alerts, ensuring broad coverage.
* **Alert Filtering**: Provides advanced options to block or filter alerts using regular expressions and wildcards.
* **Courtesy Tone Changes**: Changes repeater courtesy tones based on active alerts.
* **Duplicate Alert Removal**: Ensures you receive unique and relevant alerts by automatically removing duplicates.
* **Selective Broadcasting**: Broadcasts alerts on weather conditions' onset or dissipation.
* **Tailmessage Management**: Provides unobtrusive alerting if alert broadcasting is disabled.
* **Pushover Integration**: Sends alerts and debug messages directly to your phone.
* **Multiple Local Nodes**: Supports alert distribution to as many local node numbers as desired.

## How It Works

SkywarnPlus is a Python-based weather alert system for Asterisk/app_rpt repeater controller systems, leveraging the National Weather Service's (NWS) CAP v1.2 JSON API. The system follows several key steps to deliver timely and accurate weather alerts:

1. **Data Fetching**: The system performs regular API calls to the NWS CAP v1.2 API, which provides comprehensive, real-time data on the latest weather conditions and alerts. The frequency of these calls can be adjusted according to user needs.

2. **Data Parsing**: Upon receiving the API response, SkywarnPlus parses the JSON data to extract the information pertinent to weather alerts. This involves reading the structured JSON data and converting it into an internal format for further processing.

3. **Data Filtering**: The extracted data is then filtered based on user-defined criteria set in the configuration file. This includes narrowing down the information to specific counties or zones of interest, as well as excluding certain types of alerts. The filtering mechanism supports regular expressions and wildcards for more sophisticated filtering rules.

4. **Alert Management**: SkywarnPlus manages the filtered alerts intelligently, ensuring that each alert is unique and relevant. Duplicate alerts are automatically removed from the pool of active alerts to prevent repetition and alert fatigue.

5. **Alert Broadcasting**: The system then broadcasts the alerts according to user-defined settings. You can customize these settings to broadcast alerts when new weather conditions are detected or when existing conditions dissipate. This ensures timely communication of weather changes.

6. **Tailmessage and Courtesy Tones**: In addition to broadcasting alerts, SkywarnPlus also automatically updates tailmessages and changes the repeater courtesy tones when specific alerts are active. These changes add a level of customization and context-awareness to the alert system and can be tailored to individual preferences.

7. **Pushover Integration**: SkywarnPlus integrates with Pushover, a mobile notification service, to send alerts and debug messages directly to your phone. This provides a direct and immediate communication channel, keeping you constantly updated on the latest weather conditions.

8. **Real Human Speech**: To enhance clarity and improve user experience, SkywarnPlus uses a library of real female human speech recordings for alerts. This creates a more natural listening experience compared to synthetic speech and aids in clear communication of alert messages.

9. **Maintenance and Resource Management**: Designed with efficiency in mind, SkywarnPlus minimizes its impact on internet bandwidth and physical storage. The system conducts its operations mindful of resource usage, making it particularly suitable for devices with limited resources, such as Raspberry Pi.

This combination of steps ensures SkywarnPlus provides reliable, timely, and accurate weather alerts, while respecting your system's resources and providing extensive customization options.

## Installation

SkywarnPlus is recommended to be installed at the `/usr/local/bin/SkywarnPlus` location on a Debian machine.

Follow the steps below to install:

1. **Dependencies**

Install the required dependencies using the following commands:

**Debian**
```bash
apt install python3-pip ffmpeg
pip3 install requests python-dateutil pydub
```
**Arch**
```bash
sudo pacman -S python python-pip ffmpeg
pip install requests python-dateutil pydub
```

2. **Clone the Repository**

Clone the SkywarnPlus repository from GitHub to the `/usr/local/bin` directory:

```bash
cd /usr/local/bin
git clone https://github.com/mason10198/SkywarnPlus.git
```
3. **Edit Configuration**

Edit the configuration file to suit your system
```bash
sudo nano SkywarnPlus/config.ini
```

4. **Crontab Entry**

Add a crontab entry to call SkywarnPlus on an interval. Open your crontab file using the `crontab -e` command, and add the following line:

```bash
* * * * * /usr/bin/python3 /usr/local/bin/SkywarnPlus/SkywarnPlus.py
```

This command will execute SkywarnPlus every minute.

## Configuration

Update parameters in the [config.ini](config.ini) file according to your preferences.

## Tailmessage and Courtesy Tones

SkywarnPlus offers functionalities such as Tailmessage management and Automatic Courtesy Tones, which require specific configurations in the `rpt.conf` file.

### Tailmessage

Tailmessage functionality requires the `rpt.conf` to be properly set up. Here's an example:

```bash
tailmessagetime = 600000
tailsquashedtime = 30000
tailmessagelist = /usr/local/bin/SkywarnPlus/SOUNDS/WX-TAIL
```

### Automatic Courtesy Tones

SkywarnPlus can automatically change the repeater courtesy tone whenever certain weather alerts are active. The configuration for this is based on your `rpt.conf` file setup. Here's an example:

```bash
[NODENUMBER]
unlinkedct = ct1
remotect = ct1
linkunkeyct = ct2
[telemetry]
ct1 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/CT-LOCAL
ct2 = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/CT-LINK
remotetx = /usr/local/bin/SkywarnPlus/SOUNDS/TONES/CT-LOCAL
```

## Contributing

SkywarnPlus is open-source and welcomes contributions. If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Maintenance and Bug Reporting

SkywarnPlus is actively maintained by a single individual who dedicates their spare time to improve and manage this project. Despite best efforts, the application may have some bugs or areas for improvement.

If you encounter any issues with SkywarnPlus, please check back to the [SkywarnPlus GitHub Repository](https://github.com/mason10198/SkywarnPlus) to see if there have been any updates or fixes since the last time you downloaded it. New commits are made regularly to enhance the system's performance and rectify any known issues.

Bug reporting is greatly appreciated as it helps to improve SkywarnPlus. If you spot a bug, please raise an issue in the GitHub repository detailing the problem. Include as much information as possible, such as error messages, screenshots, and steps to reproduce the issue. This will assist in quickly understanding and resolving the issue. 

Thank you for your understanding and assistance in making SkywarnPlus a more robust and reliable system for all.

## License

SkywarnPlus is open-sourced software licensed under the [MIT license](LICENSE).
