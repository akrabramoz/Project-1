from pyrogram import Client
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

with Client("my_session", api_id, api_hash) as app:
    print("Session created successfully!")
