from os import environ as env
from dotenv import load_dotenv

load_dotenv(override=True)

HOST = env.get('HOST')
PORT = env.get('PORT')
USE_SSL = env.get('USE_SSL') == 'true'

USERNAME = env.get('USERNAME')
PASSWORD = env.get('PASSWORD')

ALLOWED_CONNECTIONS = int(env.get('ALLOWED_CONNECTIONS'))
BAN_TIME = int(env.get('BAN_TIME'))

WEBSOCKET_INTERVAL_UPDATE = env.get('WEBSOCKET_INTERVAL_UPDATE')
UNBAN_USERS_INTERVAL = int(env.get('UNBAN_USERS_INTERVAL'))
CHECK_INACTIVE_USERS_INTERVAL = int(env.get('CHECK_INACTIVE_USERS_INTERVAL'))
USER_CONNECTION_LIFETIME = int(env.get('USER_CONNECTION_LIFETIME'))

FIREWALL = env.get('FIREWALL')