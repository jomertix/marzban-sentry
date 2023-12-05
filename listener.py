import asyncio
import re

import requests
import websockets

import config

import guardian
from logger import logger


def token():
    try:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'password': f'{config.PASSWORD}',
            'username': f'{config.USERNAME}'
        }
        url = f'{http_url}/api/admin/token'
        response = requests.post(url, headers=headers, data=data)

        response.raise_for_status()
        json = response.json()
        access_token = json['access_token']
        return access_token
    except Exception as ex:
        logger.error(f"Unable to connect to Marzban: {ex}")
    return None


# TODO: add nodes, add autoreconnect
async def ws_client():
    access_token = token()

    if access_token is None:
        return

    logs_url = f"{ws_url}/api/core/logs?token={access_token}&interval={config.WEBSOCKET_INTERVAL_UPDATE}"

    logger.info(f'Connecting to {config.HOST}:{config.PORT}')
    try:
        async with websockets.connect(logs_url) as ws:
            logger.info(f'Successfully connected to {config.HOST}:{config.PORT}')
            while True:
                try:
                    log = await ws.recv()
                    handleLog(log)
                    print(log)
                except Exception as ex:
                    logger.error(f'Failed to handle server\'s response: {ex}')
    except Exception as ex:
        logger.error(f'Failed to initialize WebSocket connection: {ex}')


def handleLog(log):
    # or use log.splitlines() instead
    logs = list(re.split(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} ', log))
    logs = list(filter(lambda line: 'accepted' in line, logs))

    if len(logs) == 0:
        return

    logs = list(map(str.rstrip, logs))

    connections = list(map(extractConnection, logs))
    connections = list(filter(isConnectionValid, connections))

    for connection in connections:
        if guardian.canProceed(connection):
            guardian.record(connection)
        else:
            guardian.ban(connection)


def isConnectionValid(connection):
    # TODO: add additional checks to be sure that extracted connection is valid
    if connection.email is None or connection.ip is None:
        return False

    return True


class Connection:

    def __init__(self, email, ip):
        self.email = email
        self.ip = ip


def extractConnection(line):
    ip = extractIP(line)
    email = extractEmail(line)

    return Connection(email, ip)


def extractIP(line):
    blocks = line.split(' ')
    ip = blocks[0].split(':')[0]
    # check line != ip
    return ip


def extractEmail(line):
    blocks = line.split(':')
    email = blocks[-1]
    data = email.split('.')
    if len(data) > 1:
        # check email != line
        return data[1]
    return None


def start():
    asyncio.run(ws_client())


http_protocol = 'https' if config.USE_SSL else 'http'
http_url = f'{http_protocol}://{config.HOST}:{config.PORT}'

ws_protocol = 'wss' if config.USE_SSL else 'ws'
ws_url = f'{ws_protocol}://{config.HOST}:{config.PORT}'

