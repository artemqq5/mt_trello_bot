import asyncio
import datetime

from telebot.async_telebot import AsyncTeleBot

from bot_commands.admin_commands import *
from bot_commands.creo.creo_crypto_cmd import order_crypto_creative
from bot_commands.creo.creo_gambling_cmd import order_gambling_creative, order_gambling_creative_adaptive
from bot_commands.creo.creo_media_cmd import order_media_creative
from bot_commands.tech.add_offer_cmd import add_offer_cmd
from bot_commands.tech.create_campaign_cmd import create_campaign_cmd
from bot_commands.tech.create_pwa_cmd import create_pwa_cmd
from bot_commands.tech.edit_offer_cmd import edit_offer_cmd
from bot_commands.tech.mt_partners_cmd import mt_partners_cmd
from bot_commands.tech.other_task_cmd import other_task_cmd
from bot_commands.tech.prepare_vait_cmd import prepare_vait_cmd
from bot_commands.tech.set_domain_cmd import set_domain_cmd
from bot_commands.tech.setting_cloak_cmd import setting_cloak_cmd
from bot_commands.tech.share_app_cmd import share_app_cmd
from bot_commands.trello_mng.add_comment_cmd import add_comment_cmd
from bot_helper.creo_categories.crypto_creo import creative_task_type_crypto
from bot_helper.creo_categories.gambling_creo import creative_task_type_gambling
from bot_helper.creo_categories.media_other import choice_source_media, account_or_app_media, creative_task_type_media
from bot_helper.creo_tasks import creative_task_mode
from bot_helper.tech_categories.af_manager_buttons import af_manager_menu, choice_offer_type
from bot_helper.tech_categories.gambling_fb_buttons import gambling_fb_menu
from bot_helper.tech_categories.gambling_ppc_buttons import gambling_ppc_menu
from bot_helper.tech_categories.gambling_uac_buttons import gambling_uac_menu
from bot_helper.tech_categories.masons_partners import masons_partners_menu
from bot_helper.tech_tasks import tech_task_mode
from models.task_form import task_step, model_task_list, set_task_step, reset_task_list
from private_config import local_telegram_token, server_telegram_token
from bot_helper.main_tasks import *

# bot settings
if DEBUG_MODE:
    bot = AsyncTeleBot(local_telegram_token)
else:
    bot = AsyncTeleBot(server_telegram_token)


# send start text for user COMMAND
@bot.message_handler(commands=['start'])
async def start_message(message):
    set_state_none()  # reset user state
    #
    # await bot.set_my_commands(
    #     commands=[
    #         BotCommand("/start", "Меню"),
    #         BotCommand("/add_user", "Додати користувача"),
    #         BotCommand("/delete_user", "Видалити користувача"),
    #         BotCommand("/mailing_all", "Розсилка всім"),
    #         BotCommand("/get_all", "Показати всіх користувачів")])

    if get_user_db(message.chat.id).result is not None:
        await bot.send_message(message.chat.id, 'Меню', reply_markup=set_start_button())
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


# management user (add, delete, mailing)
@bot.message_handler(commands=['add_user', 'delete_user', 'mailing_all'])
async def menu_(message):
    set_state_none()  # reset user state

    if get_user_db(message.chat.id).result is not None:
        if get_user_db(message.chat.id).result.dep_user in ("admin", "designer", "tech"):
            if message.text == '/add_user':
                user_state["state"] = "add_user"
                await bot.send_message(message.chat.id, INPUT_USER_ADD, reply_markup=close_markup)
            elif message.text == '/delete_user':
                user_state["state"] = "delete_user"
                await bot.send_message(message.chat.id, INPUT_USER_ID, reply_markup=close_markup)
            elif message.text == '/mailing_all':
                user_state["state"] = "mailing_all"
                await bot.send_message(message.chat.id, MAIL_TO_ALL, reply_markup=close_markup)
        else:
            await bot.send_message(message.chat.id, NOT_ACCESS, reply_markup=close_markup)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(commands=['get_all'])
async def get_all(message):
    if get_user_db(message.chat.id).result is not None:
        if get_user_db(message.chat.id).result.dep_user in ("admin", "designer", "tech"):
            await get_all_command(message, bot)
        else:
            await bot.send_message(message.chat.id, NOT_ACCESS, reply_markup=close_markup)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)

    # reset user state
    set_state_none()


@bot.message_handler(func=lambda m: user_state["state"] in ("admin", "designer", "tech"))
async def add_user(message):
    if get_user_db(message.chat.id).result is not None:
        await add_user_command(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)

    # reset user state
    set_state_none()


@bot.message_handler(func=lambda m: user_state["state"] in ("admin", "designer", "tech"))
async def delete_user(message):
    if get_user_db(message.chat.id).result is not None:
        # delete user from bot
        await delete_user_command(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] in ("admin", "designer", "tech"))
