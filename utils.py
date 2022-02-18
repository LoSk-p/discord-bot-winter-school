import robonomicsinterface as RI
import yaml
import os
import logging

def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.propagate = False
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger

logger = get_logger()

def read_config() -> dict:
    path = os.path.realpath(__file__)[:-len(__file__)]
    with open(f"{path}config/config.yaml") as f:
        config = yaml.safe_load(f)
    return config

def get_devices(dev: bool=False) -> None:
    config = read_config()
    if dev:
        interface = RI.RobonomicsInterface(
                        seed=config['subscription_owner_seed'], 
                        remote_ws="ws://127.0.0.1:9944"
                        )
    else:
        interface = RI.RobonomicsInterface(
                        seed=config['subscription_owner_seed']
                        )
    devices = interface.rws_list_devices(interface.define_address())
    logger.info(f"List of devices: {devices}")
    with open(config['devices_file'], "w") as f:
        for device in devices:
            f.write(f"{device}\n")

def add_device(address: str, dev: bool=False) -> bool:
    config = read_config()
    with open(config['devices_file']) as f:
        devices = f.readlines()
    if f"{address}\n" in devices:
        logger.info(f"Address {address} is exists")
        return True
    devices.append(address)
    if dev:
        interface = RI.RobonomicsInterface(
                        seed=config['subscription_owner_seed'], 
                        remote_ws="ws://127.0.0.1:9944"
                        )
    else:
        interface = RI.RobonomicsInterface(
                        seed=config['subscription_owner_seed']
                        )
    try:
        interface.rws_set_devices(devices)
        with open(config['devices_file'], "a") as f:
            f.write(f"{address}\n")
        f"Address {address} was successfully added to subscription"
        return True
    except Exception as e:
        logger.info(f"Can't set devices with error: {e}")
        return False
