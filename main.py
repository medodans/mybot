import os
import telebot
import yt_dlp

TOKEN = "8813602337:AAHMH0OSMZnRDEBWSlE-jiDpExuJdVzR-FM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط الفيديو للتحميل.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صالح.")
        return

    msg = bot.reply_to(message, "جاري التحميل...")

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"خطأ: {str(e)}", message.chat.id, msg.message_id)

bot.infinity_polling()
