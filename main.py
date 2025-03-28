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
}

# قوائم الفلترة والإعدادات
duplication = [-1002128618822, 976544]
special_sources = [-10020056659510, -10021286188220, 6777]
update_channels = [-1002072462276, -1001933189595, -1001766944676]
ignored_users = [15966619410, 9876543210]
ignored_words = [
    "https://t.me/FLV_HUB", "@ForexLeaks_bot", "@vip_leaked", "@Paragons_FX",
    "𝙡𝙚𝙖𝙠𝙚𝙙 𝙑𝙄𝙋𝙨 ", "VIPS", "@FLV_HUB", "https://t.me/", "@malaui65",
    "t.me", "malaui65", "BFSBundle", "@BFSBundle", "@BFSAdmin7", "leaked"
]

words_to_remove = ["Joooooooookes"]
phrases_to_replace = {
    "Helooooo world": "ople",
    "Foooooo": "Remeoomb"
}


# إنشاء عميل Pyrogram
app = Client(name="my_bot", session_string=SESSION_STRING)

def get_last_n_messages(client, chat_id, n=1):
    """جلب آخر رسالة من القناة"""
    return client.get_chat_history(chat_id=chat_id, limit=n)

def are_messages_similar(msg1, msg2):
    """مقارنة متقدمة لأنواع الرسائل"""
    try:
        # مقارنة النصوص والتعليقات
        text_match = (msg1.text or "") == (msg2.text or "")
        caption_match = (msg1.caption or "") == (msg2.caption or "")
        
        if not (text_match and caption_match):
            return False
        
        # مقارنة الوسائط
        if msg1.media and msg2.media:
            if msg1.photo and msg2.photo:
                return msg1.photo.file_id == msg2.photo.file_id
            if msg1.sticker and msg2.sticker:
                return msg1.sticker.file_id == msg2.sticker.file_id
            if msg1.video and msg2.video:
                return msg1.video.file_id == msg2.video.file_id
            if msg1.document and msg2.document:
                return msg1.document.file_id == msg2.document.file_id
            return False
        return True
    except Exception as e:
        print(f"خطأ في المقارنة: {e}")
        return False

def get_last_message_per_source(client):
    """جلب آخر رسالة من كل المصادر"""
    last_messages = {}
    for source_id in source_destination_mapping:
        try:
            history = client.get_chat_history(source_id, limit=1)
            last_msg = next(history, None)
            if last_msg:
                last_messages[source_id] = last_msg
        except Exception as e:
            print(f"فشل جلب الرسالة من {source_id}: {e}")
    return last_messages

def remove_words(text):
    """حذف الكلمات الممنوعة"""
    for word in words_to_remove:
        text = text.replace(word, "")
    return text

def replace_phrases(text):
    """استبدال العبارات المحددة"""
    for original, replacement in phrases_to_replace.items():
        text = re.sub(r'\b' + re.escape(original) + r'\b', replacement, text)
    return text

@app.on_message(filters.chat(list(source_destination_mapping.keys())) & ~filters.forwarded)
def copy_message(client, message):
    try:
        # فلترة المستخدمين الممنوعين
        if message.from_user and message.from_user.id in ignored_users:
            print(f"تم تجاهل رسالة من مستخدم ممنوع: {message.from_user.id}")
            return

        # فلترة الكلمات الممنوعة
        text_content = message.text or message.caption or ""
        if any(word in text_content for word in ignored_words):
            print(f"تم تجاهل رسالة تحتوي على كلمات ممنوعة: {text_content[:50]}...")
            return

        # تطبيق التأخير
        time.sleep(1)

        # التحقق من التكرار عبر المصادر
        other_messages = get_last_message_per_source(client)
        for src_id, last_msg in other_messages.items():
            if src_id != message.chat.id and are_messages_similar(message, last_msg):
                print(f"⏳ اكتشاف تكرار في {src_id} - تم إلغاء الإرسال")
                return

        # معالجة المحتوى
        final_text = remove_words(text_content)
        final_text = replace_phrases(final_text)

        # إرسال الرسالة حسب نوعها
        for dest_id in source_destination_mapping.get(message.chat.id, []):
            if message.photo:
                client.send_photo(dest_id, message.photo.file_id, caption=final_text)
            elif message.video:
                client.send_video(dest_id, message.video.file_id, caption=final_text)
            elif message.document:
                client.send_document(dest_id, message.document.file_id, caption=final_text)
            elif message.sticker:
                client.send_sticker(dest_id, message.sticker.file_id)
            else:
                client.send_message(dest_id, final_text)

    except Exception as e:
        print(f"حدث خطأ جسيم: {str(e)}")

# تشغيل الخادم والبوت
if __name__ == "__main__":
    subprocess.Popen(["gunicorn", "app:app", "-b", "0.0.0.0:8080"])
    app.run()
