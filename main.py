import re
import time
from pyrogram import Client, filters
import subprocess
import gunicorn

# إعدادات الجلسة (SESSION STRING)
SESSION_STRING = "BAE3tTMALDxrv4uOSmrbXhYXk6Us-j2S_SZHYPMBPylNfIItX8eZW3kUKaZI3U9C48Cu1cRAs8BobMujyVOWsq1hSSJoKM_F-j8CoAblO0qW2vekguyBJPxl0YuJkrhJxgaIA83OlnleGtkpf9eH84vdyPmernMhfZwQU0UNR8EdDvi1KXWnBKJQ1-mt8fsNEaVyBJnRDRZKez9OEMjQIgISJmJmKVKIjhzAAaM1_kEcE3Dcok6KmeLFgT75J1F8elkB9238W3QjZqQgaruvkiu3YXUw70-DY9_b6eJmpaqNYzrBrlIZLJzlKhoGqPlMe12wBeYn7inlUKc9-50hrrJ8Y3zI2gAAAAGG6oJvAA"

# قاموس تعيين القنوات المصدر إلى الوجهات
source_destination_mapping = {
    # تاست خاص بي 
    (-1002072462276): [-1002131940541],
    #  تاست خاص بي المرسل
    (-1001949802085): [-1002136852657],

    
    # Modern Elliot
    (-1002043678834): [-1001998466958],

    # US30 Kingdom
    (-1001817788517): [-1002088207771],

    # Gold Killer
    (-1002142323678): [-1002054664542],

    # Fx Elite Club
    (-1002057255999): [-1002134643748],

    # Fx Predators
    (-1002052838344): [-1002032658531],

    # NAS 100 PRO
    (-1002051989870): [-1002102118137],

    # PROPFRIM TRADERS
    (-1002064671229): [-1002002911906],

    # ZA GOLD SCALPER
    (-1002000711180): [-1002023473272],

    # FOREX HINTS
    (-1002121086305): [-1002117688852],

    # WANDA
    (-1001948739186): [-1002021715309],

    # TRADING WITH MASTER
    (-1002029100734): [-1002137778091],

    # ALEX
    (-1002039208753): [-1002082429891],

    # FOREX GURU
    (-1001992843192): [-1002051298823],

    # 15M SIGNALS
    (-1002036974913): [-1002120753195],

    # FX GOLD SIGNALS
    (-1002074929751): [-1002019115733],

    # gold sniper t2
    (-1002082501366): [-1002076836030],

    # forex tem t3
    (-1002137611540): [-1002045644238],

    # غولد إينجن t4
    (-1002071601295): [-1002122596670],
    #T
    (-1002010868458): [-1002026321203],
    #T1
    (-1002088407904): [-1002045313573], 
    #T2
    (-1001803559373): [-1002043161677],
}


# قوائم الفلترة والإعدادات
duplication = [-1002128618822, 976544]
special_sources = [-10020056659510, -10021286188220, 6777]
update_channels = [-1002072462276, -1001933189595, -1001766944676]
ignored_users = [15966619410, 9876543210]
ignored_words = [
    "https://t.me/FLV_HUB", "@ForexLeaks_bot", "@vip_leaked", "@Paragons_FX",
    "𝙡𝙚𝙖𝙠𝙚𝙙 𝙑𝙄𝙋𝙨 ", "VIPS", "@FLV_HUB", "@malaui65",
     "malaui65", "BFSBundle", "@BFSBundle", "@BFSAdmin7", "leaked" , "https://t.me/BFSbundle"
]

words_to_remove = ["Joooooooookes"]
phrases_to_replace = {
    "Helooooo world": "ople",
    "Foooooo": "Remeoomb"
}


# إنشاء عميل Pyrogram
app = Client(name="my_bot", session_string=SESSION_STRING)

def get_last_n_messages(client, chat_id, n=4):
    return client.get_chat_history(chat_id=chat_id, limit=n)

def are_messages_different(msg1, msg2):
    if msg1.text != msg2.text or msg1.caption != msg2.caption:
        return True
    if msg1.caption and not msg2.photo and not msg2.video and not msg2.document:
        return msg1.caption != msg2.text
    return False

def remove_words(text):
    for word in words_to_remove:
        text = text.replace(word, "")
    return text

def replace_phrases(text):
    for original_phrase, new_phrase in phrases_to_replace.items():
        text = re.sub(r'\b' + re.escape(original_phrase) + r'\b', new_phrase, text)
    return text

