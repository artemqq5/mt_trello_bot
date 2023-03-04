from telebot import types


# ===============Gambling PPC end======================
def gambling_ppc_menu():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Подготовить вайт 🎁', callback_data="prepare_vait"),  # one
        types.InlineKeyboardButton('Настроить клоаку 📡', callback_data="setting_cloak"),  # one
        types.InlineKeyboardButton('Припарковать домен 🅿️', callback_data="set_domain"),  # one
        types.InlineKeyboardButton('Создать кампанию 🔖', callback_data="create_campaign"),
        types.InlineKeyboardButton('Заказать Креатив 🪄', callback_data="order_creative"),
        types.InlineKeyboardButton('Другое задание 💻', callback_data="other_task"),
    )

    for i in listButtons:
        markup.add(i)

    return markup
# ===============Gambling PPC end======================
