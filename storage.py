import json

import config
import time
import calendar


def isBanned(ip):
    return ip in bannedUsers


def unban(ip):
    del bannedUsers[ip]
    # TODO: async
    with open('storage.json', mode='w') as file:
        # convert dictionary to json string and write it
        file.write(json.dumps(bannedUsers))


def ban(connection):
    bannedUsers[connection.ip] = calendar.timegm(gmt)
    # TODO: async
    with open('storage.json', mode='w') as file:
        # convert dictionary to json string and write it
        file.write(json.dumps(bannedUsers))


def isLimitExceeded(connection):
    if connection.email in limits:
        if limits[connection.email] == -1:
            return False

        if connection.email in users:
            if connection.ip in users[connection.email]:
                if calendar.timegm(gmt) - users[connection.email][connection.ip] >= config.USER_CONNECTION_LIFETIME * 1000:
                    # connection is not active
                    del users[connection.email][connection.ip]
                return False

            return len(users[connection.email]) >= limits[connection.email]

        return limits[connection.email] < 1

    if connection.email in users:
        if connection.ip in users[connection.email]:
            if calendar.timegm(gmt) - users[connection.email][connection.ip] >= config.USER_CONNECTION_LIFETIME * 1000:
                # connection is not active
                del users[connection.email][connection.ip]
            return False

        return len(users[connection.email]) >= config.ALLOWED_CONNECTIONS

    return config.ALLOWED_CONNECTIONS < 1


def record(connection):
    if connection.email not in users:
        users[connection.email] = {}

    users[connection.email][connection.ip] = calendar.timegm(gmt)


def cleanService():
    now = calendar.timegm(gmt)
    for email in users:
        ips = users[email]
        for ip in ips:
            if now - ips[ip] >= config.USER_CONNECTION_LIFETIME * 1000:
                del ips[ip]
        if len(ips) == 0:
            del users[email]


gmt = time.gmtime()


"""

Structure:

{
    "email": [
        {
            "ip": {
                "record_time": "time"
            }
        }
    ]
} 

"""

# Current connections
users = {}

with open('users.json') as usersFile:
    limits = json.load(usersFile)

"""

Storage.json file structure:

{
    "ip": "time"
}

"""

# TODO: create file if it doesn't exist
with open('storage.json') as storageFile:
    bannedUsers = json.load(storageFile)
