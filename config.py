import os
from dotenv import load_dotenv

initial = os.environ
load_dotenv()


def _getConfig(key):
    if initial[key]:
        return initial[key]
    return os.environ[key]


HYPIXEL_API_KEY = _getConfig("HYPIXEL_API_KEY")
GOTIFY_URL = _getConfig("GOTIFY_URL")
GOTIFY_TOKEN = _getConfig("GOTIFY_TOKEN")
PLAYERS = _getConfig("PLAYERS").split(' ')
