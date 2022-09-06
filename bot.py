import telebot
import sqlite3
from telebot import types
import texts
from db import Database
import time
import conf

bot = telebot.TeleBot(conf.Token)

db = Database('database.db')

@bot.message_handler(commands = ['start'])
def first(message):
    if message.chat.type == 'private':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        item_one = types.InlineKeyboardButton(text='1. Получить полезную информацию', callback_data='1.')
        item_two = types.InlineKeyboardButton(text='2. Условия получения бонуса', callback_data='2.')
        item_three = types.InlineKeyboardButton(text='3. У меня возникли вопросы/проблемы', callback_data='3.')

        markup_inline.add(item_one, item_two, item_three)
        bot.send_message(message.chat.id, 'Привет, {0.first_name}!\n\n'.format(message.from_user) + texts.Texts['text1'],
            reply_markup=markup_inline
        )

        if not db.user_exists(message.chat.id):
            db.add_user(message.chat.id)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == '1.':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)

        item_info = types.InlineKeyboardButton(text='Вся полезная информация', url='https://taplink.cc/timmy_toys',  callback_data='infor')
        item_return = types.InlineKeyboardButton(text='Вернуться к начальному сообщению', callback_data='return')
        markup_inline.add(item_info, item_return)
        bot.send_message(call.message.chat.id, texts.Texts['text2'],
            reply_markup=markup_inline
        )
        bot.answer_callback_query(callback_query_id=call.id)
    elif call.data == '2.':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)

        item_special = types.InlineKeyboardButton(text='Оставить отзыв', url='https://www.wildberries.ru/lk/myorders/archive', callback_data='special')
        item_ready = types.InlineKeyboardButton(text='Я оставил(-а) отзыв', callback_data='ready')
        item_return = types.InlineKeyboardButton(text='Вернуться к начальному сообщению', callback_data='return')
        file = open('instr.png', 'rb')
        markup_inline.add(item_special, item_ready, item_return)
        bot.send_photo(call.message.chat.id, file, texts.Texts['text3'],
            reply_markup=markup_inline
        )
        bot.answer_callback_query(callback_query_id=call.id)
    elif call.data == '3.':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)

        item_help = types.InlineKeyboardButton(text='Задать вопросы', url='https://t.me/svetik_0688', callback_data='help')
        item_return = types.InlineKeyboardButton(text='Вернуться к начальному сообщению', callback_data='return')
        markup_inline.add(item_help, item_return)
        bot.send_message(call.message.chat.id, texts.Texts['text4'],
            reply_markup=markup_inline
        )
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data == 'ready':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)

        item_screen = types.InlineKeyboardButton(text='Получить бонус', url='https://t.me/svetik_0688', callback_data='screen')
        item_return = types.InlineKeyboardButton(text='Вернуться к начальному сообщению', callback_data='return')
        markup_inline.add(item_screen, item_return)
        bot.send_message(call.message.chat.id, texts.Texts['text5'],
            reply_markup=markup_inline
        )
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data == 'return':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        item_one = types.InlineKeyboardButton(text='1. Получить полезную информацию', callback_data='1.')
        item_two = types.InlineKeyboardButton(text='2. Условия получения бонуса', callback_data='2.')
        item_three = types.InlineKeyboardButton(text='3. У меня возникли вопросы/проблемы', callback_data='3.')

        markup_inline.add(item_one, item_two, item_three)
        bot.send_message(call.message.chat.id, 'Привет!\n\n'.format(call.message.from_user) + texts.Texts['text1'],
            reply_markup=markup_inline
        )
        bot.answer_callback_query(callback_query_id=call.id)

@bot.message_handler(commands=['notify'])
def notify_everyone(message: types.Message):
        if message.from_user.id == 1189827209:
            text = message.text[8:]
            users = db.get_users()
            counter = 0
            count = 0
            for row in users:
                try:
                    bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                    counter += 1
                    if counter >= 30:
                        time.sleep(1.5)
                        counter *= 0
                    count += 1
                except:
                    db.set_active(row[0], 0)
            bot.send_message(message.from_user.id, f"Сообщение успешно доставлено {count} пользователям.")
            if count >= 1:
                count *= 0
            else:
                pass


bot.polling(none_stop = True, interval=0)