from telebot import types


# def media_menu():
#     markup = types.InlineKeyboardMarkup()
#
#     markup.add(types.InlineKeyboardButton('Замовити Креатив 🪄', callback_data="order_creative"))
#     markup.add(types.InlineKeyboardButton('Інше 🖌', callback_data="other_media"))
#
#     return markup


def creative_task_type_media():
    markup = types.InlineKeyboardMarkup()

    list_buttons = (
        types.InlineKeyboardButton('Новий', callback_data='media_other_new'),
        types.InlineKeyboardButton('Адаптив', callback_data='media_other_adaptive'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup


def choice_source_media():
    markup = types.ReplyKeyboardMarkup()

    markup.row(
        types.KeyboardButton('Instagram'),
        types.KeyboardButton('Linkedin'),
        types.KeyboardButton('MT Shop'),
        types.KeyboardButton('Інше'),
    )

    return markup


def account_or_app_media():
    markup = types.ReplyKeyboardMarkup()

    markup.row(
        types.KeyboardButton('Аккаунт'),
        types.KeyboardButton('Додаток'),
    )

    return markup
