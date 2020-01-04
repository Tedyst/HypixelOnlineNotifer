import requests


class Server:
    def __init__(self, url, token):
        self.url = url
        self.token = token


def sendMessage(server, message):
    data = {
        "message": message,
        "priority": 2,
        "title": "Hypixel"
    }
    headers = {'X-Gotify-Key': str(server.token)}
    r = requests.post(server.url, data=data, headers=headers)
    if r.status_code == 200:
        print(r.text)
        return
    print(r)
    raise Exception("Idk what happened")