async def user_mailing(message):
    if get_user_db(message.chat.id).result is not None:
        await mailing_all_command(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)

    # reset user_state
    set_state_none()


@bot.message_handler(
    func=lambda m: m.text in (
            "My Tasks 📋", "Creo", "Tech"))
async def choice_category(message):
    set_state_none()  # reset user state

    if get_user_db(message.chat.id).result is not None:
        match message.text:
            case "My Tasks 📋":
                await bot.send_message(message.chat.id, message.text + " : ", reply_markup=my_tasks_menu())
            case "Creo":
                await bot.send_message(
                    message.chat.id,
                    "Тепер оберіть підкатегорію відділу Creo",
                    reply_markup=creative_task_mode())
            case "Tech":
                await bot.send_message(
                    message.chat.id,
                    "Тепер оберіть підкатегорію відділу Tech",
                    reply_markup=tech_task_mode())
            case _:
                await bot.reply_to(message, "(У розробці)")
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(
    func=lambda m: m.text in (
            "Gambling FB", "Gambling PPC", "Gambling UAC", "AF Manager", "Masons Partners"))
async def choice_subcategory_tech(message):
    set_state_none()  # reset user state

    if get_user_db(message.chat.id).result is not None:
        match message.text:
            case "AF Manager":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=af_manager_menu())
            case "Gambling FB":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_fb_menu())
            case "Gambling PPC":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_ppc_menu())
            case "Gambling UAC":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=gambling_uac_menu())
            case "Masons Partners":
                await bot.send_message(message.chat.id, message.text + " : ", reply_markup=masons_partners_menu())
            case _:
                await bot.reply_to(message, "(У розробці)")
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(
    func=lambda m: m.text in (
            "Gambling Creo", "Crypto Creo", "Media or Other"))
async def choice_subcategory_creo(message):
    set_state_none()  # reset user state

    if get_user_db(message.chat.id).result is not None:
        match message.text:
            case "Gambling Creo":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=creative_task_type_gambling())
            case "Crypto Creo":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=creative_task_type_crypto())
            case "Media or Other":
                await bot.send_message(message.chat.id, message.text + ": ", reply_markup=creative_task_type_media())
            case _:
                await bot.reply_to(message, "(У розробці)")
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "add_offer")
async def offer_add(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100:
            await add_offer_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "edit_offer")
async def offer_edit(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100:
            await edit_offer_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "order_creative_crypto")
