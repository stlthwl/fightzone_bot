import telebot
import config
from telebot import types


bot = telebot.TeleBot(config.token)
name = ''
phone = ''


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Цены', 'Записаться')
    markup.row('Расписание', 'Контакты')
    bot.send_message(message.chat.id, 'fight⚡zone_dme')
    bot.send_message(message.chat.id, 'Выбери раздел, '
                                      'пользуясь подсказками ниже👇🏻', reply_markup=markup)
    bot.register_next_step_handler(message, menu)


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup()
    if message.text == 'Цены':
        markup.row('Назад')
        bot.send_message(message.chat.id, 'Бокс (4+):\n'
                                          'Разовое посещение - 500₽\n'
                                          '4 занятия - 1800₽\n'
                                          '6 занятий - 2400₽\n'
                                          '8 занятий - 3000₽\n'
                                          '12 занятий - 4000₽\n'
                                          'Пробное занятие - БЕСПЛАТНО\n\n', reply_markup=markup)
        bot.register_next_step_handler(message, start)
    elif message.text == 'Записаться':
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Введите имя', reply_markup=markup)
        bot.register_next_step_handler(msg, reg_name)
    elif message.text == 'Расписание':
        markup.row('Назад')
        bot.send_message(message.chat.id, 'Бокс:\n'
                                          'Пн, Ср, Пт\n'
                                          '09:00-10:30\n'
                                          '19:30-21:00\n'
                                          '21:00-22:30\n'
                                          'Сб\n'
                                          '10:00-11:30\n\n', reply_markup=markup)
        bot.send_message(message.chat.id, 'Бокс (Дети):\n'
                                          'Пн, Ср, Пт\n'
                                          '16:00-17:00 (4+)\n'
                                          '17:00-18:00 (6+)\n'
                                          '19:00-20:30 (10+)\n'
                                          'Сб\n'
                                          '10:00-11:30\n\n', reply_markup=markup)
        bot.register_next_step_handler(message, start)
    elif message.text == 'Контакты':
        markup.row('Назад')
        address_btn = types.InlineKeyboardButton(text='Домодедово, Каширское шоссе, д. 1',
                                                url='https://yandex.ru/maps/10725/domodedovo/house/kashirskoye_shosse_1'
                                                    '/Z04YcQFhTU0FQFtvfXh0cnVmZg==/?indoorLevel=1&ll=37.761482%2C55.453'
                                                    '952&utm_source=main_stripe_big&z=16.63')
        instagram_btn = types.InlineKeyboardButton(text='@fight_zone_dme',
                                                   url='https://instagram.com/fight_zone_dme?utm_medium=copy_link')
        site_btn = types.InlineKeyboardButton(text='Наш сайт',
                                              url='https://fightzone-dme.ru/')
        whatsapp_btn = types.InlineKeyboardButton(text='WhatsApp: +7 (926) 139 72 22',
                                                  url='https://wa.me/79261397222')
        keyboard.add(address_btn)
        keyboard.add(instagram_btn)
        keyboard.add(site_btn)
        keyboard.add(whatsapp_btn)
        bot.send_message(message.chat.id, 'Связь с нами:', reply_markup=keyboard)
        bot.send_message(message.chat.id, '📞', reply_markup=markup)
        bot.register_next_step_handler(message, start)
    else:
        markup.row('В начало')
        bot.send_message(message.chat.id, 'Для продолжения воспользуйся встроенной клавиатурой👇🏻', reply_markup=markup)
        bot.register_next_step_handler(message, start)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите номер Вашего телефона')
    bot.register_next_step_handler(message, reg_phone)


def reg_phone(message):
    global phone
    phone = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    confirm = 'Имя: ' + str(name) + '\nТелефон: ' + str(phone)
    bot.send_message(message.from_user.id, text=confirm, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if call.data == "yes":
        global name
        global phone
        markup.row('Назад')
        confirm = 'Новая запись!\n' + 'Имя: ' + str(name) + '\nТелефон: ' + str(phone)
        msg = bot.send_message(call.message.chat.id, 'Заявка успешно отправлена!\n'
                                                     'Мы скоро вам перезвоним.', reply_markup=markup)
        bot.send_message(chat_id=config.id_tg_group, text=confirm)
        bot.register_next_step_handler(msg, start)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Повторите попытку\nВведите имя')
        bot.register_next_step_handler(call.message, reg_name)


bot.polling(none_stop=True)