def update_target_channel(client, source_channel, target_channel, messages):
    for source_msg, target_msg in zip(messages[source_channel], messages[target_channel]):
        if are_messages_different(source_msg, target_msg):
            source_text = source_msg.text or source_msg.caption or ""
            updated_text = remove_words(source_text)
            updated_text = replace_phrases(updated_text)
            if source_msg.text:
                client.edit_message_text(chat_id=target_channel, message_id=target_msg.id, text=updated_text)
            elif source_msg.caption:
                client.edit_message_caption(chat_id=target_channel, message_id=target_msg.id, caption=updated_text)

def is_message_similar_to_others(client, message, source_channels):
    for channel_id in source_channels:
        if channel_id == message.chat.id:
            continue
        last_messages = get_last_n_messages(client, channel_id, n=5)
        for last_message in last_messages:
            if last_message.text == message.text and last_message.caption == message.caption:
                return True
    return False

@app.on_message(filters.chat(list(source_destination_mapping.keys())) & ~filters.forwarded)
def copy_message(client, message):
    try:
        if message.from_user and message.from_user.id in ignored_users:
            print(f"Ignoring message from user {message.from_user.id}")
            return

        source_channel_id = message.chat.id
        dest_channels = source_destination_mapping.get(source_channel_id, [])

        if (message.text and any(word in message.text for word in ignored_words)) or (message.caption and any(word in message.caption for word in ignored_words)):
            print(f"Ignoring message with restricted words: {message.text or message.caption}")
            return

        # تأخير النقل لمدة ثانية
        time.sleep(1)

        # التحقق من الرسائل المتشابهة في قنوات المصدر الأخرى
        if is_message_similar_to_others(client, message, source_destination_mapping.keys()):
            print("Similar message found in other source channels, skipping...")
            return

        for dest_channel_id in dest_channels:
            if source_channel_id in duplication:
                last_messages = get_last_n_messages(client, dest_channel_id, n=15)
                for last_message in last_messages:
                    if last_message.text == message.text and last_message.caption == message.caption:
                        print("Message already exists, skipping...")
                        return

            if message.text:
                message_text = remove_words(message.text)
                message_text = replace_phrases(message_text)
            elif message.caption:
                message_text = remove_words(message.caption)
                message_text = replace_phrases(message_text)
            else:
                message_text = ""

            if message.reply_to_message:
                replied_message = message.reply_to_message
                if replied_message.photo or replied_message.video or replied_message.document:
                    caption = replied_message.caption or ""
                    original_message = next(client.search_messages(chat_id=dest_channel_id, query=caption), None)
                    if original_message:
                        client.copy_message(chat_id=dest_channel_id, from_chat_id=message.chat.id, message_id=message.id, reply_to_message_id=original_message.id)
                    else:
                        client.copy_message(chat_id=dest_channel_id, from_chat_id=message.chat.id, message_id=message.id)
                elif replied_message.text:
                    original_text = replied_message.text
                    original_message = next(client.search_messages(chat_id=dest_channel_id, query=original_text), None)
                    if original_message:
                        client.copy_message(chat_id=dest_channel_id, from_chat_id=message.chat.id, message_id=message.id, reply_to_message_id=original_message.id)
                    else:
                        client.copy_message(chat_id=dest_channel_id, from_chat_id=message.chat.id, message_id=message.id)
                else:
                    client.copy_message(chat_id=dest_channel_id, from_chat_id=message.chat.id, message_id=message.id)
            else:
                if source_channel_id in special_sources and message.caption:
                    client.send_message(chat_id=dest_channel_id, text=message.caption)
                else:
                    if message_text:
                        if message.photo:
                            client.send_photo(chat_id=dest_channel_id, photo=message.photo.file_id, caption=message_text)
                        elif message.video:
                            client.send_video(chat_id=dest_channel_id, video=message.video.file_id, caption=message_text)
                        elif message.document:
                            client.send_document(chat_id=dest_channel_id, document=message.document.file_id, caption=message_text)
                        else:
                            client.send_message(chat_id=dest_channel_id, text=message_text)
                    else:
                        client.send_message(chat_id=dest_channel_id, text=message_text)

        messages = {}
        for dest_channel_id in dest_channels + [source_channel_id]:
            messages[dest_channel_id] = get_last_n_messages(client, dest_channel_id)

        for dest_channel_id in dest_channels:
            if source_channel_id in update_channels:
                update_target_channel(client, source_channel_id, dest_channel_id, messages)

    except Exception as e:
        print(f"An error occurred: {e}")
        pass

subprocess.Popen(["gunicorn", "app:app", "-b", "0.0.0.0:8080"])
app.run()
