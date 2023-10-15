import os
import json

def init_config():
    config_filename = os.path.expanduser(os.getenv("CONFIG_FILENAME", "config.json"))
    with open(config_filename, "r") as f:
        config = json.load(f)
    
    return config
