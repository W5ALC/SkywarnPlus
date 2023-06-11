# SkywarnPlus

SkywarnPlus is an optimized, powerful weather alert system designed for Asterisk/app_rpt repeater controller systems. Developed in Python, a high-level and fast programming language, SkywarnPlus leverages the capabilities of the new and improved [NWS CAP v1.2 JSON API](https://www.weather.gov/documentation/services-web-api). 

The system is resource-efficient, meaning it doesn't consume unnecessary internet bandwidth or cause excess wear on your physical storage. This is especially beneficial for Raspberry Pi users, as it helps to extend the lifespan of your SD card by limiting unnecessary I/O operations. 

SkywarnPlus is designed to deliver timely and accurate weather alerts while providing extensive customization options to suit your specific needs.

## Features

* **Natural Human Speech**: SkywarnPlus features a library of real female human speech recordings, providing a more pleasant and natural experience compared to synthesized speech. This leads to clearer, more understandable alerts that enhance user experience.
* **Optimized Performance**: SkywarnPlus is written in Python, resulting in superior performance compared to scripts written in bash. The optimized design ensures minimal impact on internet bandwidth and physical storage.
* **Comprehensive alert coverage**: You can specify as many counties or zones as you want to check for alerts, enabling broad coverage and ensuring you're always informed about the latest weather conditions.
* **Advanced filtering**: Block or filter any alerts you don't want. SkywarnPlus supports regular expressions and wildcards, giving you comprehensive control over the alerts you receive.
* **Automatic courtesy tone changes**: SkywarnPlus can automatically change the repeater courtesy tones when specified alerts exist, adding a layer of customization and relevance to your alert system.
* **Duplicate alert removal**: SkywarnPlus automatically removes any duplicate alerts, ensuring you only receive unique and relevant alerts.
* **Selectable alert broadcasting**: You can choose to broadcast alerts when weather conditions change or when they dissipate, providing timely updates on weather conditions.
* **Automated Tailmessage management**: Tailmessage management provides selectable unobtrusive alerting even if alert broadcasting is disabled.
* **Pushover integration**: Get alerts and debug messages directly sent to your phone, ensuring you're always connected and updated.
* **Supports multiple local nodes**: SkywarnPlus allows you to specify as many local node numbers as you want for alerting, providing flexibility in how your alerts are distributed.

## How It Works

SkywarnPlus is a sophisticated weather alert system for Asterisk/app_rpt repeater controller systems. It leverages the capabilities of the National Weather Service's (NWS) CAP v1.2 JSON API. Here's a detailed breakdown of how SkywarnPlus functions:

1. **Data Fetching**: SkywarnPlus queries the NWS CAP v1.2 API at regular intervals. This API provides a JSON response containing comprehensive details about the latest weather conditions and alerts.

2. **Data Parsing and Filtering**: Upon receiving the API response, SkywarnPlus parses the JSON data to extract relevant information. It then filters this information based on user-defined criteria set in the configuration file, such as specific counties or zones of interest. Users can also choose to filter out certain types of alerts using regular expressions and wildcards.

3. **Alert Management**: SkywarnPlus intelligently manages alerts, eliminating duplicates to ensure that you only receive unique and relevant weather warnings. 

4. **Alert Broadcasting**: Based on your settings, SkywarnPlus will then broadcast the alerts. You can customize this process to broadcast alerts when weather conditions change or when they dissipate.

5. **Tailmessage and Courtesy Tones**: SkywarnPlus can automatically update tailmessages and change the repeater courtesy tones when specific alerts are active. This process is also customizable based on user preferences.

6. **Pushover Integration**: SkywarnPlus is integrated with Pushover, which means it can send alerts and debug messages directly to your phone, keeping you constantly updated.

7. **Real Human Speech**: Unlike many other weather alert systems, SkywarnPlus uses a library of real female human speech recordings. This makes the alerts more understandable and pleasant to listen to, compared to synthetic speech.

8. **Maintenance**: Lastly, SkywarnPlus is designed with efficiency in mind. It minimizes its impact on internet bandwidth and physical storage, making it a great choice for systems like Raspberry Pi.

SkywarnPlus's design strikes a balance between functionality and resource efficiency. While it provides a comprehensive range of features, it is also careful to respect your system's resources, ensuring a smooth and responsive experience for users.

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

Refer to the [config.ini](config.ini) file and update the parameters according to your setup and preferences.

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
