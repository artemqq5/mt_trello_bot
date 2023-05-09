from telebot import types


# ===============Gambling PPC end======================
def gambling_ppc_menu():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Підготувати вайт 🎁', callback_data="prepare_vait"),  # one
        types.InlineKeyboardButton('Налаштувати клоаку 📡', callback_data="setting_cloak"),  # one
        types.InlineKeyboardButton('Припаркувати домен 🅿️', callback_data="set_domain"),  # one
        types.InlineKeyboardButton('Створити кампанію 🔖', callback_data="create_campaign"),
        types.InlineKeyboardButton('Замовити Креатив 🪄', callback_data="order_creative"),
        types.InlineKeyboardButton('Інше завдання 💻', callback_data="other_task"),
    )

    for i in listButtons:
        markup.add(i)

    return markup
# ===============Gambling PPC end======================
