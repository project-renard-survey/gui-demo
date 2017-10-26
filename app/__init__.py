# -*- coding: utf-8 -*-
"""Global constants and pre-app initialization stuff"""
import os
import sys
import logging
from PyQt5 import QtCore
from appdirs import AppDirs
import peewee


# Loging setup
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("peewee").setLevel(logging.WARNING)
log = logging.getLogger('app')

# Application metadata
ORG_NAME = 'Content-Blockchain'
ORG_DOMAIN = 'content-blockchain.org'
APP_NAME = 'Cast'
MAJOR = 0
MINOR = 1
PATCH = 0
APP_VERSION = '{}.{}.{}'.format(MAJOR, MINOR, PATCH)

# Application paths
APP_DIR = os.path.dirname(__file__)
_dirs = AppDirs(APP_NAME, ORG_NAME, APP_VERSION)
DATA_DIR = _dirs.user_data_dir
if not os.path.exists(DATA_DIR):
    log.debug('creating data directory at: {}'.format(DATA_DIR))
    os.makedirs(DATA_DIR)

# Settings
settings = QtCore.QSettings(ORG_NAME, APP_NAME)

# Databases
PROFILE_DB_FILENAME = 'profile.sqlite'
PROFILE_DB_PATH = os.path.join(DATA_DIR, PROFILE_DB_FILENAME)
PROFILE_DB = profile_db = peewee.SqliteDatabase(PROFILE_DB_PATH)

DATA_DB_FILENAME = 'default.sqlite'
DATA_DB_PATH = os.path.join(DATA_DIR, DATA_DB_FILENAME)
DATA_DB = peewee.SqliteDatabase(DATA_DB_PATH)

# Default local node settings
NODE_RPC_HOST = '127.0.0.1'
NODE_RPC_PORT = 8374
NODE_RPC_USER = 'user'
NODE_RPC_PASSWORD = 'password'
NODE_RPC_USE_SSL = False
NODE_BOOTSTRAP = 'charm@85.197.78.50:8375'
