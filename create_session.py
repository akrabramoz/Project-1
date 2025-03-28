from pyrogram import Client

app = Client("my_session")

app.start()
app.send_message("me", "Session started successfully!")
app.stop()

# حفظ الجلسة في ملف
app.export_session_string()  # استخراج الجلسة كسلسلة
with open("session.txt", "w") as file:
    file.write(app.export_session_string())

print("تم حفظ الجلسة في session.txt")
