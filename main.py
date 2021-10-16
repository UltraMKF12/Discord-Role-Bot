import discord
import data
import os
from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

    channel = client.get_channel(data.CHANNEL_ID)
    message = await channel.fetch_message(data.MESSAGE_ID)

    for i in data.EMOJI_TO_ROLE.keys():
        await message.add_reaction(i)
    
    print("Finished adding reactions!")


@client.event
async def on_raw_reaction_add(payload):
    client.dispatch("reaction_to_role", "add", payload)


@client.event
async def on_raw_reaction_remove(payload):
    client.dispatch("reaction_to_role", "delete", payload)


@client.event
async def on_reaction_to_role(add_or_delete, payload):
    guild = await client.fetch_guild(payload.guild_id)
    user = await guild.fetch_member(payload.user_id)


    if user != client.user:
        if check_correct_message(payload.channel_id, payload.message_id):
            emoji = get_emoji(payload.emoji.name, payload.emoji.id)
            role_id = data.EMOJI_TO_ROLE[emoji]
            role = guild.get_role(role_id)

            if add_or_delete == "add":
                await user.add_roles(role)
                print(f"{role} added to {user}!")

            elif add_or_delete == "delete":
                await user.remove_roles(role)
                print(f"{role} removed from {user}!")


def check_correct_message(channel_id, message_id):
    if channel_id == data.CHANNEL_ID:
        if message_id == data.MESSAGE_ID:
            return True
    return False


# Make it work for default and custom emojis
def get_emoji(name, id):
    if id == None:
        return name
    else:
        return f"<:{name}:{id}>"


keep_alive()
client.run(os.environ['TOKEN'])