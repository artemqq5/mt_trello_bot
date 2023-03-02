from telebot import types


# ===============Gambling FB======================
def gambling_fb_menu():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Расшарить прилу 📲', callback_data="share_app"),
        types.InlineKeyboardButton('Создать кампанию 🔖', callback_data="create_campaign"),
        types.InlineKeyboardButton('PWA прила 💣', callback_data="pwa_app"),
        types.InlineKeyboardButton('Заказать Креатив 🪄', callback_data="order_creative"),
        types.InlineKeyboardButton('Другое задание 💻', callback_data="other_task"),
    )

    for i in listButtons:
        markup.add(i)

    return markup

# ===============Gambling FB end======================
