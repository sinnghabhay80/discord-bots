import os
import discord
import requests
import json
import random
from decouple import config

token = config('token')

client = discord.Client()

discourage_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "lowly", "scum" ]

encourage_starter = [ "Cheer up!", "Hang in there.", "You are a great person/bot!" ]

encouragements = []

responding = True

def get_encourage_text():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    encourage_text = json_data[0]['q'] + " - " + json_data[0]['a']
    return encourage_text

def update_encouragements(encouraging_text):
    encouragements.append(encouraging_text)

def delete_encouragment(index):
    del encouragements[index]

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global responding
    msg = message.content.lower()

    if message.author == client.user:
        return

    if msg.startswith("$encourage"):
        encourage_text = get_encourage_text()
        await message.channel.send(encourage_text)

    if msg.startswith("hello"):
        await message.channel.send("Hello! "+ str(message.author))

    if responding:
        encourage_options = encourage_starter + encouragements

        if any(word in msg for word in discourage_words):
            await message.channel.send(random.choice(encourage_options))

    if msg.startswith("$new"):
        encouraging_text = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_text)
        await message.channel.send("New Encouragement Text Added.")

    if msg.startswith("$del"):
        if len(encouragements) > 0:
            if msg.split("$del", 1)[1] != "":
                index = int(msg.split("$del", 1)[1])
                delete_encouragment(index)
        await message.channel.send(list(encouragements))

    if msg.startswith("$list"):
        await message.channel.send(list(encouragements))

    if msg.startswith("$responding"):
        val = msg.split("$responding ", 1)[1]
        if val.lower() == "true":
            responding = True
            await message.channel.send("Bot will now respond to sad words.")
        elif val.lower() == "false":
            responding = False
            await message.channel.send("Bot will not respond to sad words.")

client.run(token)