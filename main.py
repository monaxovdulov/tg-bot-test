import telebot
import random
import time
import os

token= os.getenv('TELEGRAM_TOKEN') 
stop_adding = 0
bot=telebot.TeleBot(token)
admins= [7123855395]
users= []
id_users_only= []
user_numbers= {}
users_for_lottery= []
winner_id = None
count_of_users = 0


@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ это бот где регулярно будут проходить розыгриши! Мы уже тебя зарегестрировали. В каждом розыгрыше вы получите свой номер. Удачи🎉")
  users.append(f'{message.chat.id} - @{message.from_user.username}')
  id_users_only.append(message.chat.id)

@bot.message_handler(commands=['get_users'])
def get_users(message):
   bot.send_message(message.chat.id, '\n'.join(users))
   print(users)

@bot.message_handler(func=lambda message: message.text.startswith("/lottery"), content_types=['text'])
def admin_comands(message):
   global count_of_users
   if message.text == '/lottery10':
      count_of_users = 2

   elif message.text == '/lottery25':
      count_of_users = 25
         
   elif message.text == '/lottery50':
      count_of_users = 50

   start_lottery(message)


def start_lottery(message):     
    for id in id_users_only:
      bot.send_message(id, f"Напиши go чтобы участвовать. Всего мест {str(count_of_users)}. Если вы победили, бот оповестит вас.")
   #  bot.register_next_step_handler(message, lottery)

@bot.message_handler(func=lambda message: message.text.startswith("go"), content_types=['text'])
def lottery(message):
   global stop_adding, winner_id, count_of_users

   if message.text == 'go' and stop_adding < count_of_users and count_of_users != 0 and message.chat.id not in users_for_lottery:
      stop_adding += 1
      users_for_lottery.append(message.chat.id)
      user_numbers[message.chat.id] = stop_adding
      bot.send_message(message.chat.id, f"Вы учавствуете в розыгрыше! Ваш номер {stop_adding}.")
   
   elif message.text == 'go' and stop_adding == 0:
      bot.send_message(message.chat.id,"Розыгрыш ещё не начался!")

   else:
      bot.send_message(message.chat.id,"Ты уже участвуешь!")
    
   if stop_adding == count_of_users and stop_adding != 0 and count_of_users != 0:
      bot.send_message(message.chat.id, "Места закончились!")
      winner_id = random.choice(users_for_lottery)
      time.sleep(10)
      for id in id_users_only:
         bot.send_message(id, f"Победил человек с номером {user_numbers[winner_id]}🎉")
      bot.send_message(winner_id, f"Поздравляю вы выиграли 🥳 скоро вам напишет создатель этого бота.")
      bot.send_message(7123855395, f'{winner_id}-{user_numbers[winner_id]}')
      stop_adding = 0
      count_of_users = 0
      users_for_lottery.clear()


   print(user_numbers)


bot.infinity_polling()
