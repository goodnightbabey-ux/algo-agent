import os
from telethon import TelegramClient, events
from openai import OpenAI

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
openai_key = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=openai_key)

telegram = TelegramClient("session", api_id, api_hash)

SYSTEM_PROMPT = """
You are MRALGO AI support assistant.

Speak Arabic, Darija, French and English.

Help users:
- register on Quotex
- deposit
- understand VIP
- understand risk management
- read pinned messages

Affiliate:
https://broker-qx.pro/sign-up/?lid=749442

Support:
@MRALGOSUPPORT

Make your answers direct and short.
Never promise guaranteed profits.
"""

@telegram.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        text = event.raw_text

        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )

        reply = response.choices[0].message.content
        await event.reply(reply)

telegram.start()
telegram.run_until_disconnected()
