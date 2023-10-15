import os
import json

# from dotenv import load_dotenv


def init_config():
    config_filename = os.getenv("CONFIG_FILENAME", "config.json")
    with open(config_filename, "r") as f:
        config = json.load(f)
    
    return config


# def init_config_from_env(filename=None):
#     if filename:
#         load_dotenv(filename)
#     else:
#         load_dotenv()

#     return init_config()
