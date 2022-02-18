import discord
from utils import read_config, add_device, get_devices

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
    if str(message.channel) == config['channel']:
        print(f"Got message: {message.content}")
        result = add_device(message.content, dev=DEV)
        if result:
            response = f"Address {message.content} was successfully added to subscription"
            await message.channel.send(response)
        else:
            response = f"Address {message.content} wasn't added to subscription\n Please, send your address again"
            await message.channel.send(response)

if __name__ == '__main__':
    get_devices(dev=DEV)
    client.run(config['token'])