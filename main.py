import re
import time
from pyrogram import Client, filters
import subprocess
import gunicorn

# ضع SESSION_STRING هنا
SESSION_STRING = "BAE3tTMALDxrv4uOSmrbXhYXk6Us-j2S_SZHYPMBPylNfIItX8eZW3kUKaZI3U9C48Cu1cRAs8BobMujyVOWsq1hSSJoKM_F-j8CoAblO0qW2vekguyBJPxl0YuJkrhJxgaIA83OlnleGtkpf9eH84vdyPmernMhfZwQU0UNR8EdDvi1KXWnBKJQ1-mt8fsNEaVyBJnRDRZKez9OEMjQIgISJmJmKVKIjhzAAaM1_kEcE3Dcok6KmeLFgT75J1F8elkB9238W3QjZqQgaruvkiu3YXUw70-DY9_b6eJmpaqNYzrBrlIZLJzlKhoGqPlMe12wBeYn7inlUKc9-50hrrJ8Y3zI2gAAAAGG6oJvAA"


source_destination_mapping = {
    # تاست خاص بي 
    (-1002072462276): [-1002131940541],
       # gold sniper t2
    (-1002082501366): [-1002076836030],


}

duplication = [-1002128618822, 976544]
special_sources = [-10020056659510, -10021286188220, 6777]
update_channels = [-1002072462276, -1001933189595, -1001766944676]
ignored_users = [15966619410, 9876543210]
ignored_words = ["https://t.me/FLV_HUB", "@ForexLeaks_bot", "@vip_leaked", "@Paragons_FX",
                 "𝙡𝙚𝙖𝙠𝙚𝙙 𝙑𝙄𝙋𝙨 ", "VIPS", "@FLV_HUB", "https://t.me/", "@malaui65",
                 "t.me", "malaui65", "BFSBundle", "@BFSBundle", "@BFSAdmin7", "leaked"]

words_to_remove = ["Joooooooookes"]
phrases_to_replace = {
    "Helooooo world": "ople",
    "Foooooo": "Remeoomb"
}



# إنشاء عميل Pyrogram باستخدام SESSION_STRING
app = Client(name="my_bot", session_string=SESSION_STRING)


# ... [المتغيرات الأصلية تبقى كما هي] ...

DELAY_DURATION = 0.5

def are_messages_similar(msg1, msg2):
    """مقارنة متقدمة لأنواع الرسائل المختلفة"""
    try:
        # المقارنة الأساسية للنصوص والتعليقات
        if (msg1.text or "") != (msg2.text or "") or (msg1.caption or "") != (msg2.caption or ""):
            return False
        
        # مقارنة أنواع الوسائط
        if msg1.media:
            if msg1.photo and msg2.photo:
                return msg1.photo.file_id == msg2.photo.file_id
            elif msg1.sticker and msg2.sticker:
                return msg1.sticker.file_id == msg2.sticker.file_id
            elif msg1.video and msg2.video:
                return msg1.video.file_id == msg2.video.file_id
            elif msg1.document and msg2.document:
                return msg1.document.file_id == msg2.document.file_id
            else:
                return False
        return True
    except Exception as e:
        print(f"Error in comparison: {e}")
        return False

def get_last_message_per_source(client):
    """جلب آخر رسالة واحدة من كل قناة مصدر"""
    last_messages = {}
    for source_id in source_destination_mapping:
        try:
            msg = next(client.get_chat_history(source_id, limit=1), None)
            if msg:
                last_messages[source_id] = msg
        except Exception as e:
            print(f"Failed to get message from {source_id}: {e}")
    return last_messages

@app.on_message(filters.chat(list(source_destination_mapping.keys())) & ~filters.forwarded)
def copy_message(client, message):
    try:
        if message.from_user and message.from_user.id in ignored_users:
            return

        source_channel_id = message.chat.id
        dest_channels = source_destination_mapping.get(source_channel_id, [])

        if (message.text and any(word in message.text for word in ignored_words)) or (message.caption and any(word in message.caption for word in ignored_words)):
            return

        time.sleep(DELAY_DURATION)

        # جلب آخر رسالة من كل المصادر الأخرى
        other_sources_messages = get_last_message_per_source(client)
        
        # التحقق من التكرار في المصادر الأخرى
        for src_id, last_msg in other_sources_messages.items():
            if src_id == source_channel_id:  # تخطى المصدر الحالي
                continue
                
            if are_messages_similar(message, last_msg):
                print(f"⛔ Duplicate found in {src_id} - Message blocked")
                return

        # ... [بقية الكود الأصلي لإرسال الرسالة] ...

    except Exception as e:
        print(f"Error: {e}")

# ... [بقية الكود يبقى كما هو] ...
