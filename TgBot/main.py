import os

import telebot
import DB_connection as db
import re
from for_audio.audio_emotions import audio_emotions
from for_text.text_emotions import text_emotions

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
    record = info.fetchall()
    print(record)
    if len(record) == 0:
        db.cursor.execute(create_user, (message.from_user.id,))
        db.cursor.connection.commit()
        bot.send_message(message.chat.id, "Hi, I'm a bot psychologist. Send me a text or audio message and receive "
                                          "advice on your condition. \nBut first, enter the tgID of your loved one,"
                                          " whoever you would not be embarrassed to turn to for help in difficult times. If "
                                          "there is no such thing, send \"-\".")


@bot.message_handler(content_types='text')
def message_reply(message):
    check = db.cursor.execute('SELECT user_name FROM users WHERE user_id=?', (message.from_user.id,)).fetchall()
    if len(check) == 0:
        bot.send_message(message.chat.id,
                         "Please enter the /start command before using the bot")
    else:
        info = db.cursor.execute('SELECT have_friends FROM users WHERE user_id=?', (message.from_user.id,)).fetchall()[0][0]
        print(info)
        if (info is not None):
            if (len(message.text.split()) >= 2):
                emotion = text_emotions(message.text)
                friend = db.cursor.execute('SELECT have_friends FROM users WHERE user_id=?', (message.from_user.id,)).fetchall()[0][0]
                if (emotion == "empty" or emotion == "neutral"):
                    bot.send_message(message.chat.id,
                                     "The bot could not recognize the emotion you are experiencing. Most likely you are feeling"
                                     " fine.")
                if (emotion == "sadness"):
                    if friend:
                        name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                              (message.from_user.id,)).fetchall()[0][0]
                        id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                            (name_users_friend,)).fetchall()
                        if len(id_users_friend) != 0:
                            bot.send_message(id_users_friend[0][0],
                                        f"Your friend @{message.from_user.username} is sad right now. Try to"
                                             f" support him, this is very important for him!")
                        bot.send_message(message.chat.id,
                                         "You are sad now. At such moments it is important to find support, try to do "
                                         "your favorite thing, or, on the contrary, try something new. Usually, walks in the fresh air "
                                         "air can help you cope with your thoughts at least a little."
                                         f"\nDon't forget that your friend @{name_users_friend} is always with you and ready to help you!")
                    else:
                        bot.send_message(message.chat.id,
                                         "You are sad now. At such moments it is important to find support, try to do "
                                         "your favorite thing, or, on the contrary, try something new. Usually, walks in the fresh air "
                                         "air can help you cope with your thoughts at least a little.")

                if (emotion == "enthusiasm"):
                    bot.send_message(message.chat.id,
                                        "You look like you're having a blast right now! We hope you are now experiencing such "
                                        "emotions that you will remember for the rest of your life!")
                if (emotion == "worry"):
                    if friend:
                        name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                              (message.from_user.id,)).fetchall()[0][0]
                        id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                            (name_users_friend,)).fetchall()
                        if len(id_users_friend) != 0:
                            bot.send_message(id_users_friend[0][0],
                                             f"Your friend @{message.from_user.username} is worried about something right now."
                                             f" Try to find out what's wrong with him so that everything will definitely be fine!")
                        bot.send_message(message.chat.id,
                                         "You seem to be very worried right now. Try to breathe deeper, if possible, "
                                         "wash your face with cold water. If you are concerned about your health, be sure to consult a doctor "
                                         f"or your friend @{name_users_friend}. They will be able to help you more specifically.")
                    else:
                        bot.send_message(message.chat.id,
                                         "You seem to be very worried right now. Try to breathe deeper, if possible, "
                                         "wash your face with cold water. If you are concerned about your health, be sure to consult a doctor.")
                if emotion == "surprise":
                    bot.send_message(message.chat.id,
                                     "You are clearly surprised by something now. We hope that this surprise is extremely positive!")
                if emotion == "love":
                    bot.send_message(message.chat.id,
                                     "You feel a feeling of love. Wonderful feeling!")
                if emotion == "fun" or emotion == "happiness":
                    bot.send_message(message.chat.id,
                                     "You’re clearly having fun! Try to stretch out these emotions as long as possible, it’s not always possible "
                                     "we feel so good. Share your joy with your loved ones!")
                if emotion == "hate":
                    bot.send_message(message.chat.id,
                                     "You are clearly in an unpleasant situation now. Try to calm down and let it go, "
                                     "so as not to do anything stupid.")
                if emotion == "boredom":
                    bot.send_message(message.chat.id,
                                     f" You're bored now. Try something new or meet friends, usually people"
                                    " helps avoid boredom.")
                if emotion == "relief":
                    bot.send_message(message.chat.id,
                                     " You feel relieved about this. We are very glad that this happened!")
                if emotion == "anger":
                    if friend:
                        name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                              (message.from_user.id,)).fetchall()[0][0]
                        id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                            (name_users_friend,)).fetchall()
                        if len(id_users_friend) != 0:
                            bot.send_message(id_users_friend[0][0],
                                             f"Your friend @{message.from_user.username} is angry now. Try "
                                             f"gently ask how you can help him so as not to anger him even more.")
                        bot.send_message(message.chat.id,
                                         "You're clearly angry right now. Try to relax and start breathing in a square pattern. "
                                         "The idea is that you take deep breaths in and out and hold them in between "
                                         "breathing. The time for each action should be the same.\n"
                                         "Also try to wash your face with cool water and think about how you can avoid "
                                         f"in the future of this malice. And don't forget you can always contact @{name_users_friend}.")
                    else:
                        bot.send_message(message.chat.id,
                                         "You're clearly angry right now. Try to relax and start breathing in a square pattern. "
                                         "The idea is that you take deep breaths in and out and hold them in between "
                                         "breathing. The time for each action should be the same.\n"
                                         "Also try to wash your face with cool water and think about how you can avoid in the future of this malice.")
    # ---------------------------------------------------------------------------------------------------------------------------
            else:
                bot.send_message(message.chat.id,
                                 "Unfortunately, such a small text is not enough for the bot to understand your emotions."
                                 "Please write a text of 2 words or more.")
        else:
            if (re.search(r'@{1}.*', message.text)):
                db.cursor.execute("""
                                UPDATE users 
                                SET have_friends = 1, user_name=?
                                WHERE user_id=?
                                """, (message.from_user.username, message.from_user.id,))
                db.cursor.execute("""
                                INSERT INTO users_friends
                                    (user_friend, user_id)
                                VALUES (?, ?);
                                """, (message.text[1:], message.from_user.id))
                db.cursor.connection.commit()
                bot.send_message(message.chat.id, "Your friend has been successfully added! You can proceed "
                                                  "bot functionality!")
                bot.send_message(message.chat.id,
                                 "Now you can write a message with your problems (minimum 2 words), or send"
                                 " voice message.")
            elif (message.text == "-"):
                db.cursor.execute("""
                                UPDATE users 
                                SET have_friends = 0
                                WHERE user_id=?
                                """, (message.from_user.id,))
                db.cursor.connection.commit()
                bot.send_message(message.chat.id, "We hope our bot will help you solve your problems without resorting "
                                                  "to help other people!")
                bot.send_message(message.chat.id,
                                 "Now you can write a message with your problems (minimum 2 words), or send"
                                 " voice message.")
            else:
                bot.send_message(message.chat.id, "Invalid input! Please enter tgID as @(username)"
                                                  ", or \"-\" if you don't want to enter anyone.")


