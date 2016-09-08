import discord
import asyncio
import skill_adapter
import os

client = discord.Client()

@client.event
async def on_ready():
    global uid
    uid = "<@"+client.user.id+">"
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('======')
    await skill_adapter.load_skills()

@client.event
async def on_message(message):
    print(str(message.content))
    if message.content.startswith(uid):
        phrase = message.content.lstrip(uid)
        intents = sorted(skill_adapter.engine.determine_intent(phrase), key = lambda x: x["confidence"])
        print("Message recieved. Responding")
        print(intents)
        if len(intents) < 1:
            await client.send_message(message.channel, "I'm sorry, I couldn't understand you")
        else:
            intent = intents[0]
            skill = skill_adapter.skills[intent.pop("intent_type")]
            intent.pop("target")
            intent.pop("confidence")
            await client.send_message(message.channel, str(await skill.parse(message, **intent)))

def main():
    client.run(os.environ["discord"])

if __name__=='__main__':
    main()
