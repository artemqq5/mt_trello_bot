from telebot import types


# ===============Gambling FB======================
def gambling_fb_menu():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Розшарити прілу 📲', callback_data="share_app"),
        types.InlineKeyboardButton('Створити кампанію 🔖', callback_data="create_campaign"),
        types.InlineKeyboardButton('PWA пріла 💣', callback_data="pwa_app"),
        types.InlineKeyboardButton('Замовити Креатив 🪄', callback_data="order_creative"),
        types.InlineKeyboardButton('Інше завдання 💻', callback_data="other_task"),
    )

    for i in listButtons:
        markup.add(i)

    return markup

# ===============Gambling FB end======================