@bot.message_handler(content_types='voice')
def audio_message_reply(message):
    check = db.cursor.execute('SELECT user_name FROM users WHERE user_id=?', (message.from_user.id,)).fetchall()
    if len(check) == 0:
        bot.send_message(message.chat.id,
                         "Please enter the /start command before using the bot")
    else:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'voice_lines\\{message.chat.id}.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)
        emotions = audio_emotions(f'voice_lines\\{message.chat.id}.ogg')[0]
        basic_emotions = ['sad', 'angry', 'disgust', 'fear', 'happy', 'neutral']
        friend = db.cursor.execute('SELECT have_friends FROM users WHERE user_id=?', (message.from_user.id,)).fetchall()[0][0]
        if emotions[5] == 1.0:
            bot.send_message(message.chat.id,
                            "The bot could not recognize the emotion you are experiencing. Most likely you are feeling "
                             "fine.")
        if emotions[4] == 1.0:
            bot.send_message(message.chat.id,
                             "You’re clearly having fun! Try to stretch out these emotions as long as possible, it’s not always possible "
                             "we feel so good. Share your joy with your loved ones!")
        if emotions[3] == 1.0:
            if friend:
                name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                      (message.from_user.id,)).fetchall()[0][0]
                id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                    (name_users_friend,)).fetchall()
                if len(id_users_friend) != 0:
                    bot.send_message(id_users_friend[0][0],
                                     f"Your friend @{message.from_user.username} is scared right now. Try to"
                                     f" help him, this is very important for him!")
                bot.send_message(message.chat.id,
                                 "You're scared right now. Try to relax and start breathing in a square pattern. "
                                 "The idea is that you take deep breaths in and out and hold them in between "
                                 "breathing. The time for each action should be the same.\n"
                                 f"And be sure to contact @{name_users_friend}, now more than ever you need help!")
            else:
                bot.send_message(message.chat.id,
                                 "You're scared right now. Try to relax and start breathing in a square pattern."
                                 "The idea is that you take deep breaths in and out and hold them in between "
                                 "breathing. The time for each action should be the same. Also try to find "
                                 "people who can help you cope with this condition.")
        if emotions[2] == 1.0:
            bot.send_message(message.chat.id,
                             "You are clearly disgusted. Try to calm down and get rid of the source, "
                             "otherwise the problem will be difficult to solve. Or find people who will help you with this.")
        if emotions[1] == 1.0:
            if friend:
                name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                      (message.from_user.id,)).fetchall()[0][0]
                id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                    (name_users_friend,)).fetchall()
                if len(id_users_friend) != 0:
                    bot.send_message(id_users_friend[0][0],
                                     f"Your friend @{message.from_user.username} is angry now. Try "
                                     f"gently ask how you can help him so as not to anger him even more.")
                bot.send_message(message.chat.id,
                                 "You're clearly angry right now. Try to relax and start breathing in a square pattern. "
                                 "The idea is that you take deep breaths in and out and hold them in between "
                                 "breathing. The time for each action should be the same.\n"
                                 "Also try to wash your face with cool water and think about how you can avoid "
                                 f"in the future of this malice. And don't forget you can always contact @{name_users_friend}.")
            else:
                bot.send_message(message.chat.id,
                                 "You're clearly angry right now. Try to relax and start breathing in a square pattern. "
                                 "The idea is that you take deep breaths in and out and hold them in between "
                                 "breathing. The time for each action should be the same.\n"
                                 "Also try to wash your face with cool water and think about how you can avoid in the future of this malice.")
        if emotions[0] == 1.0:
            if friend:
                name_users_friend = db.cursor.execute('SELECT user_friend FROM users_friends WHERE user_id=?',
                                                      (message.from_user.id,)).fetchall()[0][0]
                id_users_friend = db.cursor.execute('SELECT user_id FROM users WHERE user_name=?',
                                                    (name_users_friend,)).fetchall()
                if len(id_users_friend) != 0:
                    bot.send_message(id_users_friend[0][0],
                                     f"Your friend @{message.from_user.username} is sad right now. Try to"
                                     f" support him, this is very important for him!")
                bot.send_message(message.chat.id,
                                 "You are sad now. At such moments it is important to find support, try to do "
                                 "your favorite thing, or, on the contrary, try something new. Usually, walks in the fresh air "
                                 "air can help you cope with your thoughts at least a little."
                                 f"\nDon't forget that your friend @{name_users_friend} is always with you and ready to help you!")
            else:
                bot.send_message(message.chat.id,
                                 "You are sad now. At such moments it is important to find support, try to do "
                                 "your favorite thing, or, on the contrary, try something new. Usually, walks in the fresh air "
                                 "air can help you cope with your thoughts at least a little.")
        os.remove(f'voice_lines\\{message.chat.id}.ogg')


bot.polling(none_stop=True)
