from robonomicsinterface import RWS, Account, Datalog, DigitalTwin, SubEvent, Subscriber
from substrateinterface import KeypairType
import yaml
import os
import discord
import functools
import typing
import asyncio


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

def read_config() -> dict:
    path = os.path.realpath(__file__)[:-len(__file__)]
    with open(f"{path}config/config.yaml") as f:
        config = yaml.safe_load(f)
    return config

def get_devices(dev: bool=False) -> None:
    config = read_config()
    sub_owner = Account(seed=config['subscription_owner_seed'], crypto_type=KeypairType.ED25519)
    devices = RWS(Account()).get_devices(sub_owner.get_address())
    print(f"List of devices: {devices}")
    print(f"Devices file: {config['devices_file']}")
    with open(config['devices_file'], "w") as f:
        for device in devices:
            f.write(f"{device}\n")

@to_thread
def add_device(address: str, dev: bool=False) -> bool:
    config = read_config()
    with open(config['devices_file']) as f:
        devices = f.readlines()
    if f"{address}\n" in devices:
        print(f"Address {address} is exists")
        return True
    devices.append(address)
    sub_owner = Account(seed=config['subscription_owner_seed'], crypto_type=KeypairType.ED25519)
    rws = RWS(sub_owner)
    try:
        rws.set_devices(devices)
        with open(config['devices_file'], "a") as f:
            f.write(f"{address}\n")
        print(f"Address {address} was successfully added to subscription")
        return True
    except Exception as e:
        print(f"Can't set devices with error: {e}")
        return False
