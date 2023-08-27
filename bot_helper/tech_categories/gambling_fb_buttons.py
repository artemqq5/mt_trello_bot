from telebot import types


# ===============Gambling FB======================
def gambling_fb_menu():
    markup = types.InlineKeyboardMarkup()

    list_buttons = (
        types.InlineKeyboardButton('Розшарити прілу 📲', callback_data="share_app"),
        types.InlineKeyboardButton('Створити кампанію 🔖', callback_data="create_campaign"),
        types.InlineKeyboardButton('PWA пріла 💣', callback_data="pwa_app"),
        types.InlineKeyboardButton('Інше завдання 💻', callback_data="other_task"),
    )

    for i in list_buttons:
        markup.add(i)

    return markup

# ===============Gambling FB end======================
