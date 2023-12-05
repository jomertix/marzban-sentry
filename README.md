
# Marzban-Sentry

Marzban-Sentry a tool to limit the number of simultaneous connections to an account. 
## Table of contents

 - [Overview](https://github.com/jomertix/marzban-sentry/blob/master/README.md#overview)
 - [Features](https://github.com/jomertix/marzban-sentry/blob/master/README.md#features)
 - [Firewall](https://github.com/jomertix/marzban-sentry/blob/master/README.md#firewall)
 - [Installation](https://github.com/jomertix/marzban-sentry/blob/master/README.md#installation)
 - [Configuration](https://github.com/jomertix/marzban-sentry/blob/master/README.md#configuration)
 - [Run the tool](https://github.com/jomertix/marzban-sentry/blob/master/README.md#run-the-tool)
 - [API](https://github.com/jomertix/marzban-sentry/blob/master/README.md#api)


## Overview

Marzban-Sentry saves all connections to the account, checks if the limit is exceeded on a new connection, and if so, blocks the new connection, leaving the previous ones untouched. You can choose any convenient firewall: Iptables, UFW, Fail2ban (currently only UFW is supported)


## Features

TODO
## Firewall

In order for the IP address to be blocked, you need to set up a firewall.

### UFW

Example of UFW configuration:
```
sudo apt install ufw
sudo ufw default deny incoming 
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

sudo ufw disable && sudo ufw enable
```
## Installation

Install Python and pip:
```bash
sudo apt install python3 python3-pip
```

Marzban-Sentry is written in Python and uses some of its modules. Let's install them:


```bash
pip install websockets python-dotenv schedule

```
Clone the project:
```bash
git clone https://github.com/jomertix/marzban-sentry.git
cd marzban-sentry
```

## Configuration

The entire setup of the program takes place in two files, these are "users.json" and ".env". File "users.json" contains an overridden number of simultaneous connections for the account. Here you can override the default limit for accounts, if you need it. 

```json
{
  "admin": 6,
  "moderator": 4
}
```


The rest of the setup takes place in file ".env". Open it: `nano .env`

```
# Marzban Panel
HOST = localhost
PORT = 443
USE_SSL = false
USERNAME = admin
PASSWORD = admin

ALLOWED_CONNECTIONS = 2
BAN_TIME = 60

# Which firewall should be used: UFW/Iptables/Fail2ban
FIREWALL = UFW


# Advanced configuration

# How often (in seconds) the tool receive logs from the server.
WEBSOCKET_INTERVAL_UPDATE = 1

UNBAN_USERS_INTERVAL = 5
# Scheduler parameters (in seconds) for checking inactive connections.
CHECK_INACTIVE_USERS_INTERVAL = 120
# The tool stores the time of the user's last connection to Marzban.
# If this time (in seconds) has passed since the last connection, the connection is considered inactive.
USER_CONNECTION_LIFETIME = 90

```

## Run the tool

After configuring the project, run it. 

```
python3 main.py
```

TODO: add Screen
## API

TODO