async def order_creative_crypto(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (2, 3):
            await order_crypto_creative(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "order_creative_gamble")
async def order_creative_gamble(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (3, 4, 12, 13, 14):
            if model_task_list["type_creo"] == "Новий":
                await order_gambling_creative(message, bot)
            else:
                await order_gambling_creative_adaptive(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "order_creative_media")
async def order_creative_media(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] in (2, 3):
            await order_media_creative(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "share_app")
async def share_app(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            await share_app_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "other_task")
async def other_task(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 1:
            await other_task_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "pwa_app")
async def pwa_(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100 or task_step["step"] == 2:
            await create_pwa_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "create_campaign")
async def create_campaign(message):
    if get_user_db(message.chat.id).result is not None:
        if len(message.text) < 100:
            await create_campaign_cmd(message, bot)
        else:
            await bot.reply_to(message, MESSAGE_UP_TO_100)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "set_domain")
async def set_domain(message):
    if get_user_db(message.chat.id).result is not None:
        await set_domain_cmd(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "setting_cloak")
async def setting_cloak(message):
    if get_user_db(message.chat.id).result is not None:
        await setting_cloak_cmd(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "prepare_vait")
async def prepare_vait(message):
    if get_user_db(message.chat.id).result is not None:
        await prepare_vait_cmd(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "masons_partners")
async def masons_partners(message):
    if get_user_db(message.chat.id).result is not None:
        await mt_partners_cmd(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.message_handler(func=lambda m: user_state["state"] == "add_comment")
async def add_comment(message):
    if get_user_db(message.chat.id).result is not None:
        await add_comment_cmd(message, bot)
    else:
        await bot.send_message(message.chat.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in (
        "crypto_new", "crypto_adaptive", "gambling_new", "gambling_adaptive", "media_other_new",
        "media_other_adaptive"))
async def answer_creo(call):
    set_state_none()  # reset user state

    reset_task_list()

    current_user = get_user_db(call.from_user.id).result

    if current_user is not None:
        if current_user.dep_user in ("gambleppc", "gambleuac", "gamblefb", "admin", "gambleuac_gambleppc",
                                     "designer", "media"):
            match call.data:
                case "crypto_new" | "crypto_adaptive":
                    user_state["state"] = "order_creative_crypto"
                    model_task_list["type_creo"] = "Новий" if call.data == "crypto_new" else "Адаптив"

                    await bot.send_message(
                        call.from_user.id,
                        "Кількість : ",
                        reply_markup=close_markup)

                case "media_other_new" | "media_other_adaptive":
                    user_state["state"] = "order_creative_media"
                    model_task_list["type_creo"] = "Новий" if call.data == "media_other_new" else "Адаптив"

                    await bot.send_message(
                        call.from_user.id,
                        "Кількість : ",
                        reply_markup=close_markup)

                case "gambling_new" | "gambling_adaptive":
                    user_state["state"] = "order_creative_gamble"
                    model_task_list["type_creo"] = "Новий" if call.data == "gambling_new" else "Адаптив"

                    await bot.send_message(
                        call.from_user.id,
                        "Кількість : ",
                        reply_markup=close_markup)
        else:
            await bot.send_message(call.from_user.id, HAVE_NOT_ACCESS_CALL_ADMINS)

    else:
        await bot.send_message(call.from_user.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in (
        "edit_offer", "add_offer", "share_app", "other_task", "pwa_app", "create_campaign", "set_domain",
        "setting_cloak", "prepare_vait", "my_task_creo", "my_task_tech", "masons_partners"))
async def answer(call):
    set_state_none()  # reset user state

    reset_task_list()

    current_user = get_user_db(call.from_user.id).result

    if current_user is not None:
        match call.data:
            case "edit_offer":
                if current_user.dep_user in ("afmngr", "admin"):
                    user_state["state"] = "edit_offer"
                    await bot.send_message(
                        call.from_user.id,
                        "Id оффера у трекері : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "add_offer":
                if current_user.dep_user in ("afmngr", "admin"):
                    user_state["state"] = "add_offer"
                    await bot.send_message(
                        call.from_user.id,
                        "Новий рекламодавець чи існуючий?",
                        reply_markup=choice_offer_type()
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "share_app":
                if current_user.dep_user in ("gamblefb", "gambleuac", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "share_app"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть назву програми : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "other_task":
                if current_user.dep_user in ("gamblefb", "gambleuac", "gambleppc", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "other_task"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть коротку назву завдання : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "pwa_app":
                if current_user.dep_user in ("gamblefb", "gambleuac", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "pwa_app"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "create_campaign":
                if current_user.dep_user in ("gamblefb", "gambleuac", "gambleppc", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "create_campaign"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "set_domain":
                if current_user.dep_user in ("gambleppc", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "set_domain"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть назви доменів : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "setting_cloak":
                if current_user.dep_user in ("gambleppc", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "setting_cloak"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "prepare_vait":
                if current_user.dep_user in ("gambleppc", "admin", "gambleuac_gambleppc"):
                    user_state["state"] = "prepare_vait"

                    await bot.send_message(
                        call.from_user.id,
                        "Гео : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
            case "my_task_creo":
                creo_tasks = get_tasks(type="creo", userlabel=current_user.label_creo)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваші завдання creo : ", reply_markup=creo_tasks.markup)

            case "my_task_tech":
                creo_tasks = get_tasks(type="tech", userlabel=current_user.label_tech)
                if creo_tasks.markup is None:
                    await bot.send_message(call.from_user.id, creo_tasks.message)
                else:
                    await bot.send_message(call.from_user.id, "Ваші завдання tech : ", reply_markup=creo_tasks.markup)
            case "masons_partners":
                if current_user.dep_user in ("mt_partners", "admin"):
                    user_state["state"] = "masons_partners"

                    await bot.send_message(
                        call.from_user.id,
                        "Введіть назву для завдання : ",
                        reply_markup=close_markup
                    )
                else:
                    await bot.send_message(
                        call.from_user.id,
                        HAVE_NOT_ACCESS_CALL_ADMINS
                    )
    else:
        await bot.send_message(call.from_user.id, NOT_REGISTERED_USER, reply_markup=close_markup)


@bot.callback_query_handler(func=lambda call: call.data in get_callback_cards() + ["delete_card", "commend_card"])
async def answer_cards(call):
    set_state_none()  # reset user state

    match call.data:
        case "delete_card":
            try:
                if delete_card(id_card=model_task_list["current_card"]):
                    await bot.send_message(call.from_user.id, "✅ Завдання видалено з Trello")
                else:
                    await bot.send_message(call.from_user.id, "Помилка при видаленні")
            except:
                pass
        case "commend_card":
            user_state["state"] = "add_comment"

            await bot.send_message(
                call.from_user.id,
                "Введіть коментар : ",
                reply_markup=close_markup
            )
        case _:
            card = get_card(call.data.replace("card_", ""))
            model_task_list["current_card"] = card.id
            await bot.send_message(
                call.from_user.id,
                f"<b>{card.name}</b>\n{'=' * len(card.name)}\n{card.desc}",
                parse_mode="Html",
                reply_markup=manage_card()
            )


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
