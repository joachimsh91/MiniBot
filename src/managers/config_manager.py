"""
Configuration file manager

"""

import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

SETUP_FILE = os.path.join(BASE_DIR, "setup.json")


def load_config():
    """
    Loads the entire JSON config.
    """

    if not os.path.exists(SETUP_FILE):
        return {}

    try:
        with open(SETUP_FILE, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        print("[Config] Invalid JSON detected, resetting config.")
        return {}


def save_config(data):
    """
    Saves full config dictionary.
    """

    with open(SETUP_FILE, "w") as f:
        json.dump(data, f, indent=4)


def save_region(region, key):
    """
    Save region coordinates.
    """

    data = load_config()

    data[key] = {
        "left": region[0],
        "top": region[1],
        "width": region[2],
        "height": region[3]
    }

    save_config(data)

    print(f"[Config] Saved region: {key}")


def load_region(key):
    """
    Load saved region.
    """

    data = load_config()

    region = data.get(key)

    if not region:
        return None

    return (
        region["left"],
        region["top"],
        region["width"],
        region["height"]
    )


def save_value(key, value):
    """
    Save any config value.
    """

    data = load_config()

    data[key] = value

    save_config(data)

    print(f"[Config] Saved value: {key}")


def load_value(key):
    """
    Loads hotkey.
    """

    data = load_config()

    return data.get(key)
