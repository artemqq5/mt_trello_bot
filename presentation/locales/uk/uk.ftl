# Кнопки навігації
BACK = ⬅️ Назад
SKIP = ⏭️ Пропустити

# Повідомлення про доступ
ACCESS_DENIED = 🚫 Доступ не видано. Напишіть адміну для отримання доступу.

# get user id
GET_USER_ID = Ваш Telegram ID (<code>{$telegram_id}</code>)

# Привітання
START = 👋 Привіт, оберіть тип завдання
START_ADMIN = 👋 Привіт, Ви адміністратор, у вас повний доступ
START_SPECIAL = 👋 Привіт, у тебе з функціоналу лише push-повідомлення

# Завдання
MY_TASK = 📝 Мої завдання
TASK_CREO = 🎨 Крео
TASK_TECH = 🛠️ Технічка
TASK_AFF = 🤝 Аффілейт

# admin menu
ADMIN-ADD = ➕ Додати
ADMIN-DELETE = 🔻 Видалити
ADMIN-MAILING = 📩 Розсилка
ADMIN-USERS = 👨‍👩‍👦 Користувачі

# Додати користувача
ADMIN-ADD_USER-NAME = Введіть ім'я користувача:
ADMIN-ADD_USER-TELEGRAM_ID = Введіть Telegram ID користувача. Користувач, якого потрібно додати, може дізнатися своє ID ввівши команду /get_id в цьому ж боті:
ADMIN-ADD_USER-ROLE = Оберіть роль користувача:
ADMIN-ADD_USER-TDS_ID = Введіть TDS ID користувача:
ADMIN-ADD_USER-ALREADY_EXIST = ⚠️ Користувач вже є в базі
ADMIN-ADD_USER-SUCCESS = ✅ Користувач доданий
ADMIN-ADD_USER-FAIL = ❌ Невдалося додати користувача
ADMIN-ADD_USER-ERROR_SYMBOLS = Забагато символів, вкладись у 255

# Видалити користувача
ADMIN-DELETE_USER = Введіть ID користувача :
ADMIN-USER_NO_EXIST = ⚠️ Такого користувача немає в базі
ADMIN-DELETE_USER_SUCCESS = ✅ Користувача видалено
ADMIN-DELETE_USER_FAIL = ❌ Не вдалося видалити користувача

# Інформація про користувача
ADMIN-GET_USER_INFO = <b>📋 Телеграм ID:</b> <code>{$tg}</code>
    <b>Ім'я:</b> {$nickname}
    <b>Телеграм ім'я:</b> {$firstname}
    <b>Юзернейм:</b> {$username}
    <b>Роль:</b> {$dep}
    <b>TDS ID:</b> <code>{$tds}</code>

# Розсилка
ADMIN-INPUT_TEXT_MAILING = Введіть текст для розсилки:
ADMIN-RESULT_NOTIFICATION = <b>-📊 Результат розсилки-</b>

    Отримали повідомлення: {$send}\{$users}
    Заблокували бота: {$block}
    Інше: {$other}

# Дедлайн
DEADLINE = ⏰ Орієнтовний дедлайн:

    Наприклад <b>17:00 26.09.24</b>
DEADLINE_ERROR = ❌ Неправильний формат, перевірте на наявність зайвих пробілів, введіть у форматі
    ГОДИНИ:ХВИЛИНИ ЧИСЛО.МІСЯЦЬ.РІК

    Наприклад <b>17:00 26.09.24</b>

# Створення завдання
ERROR_CREATE_CARD = ❌ Помилка при створенні картки
TASK_SEND_SUCCESS = ✅ Завдання успішно надіслано
