import os
from pyrogram import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

async def main():
    await app.start()
    print("Session created successfully!")
    await app.send_message("me", "Session created successfully!")
    await app.stop()

app.run(main())

# إعادة تسمية ملف الجلسة ليسهل رفعه
os.rename("my_session.session", "session.session")
