import discord
from utils import read_config, add_device, get_devices
from substrateinterface.utils.ss58 import is_valid_ss58_address

# Work with local node
DEV = True

client = discord.Client()
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
    print(message.channel)
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
        result = add_device(address, dev=DEV)
        if result:
            response = f"Address {address} from {message.author} was successfully added to subscription"
            await message.channel.send(response)
        else:
            response = f"Address {address} from {message.author} wasn't added to subscription\n Please, send your address again"
            await message.channel.send(response)

if __name__ == '__main__':
    get_devices(dev=DEV)
    client.run(config['token'])