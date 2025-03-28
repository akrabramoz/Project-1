import os
from pyrogram import Client

api_id = 20428083 # استبدله بالـ API_ID الخاص بك
api_hash = "c2c7f4fd4c392d80f859466a73b677f5"  # استبدله بالـ API_HASH الخاص بك

session_string = os.getenv("SESSION_STRING")  # جلب الجلسة من GitHub Secrets

app = Client(":memory:", api_id=api_id, api_hash=api_hash, session_string=session_string)

app.start()
print("✅ تم تسجيل الدخول بنجاح!")
