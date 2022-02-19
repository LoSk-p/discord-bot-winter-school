import discord
import threading
from utils import read_config, add_device, get_devices
from substrateinterface.utils.ss58 import is_valid_ss58_address

# Work with local node
DEV = False

client = discord.Client(heartbeat_timeout=120)
config = read_config()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == config['guild']:
            break
    print(
        f'{client.user} is connected to the {guild.name}\n'
    )

@client.event
async def on_message(message):
    if message.author == client.user or message.author == "MEE6#4876":
        return
    if str(message.channel) == config['channel']:
        print(f"Got message: {message.content}")
        mes = str(message.content).split()
        for word in mes:
            word = word.strip()
            if is_valid_ss58_address(word):
                address = word
                break
        else:
            address = ""
        response = await add_device(address, message, dev=DEV)
        if response:
            await message.channel.send(f"Address {address} from {message.author} was successfully added to subscription")
        else:
            await message.channel.send(f"Address {address} from {message.author} wasn't added to subscription\n Please, send your address again")

if __name__ == '__main__':
    get_devices(dev=DEV)
    client.run(config['token'])