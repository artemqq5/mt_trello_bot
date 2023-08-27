from telebot import types


def creative_task_type_gambling():
    markup = types.InlineKeyboardMarkup()

    list_buttons = (
        types.InlineKeyboardButton('Новий', callback_data='gambling_new'),
        types.InlineKeyboardButton('Адаптив', callback_data='gambling_adaptive'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup
