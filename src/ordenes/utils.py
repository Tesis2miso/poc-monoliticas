import os
import time
PULSAR_ENV: str = 'BROKER_HOST'
DB_HOSTNAME: str = 'DB_HOSTNAME'
DB_USER_ENV: str = 'DB_USER'
DB_DATABASE: str = 'DB_DATABASE'
DB_READ_HOSTNAME: str = 'DB_READ_HOSTNAME'

def broker_host():
    return os.getenv(PULSAR_ENV, default="34.121.128.81")

def db_host():
    return os.getenv(DB_HOSTNAME, default="34.68.216.107")

def db_user():
    return os.getenv(DB_USER_ENV, default="root")

def db_database():
    return os.getenv(DB_DATABASE, default="monoliticas")


def db_host_replica():
    return os.getenv(DB_READ_HOSTNAME, default="35.226.225.189")

def db_user_replica():
    return os.getenv(DB_USER_ENV, default="root")

def db_database_replica():
    return os.getenv(DB_DATABASE, default="monoliticas-lectura")



def time_millis():
    return int(time.time() * 1000)