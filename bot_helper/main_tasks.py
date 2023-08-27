from telebot import types

# close markup
close_markup = types.ReplyKeyboardRemove(selective=False)


def set_start_button():
    markup = types.ReplyKeyboardMarkup()

    list_buttons = (
        types.KeyboardButton('My Tasks 📋'),
        types.KeyboardButton('Creo'),
        types.KeyboardButton('Tech'),
    )

    for i in list_buttons:
        markup.add(i)

    return markup


def my_tasks_menu():
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton('tech', callback_data="my_task_tech"),
        types.InlineKeyboardButton('creo', callback_data="my_task_creo")
    )

    return markup


def manage_card():
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton('Видалити завдання', callback_data="delete_card"),
        types.InlineKeyboardButton('Написати коментар', callback_data="commend_card")
    )

    return markup


def choice_date():
    markup = types.ReplyKeyboardMarkup()

    markup.add(types.KeyboardButton('Пропустити'))

    markup.row(
        types.KeyboardButton('Завтра 12:00'),
        types.KeyboardButton('Завтра 15:00'),
        types.KeyboardButton('Завтра 18:00'),
    )

    return markup


def skip_desc():
    return types.ReplyKeyboardMarkup().add(types.KeyboardButton("Пропустити"))


def yes_no():
    return types.ReplyKeyboardMarkup().row(types.KeyboardButton('Так'), types.KeyboardButton('Ні'))
