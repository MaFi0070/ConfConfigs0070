import os, re, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    links = []
    async for msg in client.iter_messages("napsternetv", limit=300):
        if msg.text:
            links += re.findall(r"(?:vless|vmess|trojan|ss)://[^\s\"'<>]+", msg.text)
    unique = list(dict.fromkeys(links))
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique))
    print(f"{len(unique)} configs saved")
    await client.disconnect()

asyncio.run(main())
