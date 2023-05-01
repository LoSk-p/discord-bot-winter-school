import discord
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
    if message.author == client.user:
        return
    if str(message.channel) == config['channel']:
        print(f"Got message: {message}")
        print(f"Got message content: {message.content}")
        mes = str(message.content).split()
        for word in mes:
            word = word.strip()
            if is_valid_ss58_address(word):
                if is_valid_ss58_address(word, valid_ss58_format=32):
                    address = word
                    response = await add_device(address, dev=DEV)
                    if response:
                        await message.channel.send(f"Address {address} from {message.author} was successfully added to subscription")
                    else:
                        await message.channel.send(f"Address {address} from {message.author} wasn't added to subscription\n Please, send your address again")
                    break
                else:
                    await message.channel.send(f"Address {word} from {message.author} has wrong format. Please, use address from https://blackmirror.robonomics.network/#/")

if __name__ == '__main__':
    get_devices(dev=DEV)
    client.run(config['token'])