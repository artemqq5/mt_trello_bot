NOT_REGISTERED_USER = "⛔ Ви не зареєстровані, пишіть адміну"
NOT_ACCESS = "У вас немає доступу, напишіть адміну"
ERROR_OPERATION = "Помилка"

INPUT_USER_ADD = "Введіть користувача формат id name dep :"
INPUT_USER_ADD_ERROR = "Помилка вводу. Використовуйте формат id name dep /add_user"
INPUT_USER_ID = "Введіть ID користувача :"
USER_ALREADY_HAVE = "Користувач вже в базі"
USER_ADDED = "Користувач доданий"
USER_ADD_ERROR = "Невдалося додати користувача"
USER_DELETED = "Користувача видалено"
HAVE_NOT_DEP = "Такого dep немає. Використовуйте один з"
ERROR_DELETE_USER = "Не вдалося видалити користувача, напишіть адміну"
USER_HAVE_NOT_IN_DB = "Такого користувача немає в базі"

MAIL_TO_ALL = "Введіть повідомлення для розсилки всім користувачам:"

MESSAGE_SEND = "✅ Задание отправленно!"
MESSAGE_DONT_SEND = "Не вийшло надіслати завдання"
MESSAGE_UP_TO_100 = "Введіть рядок до 100 символів"

TIME_CHOICE = "Введіть дедлайн завдання у форматі\nРІК-МІСЯЦЬ-ЧИСЛО ГОДИНИ:ХВИЛИНИ\nНаприклад 2023-02-24 04:00"
WRONG_TIME_CHOICE = "Неправильный формат, введите в формате\nРІК-МІСЯЦЬ-ЧИСЛО ГОДИНИ:ХВИЛИНИ\nНаприклад 2023-02-24 04:00"
SKIP = "Пропустити"

HAVE_NOT_ACCESS_CALL_ADMINS = "Немає доступу, запитайте у адмінів"

# @bot.message_handler(commands=['load'])
# async def load_arhive_to_trello_test(message):
#     global user_state["state"
#     user_state["state" = "load_file"
#     await bot.send_message(message.chat.id, 'Киньте архів з фалами для завантаження у таск', reply_markup=skip_desc())
#
#
# @bot.message_handler(func=lambda m: user_state["state" in ("load_file",), content_types=['document'])
# async def load_arhive_to_trello_test_handler(message):
#     global user_state["state"
#     try:
#         file_info = await bot.get_file(message.document.file_id)
#         file_url = f"https://api.telegram.org/file/bot{local_telegram_token}/{file_info.file_path}"
#         file_content = requests.get(file_url).content
#
#         trello_url = f"https://api.trello.com/1/cards/64a6a5a758d2aaeb9d64d2b4/attachments?key={local_api_key_trello}&token={local_token_trello}"
#         response = requests.post(trello_url, files={"file": ("photos.zip", file_content, "application/zip")})
#
#         if response.status_code == 200:
#             await bot.reply_to(message, "Файл успішно завантажено до Trello!")
#         else:
#             await bot.reply_to(message, "Помилка при завантаженні файлу до Trello.")
#
#         set_state_none()
#     except Exception as e:
#         await bot.reply_to(message, e)