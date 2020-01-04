#!/usr/bin/python3
import requests
import config
import json
import time


class PlayerClass:
    def __init__(self, name, uuid, lastLogin=0, lastLogout=0):
        if name == "" or uuid == "":
            raise Exception("Invalid user with name " +
                            name + "and UUID " + uuid + "!")
        self.name = name
        self.uuid = uuid
        self.lastLogin = lastLogin
        self.lastLogout = lastLogout

    def isOnline(self):
        if self.lastLogin == 0 or self.lastLogout == 0:
            return False  # Assume offline
        if self.lastLogout < self.lastLogin:
            return True
        return False


if config.GOTIFY_URL and config.GOTIFY_TOKEN:
    if config.GOTIFY_TOKEN != "" and config.GOTIFY_URL != "":
        usingGotify = True
        import gotify
        gotifyServer = gotify.Server(config.GOTIFY_URL, config.GOTIFY_TOKEN)


def getInfo(text):
    if len(text) == 32:  # Already an UUID
        r = requests.get(
            "https://api.mojang.com/user/profiles/" + text + "/names")
        j = json.loads(r.text)
        lastname = j[len(j)-1]
        name = lastname["name"]
        return name, text
    if len(text) > 16:  # Invalid username
        return "", ""
    r = requests.get(
        'https://api.mojang.com/users/profiles/minecraft/' + text)
    if r.text == "":  # The username does not exist
        return "", ""
    j = json.loads(r.text)
    uuid = j["id"]
    name = j["name"]
    return name, uuid


def updateClass(player):
    r = requests.get('https://api.hypixel.net/player?key=' +
                     config.HYPIXEL_API_KEY + '&uuid=' + player.uuid)
    j = json.loads(r.text)
    player.lastLogout = j["player"]["lastLogout"]
    player.lastLogin = j["player"]["lastLogin"]


def notify(text, priority=5):
    if usingGotify:
        gotify.sendMessage(gotifyServer, text, priority=priority)
    else:
        print(text)


uuid = []
for player in config.PLAYERS:
    name, uid = getInfo(player)
    print("Using UUID " + uid + " for player " + name + "!")
    p = PlayerClass(name, uid, 0, 0)
    updateClass(p)
    uuid.append(p)


while True:
    time.sleep(10)
    for player in uuid:
        old = player.isOnline()
        updateClass(player)
        if (player.isOnline() != old):  # Status changed
            if player.isOnline() is True:
                # This would make a notification sound
                notify(player.name + " is now online on Hypixel!", 5)
            else:
                # This won't make a notification sound
                notify(player.name + " is now offline on Hypixel!", 2)
        time.sleep(3)
