import telebot
import DB_connection as db
import re

token = '6370582872:AAEv0DKfC_TWVuIBRGLrJ3ZgPbm0IIBM1KM'
bot = telebot.TeleBot(token)

create_user = """
    INSERT INTO users
        (user_id)
    VALUES (?);
    """
@bot.message_handler(commands=['start'])
def start_message(message):
    info = db.cursor.execute('SELECT * FROM users WHERE user_id=?', (message.from_user.id,))
    record = info.fetchone()
    if record is None:
        db.cursor.execute(create_user, (message.from_user.id,))
        db.cursor.connection.commit()
        bot.send_message(message.chat.id, "Привет, я - бот психолог. Отправь мне текст или аудиосообщение и получи"
                                        " советы по твоему состоянию. \nНо для начала, введи tgID своего близкого человека, "
                                        "к которыму ты бы не постеснялся обратиться за помощью в трудную минуту. Если "
                                        "такого нет, отправь \"-\".")
@bot.message_handler(content_types='text')
def message_reply(message):
    info = db.cursor.execute('SELECT have_friends FROM users WHERE user_id=?', (message.from_user.id,))
    if (info.fetchone()[0] is None):
        if (re.search(r'@{1}.*', message.text)):
            bot.send_message(message.chat.id, "qwewqe")
            db.cursor.execute("""
                            UPDATE users 
                            SET have_friends = 1
                            WHERE user_id=?
                            """, (message.from_user.id,))
            db.cursor.execute("""
                            INSERT INTO users_friends
                                (user_friend, user_id)
                            VALUES (?, ?);
                            """, (message.text, message.from_user.id))
            db.cursor.connection.commit()
            bot.send_message(message.chat.id, "Ваш близкий был успешно добавлен! Можете приступать к "
                                              "функционалу бота!")
        elif (message.text == "-"):
            db.cursor.execute("""
                            UPDATE users 
                            SET have_friends = 0
                            WHERE user_id=?
                            """, (message.from_user.id,))
            db.cursor.connection.commit()
            bot.send_message(message.chat.id, "Надеемся наш бот поможет справиться с вашими проблемами не прибегая"
                                              " к помощи других людей!")
        else:
            bot.send_message(message.chat.id, "Некорректный ввод! Пожалуйста, введите tgID в виде @(имя пользователя)"
                                              ", либо \"-\", если не хотите никого вводить.")
        bot.send_message(message.chat.id,
                         "Теперь вы можете писать сообщение с вашими проблемами(минимум 20 слов), либо отправлять"
                         " голосовое (но не чаще, чем раз в 5 минут).")
    else:
        if (len(message.text.split()) >= 2):
            bot.send_message(message.chat.id,
                             "Ваше сообщение было взято на обработку! Ожидание ответа...")
        else:
            bot.send_message(message.chat.id,
                         "К сожалению, боту недостаточно такого маленького текста для понимания ваших эмоций."
                         " Пожалуйста, напишите текст от 20 слов и более.")

@bot.message_handler(content_types='voice')
def audio_message_reply(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
bot.polling(none_stop=True)