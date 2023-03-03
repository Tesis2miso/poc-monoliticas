import os

PULSAR_ENV: str = 'BROKER_HOST'

def broker_host():
    return os.getenv(PULSAR_ENV, default="34.121.128.81")