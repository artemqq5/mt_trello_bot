from telebot import types


# ===============Media======================
def media_menu():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Замовити Креатив 🪄', callback_data="order_creative"))

    return markup

# ===============Media end======================
