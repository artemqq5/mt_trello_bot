from telebot import types


# ===============Media======================
def media_menu():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Замовити Креатив 🪄', callback_data="order_creative"))
    markup.add(types.InlineKeyboardButton('Інше 🪄', callback_data="other_media"))

    return markup

# ===============Media end======================
