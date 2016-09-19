import discord
import asyncio
import skill_adapter
from datetime import datetime
import sys

def queue_put(q):
    asyncio.ensure_future(q.put(sys.stdin.readline()))

async def on_ready():
    print("Loading skills:")
    await skill_adapter.load_skills()
    print("Done loading skills!")

async def on_message(phrase):
    intents = sorted(skill_adapter.engine.determine_intent(phrase), key = lambda x: x["confidence"])
    print(intents)
    if len(intents) < 1:
        print("I'm sorry, I couldn't understand you")
    else:
        intent = intents[0]
        skill = skill_adapter.skills[intent.pop("intent_type")]
        intent.pop("target")
        intent.pop("confidence")
        print(str(await skill.parse(None, **intent)))

async def main_loop():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    loop.add_reader(sys.stdin, queue_put, queue)
    await on_ready()
    while True:
        phrase = await queue.get()
        print(await on_message(phrase))

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_loop())
    finally:
        loop.close()
