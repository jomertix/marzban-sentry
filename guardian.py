import time
import calendar
import config
import storage

from firewall import UFW
from logger import logger


def ban(connection):
    if not storage.isBanned(connection.ip):
        firewall.ban(connection.ip)
        storage.ban(connection)
        logger.info(f'{connection.ip} has been banned ({connection.email})')


def unban(ip):
    if storage.isBanned(ip):
        firewall.unban(ip)
        storage.unban(ip)
        logger.info(f'{ip} has been unbanned')


def canProceed(connection):
    return not storage.isLimitExceeded(connection)


def isBanned(connection):
    return storage.isBanned(connection)


def record(connection):
    storage.record(connection)


def unbanService():
    gmt = time.gmtime()
    now = calendar.timegm(gmt)
    for ip in storage.bannedUsers:
        if now - storage.bannedUsers[ip] >= config.BAN_TIME * 1000:
            unban(ip)
            del storage.bannedUsers[ip]


firewall = UFW() # By default