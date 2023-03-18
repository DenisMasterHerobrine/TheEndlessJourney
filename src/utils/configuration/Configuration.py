import os
import json

from src.utils import Utils

GAME_DATA_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'TheEndlessJourney')
JSON_TEMPLATE = {
    "MUSIC_VOLUME": 20,
    "SFX_VOLUME": 35,
    "WIDTH": 1366,
    "HEIGHT": 768,
    "FPS": 144,
    "SPACESHIP_SPEED_MODIFIER": 4,
    "ENEMY_SPEED_MODIFIER": 2,
    "PARALLAX_SPEED_MODIFIER": 0.1
}

# Creates a SETTINGS.CFG file inside savegame directory
def createConfig():
    if not (os.path.exists(GAME_DATA_DIR)):
        os.mkdir(GAME_DATA_DIR)
        SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "w")
        SETTINGS_FILE.write(json.dumps(JSON_TEMPLATE, indent=3))
        SETTINGS_FILE.close()
        print("[Configuration API] Created config!")
    else:
        if os.path.exists(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON')):
            SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "r")
            valid = Utils.validateJSONFile(SETTINGS_FILE)
            SETTINGS_FILE.close()
            if not (valid.__eq__("True")):
                SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "w")
                print("[Configuration API] ERROR: Invalid configuration data! Rewriting to default parameters.")
                SETTINGS_FILE.write(json.dumps(JSON_TEMPLATE, indent=3))
                SETTINGS_FILE.close()
        else:
            SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "w")
            SETTINGS_FILE.write(json.dumps(JSON_TEMPLATE, indent=3))
            SETTINGS_FILE.close()
            print("[Configuration API] ERROR: Missing configuration data! Rewriting to default parameters.")


def getField(field):
    SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "r")
    data = json.load(SETTINGS_FILE)
    SETTINGS_FILE.close()

    value = data[field]
    return value


def updateField(field, value):
    SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "r")
    data = json.load(SETTINGS_FILE)
    SETTINGS_FILE.close()

    data[field] = value

    SETTINGS_FILE = open(os.path.join(GAME_DATA_DIR, 'SETTINGS.JSON'), "w")
    SETTINGS_FILE.write(json.dumps(data, indent=3))
    SETTINGS_FILE.close()
