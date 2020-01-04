import requests


class Server:
    def __init__(self, url, token):
        self.url = url
        self.token = token


def sendMessage(server, message, priority=5):
    data = {
        "message": message,
        "priority": priority,
        "title": "Hypixel"
    }
    headers = {'X-Gotify-Key': str(server.token)}
    r = requests.post(server.url, data=data, headers=headers)
    if r.status_code == 200:
        print(r.text)
        return
    print(r)
    raise Exception("Cannot send the message to the Gotify server!")


# This is for testing only, please ignore
if __name__ == "__main__":
    import config
    server = Server(config.GOTIFY_URL, config.GOTIFY_TOKEN)
    sendMessage(server, 'https://stoicatedy.ovh', 2)
