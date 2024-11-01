import telebot
import random
import time
import os

token= os.getenv('TELEGRAM_TOKEN') 

stop_adding = 0
bot = telebot.TeleBot(token)
admins = [7123855395]
users = []
id_users_only = []
user_numbers = {}
users_for_lottery = []
ban_users = []
winner_id = None
count_of_users = 0
start_or_wait = False


@bot.message_handler(commands=["start"])
def start_message(message):
    markup_st = telebot.types.ReplyKeyboardMarkup()
    it_1 = telebot.types.KeyboardButton("/get_users")
    it_2 = telebot.types.KeyboardButton("/lottery10")
    it_3 = telebot.types.KeyboardButton("/lottery25")
    it_4 = telebot.types.KeyboardButton("/lottery50")
    it_5 = telebot.types.KeyboardButton("/write_comment")
    it_6 = telebot.types.KeyboardButton("/ban_user")
    markup_st.row(it_1, it_2, it_3)
    markup_st.row(it_4, it_5, it_6)

    if message.text == '/start' and message.chat.id in admins:
        for id in admins:
            bot.send_message(id, "Список команд для админа.", reply_markup=markup_st)

    bot.send_message(message.chat.id,"Привет ✌️ это бот где регулярно будут проходить розыгриши! Мы уже тебя зарегестрировали. В каждом розыгрыше вы получите свой номер. Удачи🎉",)
    if message.chat.id not in id_users_only:
        users.append(f"{message.chat.id} - @{message.from_user.username}")
        id_users_only.append(message.chat.id)


@bot.message_handler(commands=["get_users"])
def get_users(message):
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "\n".join(users))
    print(users)

@bot.message_handler(commands=["write_comment"])
def admin_message(message):
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "Напишите комментарий.")
        bot.register_next_step_handler(message, write_comment)


def write_comment(message):
    for id in id_users_only:
        bot.send_message(id, message.text)

@bot.message_handler(commands=["ban_user"])
def ban_user(message):
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "Напишите id человека которого хотите забанить.")
        ban_users.append(message.text)



@bot.message_handler(func=lambda message: message.text.startswith("/lottery"), content_types=["text"])
def admin_comands(message):
    global count_of_users
    if message.text == "/lottery10" and message.chat.id in admins:
        count_of_users = 3

    elif message.text == "/lottery25" and message.chat.id in admins:
        count_of_users = 25

    elif message.text == "/lottery50" and message.chat.id in admins:
        count_of_users = 50

    start_lottery(message)


def start_lottery(message):
    for id in id_users_only:
        bot.send_message(id, f"Напиши go чтобы участвовать. Всего мест {str(count_of_users)}. Если вы победили, бот оповестит вас.",)


#  bot.register_next_step_handler(message, lottery)


@bot.message_handler(func=lambda message: message.text.startswith("go"), content_types=["text"])
def lottery(message):
    global stop_adding, winner_id, count_of_users, start_or_wait

    if (
        message.text == "go"
        and message.chat.id not in admins
        and stop_adding < count_of_users
        and count_of_users != 0
        and message.chat.id not in users_for_lottery
        and message.chat.id not in ban_users
    ):
        stop_adding += 1
        users_for_lottery.append(message.chat.id)
        user_numbers[message.chat.id] = stop_adding
        bot.send_message(message.chat.id, f"Вы учавствуете в розыгрыше! Ваш номер {stop_adding}.")

    if message.text == "go" and message.chat.id in admins:
        start_or_wait = True
        bot.send_message(message.chat.id, "Места закончились!")
        winner_id = random.choice(users_for_lottery)
        time.sleep(10)
        for id in id_users_only:
            bot.send_message(id, f"Победил человек с номером {user_numbers[winner_id]}🎉")


        bot.send_message(winner_id, f"Поздравляю вы выиграли 🥳 скоро вам напишет создатель этого бота.",)
        bot.send_message(7123855395, f"{winner_id}-{user_numbers[winner_id]}")
        stop_adding = 0
        count_of_users = 0
        users_for_lottery.clear()

    elif message.text == "go" and stop_adding == 0:
        bot.send_message(message.chat.id, "Розыгрыш ещё не начался!")

    else:
        bot.send_message(message.chat.id, "Ты уже участвуешь!")

    if ( 
        stop_adding == count_of_users 
        and stop_adding != 0 
        and count_of_users != 0 
        and start_or_wait == False
    ):
        bot.send_message(message.chat.id, "Места закончились!")
        winner_id = random.choice(users_for_lottery)
        time.sleep(10)
        for id in id_users_only:
            bot.send_message(id, f"Победил человек с номером {user_numbers[winner_id]}🎉")

        bot.send_message(winner_id, f"Поздравляю вы выиграли 🥳 скоро вам напишет создатель этого бота.",)
        bot.send_message(7123855395, f"{winner_id}-{user_numbers[winner_id]}")
        stop_adding = 0
        count_of_users = 0
        users_for_lottery.clear()

    print(user_numbers)


bot.infinity_polling()
