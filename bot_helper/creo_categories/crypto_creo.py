from telebot import types


def creative_task_type_crypto():
    markup = types.InlineKeyboardMarkup()

    list_buttons = (
        types.InlineKeyboardButton('Новий', callback_data='crypto_new'),
        types.InlineKeyboardButton('Адаптив', callback_data='crypto_adaptive'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup
