import json
import os
from pathlib import Path

from notion_client import Client

DEFAULT_CONFIG_LOCATION = ".notionblueprint"
DEFAULT_CONFIG_NAME = "secrets.json"
DEFAULT_CONFIG_FILE = str(
    Path.home() / DEFAULT_CONFIG_LOCATION / DEFAULT_CONFIG_NAME
)


def get_notionclient(auth_token_key=None):
    # If auth_token_key is not provided, use the default
    if auth_token_key is None:
        try:
            auth_token_key = get_config().get("notion_token")
        except Exception:
            raise ValueError("Config file does not have notion token.")

    notion = Client(auth=auth_token_key)

    return notion


def get_config(config_file=None):
    # If config_file is not provided, use the default
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = None

    return config
