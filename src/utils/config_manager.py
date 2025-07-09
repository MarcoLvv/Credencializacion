import os
import configparser
from pathlib import Path

from src.utils.rutas import get_configuration

CONFIG_PATH = get_configuration()


def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            f.write("[GENERAL]\nmodule_id=\n")
    config.read(CONFIG_PATH)
    return config

def get_module_id():
    config = load_config()
    module_id = config["GENERAL"].get("module_id", "")
    return module_id.strip()

def set_module_id(module_id):
    config = load_config()
    config["GENERAL"]["module_id"] = module_id
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

set_module_id(get_module_id())