# SkywarnPlus

SkywarnPlus is an optimized, powerful weather alert system designed for Asterisk/app_rpt repeater controller systems. Developed in Python, a high-level and fast programming language, SkywarnPlus leverages the capabilities of the new and improved NWS CAP v1.2 JSON API. 

The system is resource-efficient, meaning it doesn't consume unnecessary internet bandwidth or cause excess wear on your physical storage. This is especially beneficial for Raspberry Pi users, as it helps to extend the lifespan of your SD card by limiting unnecessary I/O operations. 

SkywarnPlus is designed to deliver timely and accurate weather alerts while providing extensive customization options to suit your specific needs.

## Features

* **Optimized Performance**: SkywarnPlus is written in Python, resulting in superior performance compared to scripts written in bash. The optimized design ensures minimal impact on internet bandwidth and physical storage.
* **Comprehensive alert coverage**: You can specify as many counties or zones as you want to check for alerts, enabling broad coverage and ensuring you're always informed about the latest weather conditions.
* **Advanced filtering**: Block or filter any alerts you don't want. SkywarnPlus supports regular expressions and wildcards, giving you comprehensive control over the alerts you receive.
* **Automatic courtesy tone changes**: SkywarnPlus can automatically change the repeater courtesy tones when specified alerts exist, adding a layer of customization and relevance to your alert system.
* **Duplicate alert removal**: SkywarnPlus automatically removes any duplicate alerts, ensuring you only receive unique and relevant alerts.
* **Selectable alert broadcasting**: You can choose to broadcast alerts when weather conditions change or when they dissipate, providing timely updates on weather conditions.
* **Automated Tailmessage management**: Tailmessage management is selectable and automated, providing more detailed information about the alert.
* **Pushover integration**: Get alerts and debug messages directly sent to your phone, ensuring you're always connected and updated.
* **Supports multiple local nodes**: SkywarnPlus allows you to specify as many local node numbers as you want for alerting, providing flexibility in how your alerts are distributed.

## Installation

SkywarnPlus is recommended to be installed at the `/usr/local/bin/SkywarnPlus` location on a Debian machine.

Follow the steps below to install:

1. **Dependencies**

Install the required dependencies using the following commands:

```bash
apt install python3-pip ffmpeg
pip3 install requests python-dateutil pydub
```

2. **Clone the Repository**

Clone the SkywarnPlus repository from GitHub to the `/usr/local/bin` directory:

```bash
cd /usr/local/bin
git clone https://github.com/user/SkywarnPlus.git
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

## License

SkywarnPlus is open-sourced software licensed under the [MIT license](LICENSE).
