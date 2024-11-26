# Навигационные кнопки
BACK = ⬅️ Назад
SKIP = ⏭️ Пропустить

# Сообщения о доступе
ACCESS_DENIED = 🚫 Доступ не предоставлен. Напишите администратору для получения доступа.

# get user id
GET_USER_ID = Ваш Telegram ID (<code>{$telegram_id}</code>)

# Приветствие
START = 👋 Привет, выберите тип задания
START_ADMIN = 👋 Привет, вы администратор, у вас полный доступ
START_SPECIAL = 👋 Привет, у тебя есть только функционал push-уведомлений

# Задания
MY_TASK = 📝 Мои задания
TASK_CREO = 🎨 Креатив
TASK_TECH = 🛠️ Техзадание
TASK_AFF = 🤝 Партнерка

# admin menu
ADMIN-ADD = ➕ Добавить
ADMIN-DELETE = 🔻 Удалить
ADMIN-MAILING = 📩 Рассылка
ADMIN-USERS = 👨‍👩‍👦 Пользователи

# Добавить пользователя
ADMIN-ADD_USER-NAME = Введите имя пользователя:
ADMIN-ADD_USER-TELEGRAM_ID = Введите Telegram ID пользователя. Пользователь, которого нужно добавить, может узнать свой ID, введя команду /get_id в этом же боте:
ADMIN-ADD_USER-ROLE = Выберите роль пользователя:
ADMIN-ADD_USER-TDS_ID = Введите TDS ID пользователя:
ADMIN-USER_ALREADY_EXIST = ⚠️ Пользователь уже есть в базе
ADMIN-USER_ADD_SUCCESS = ✅ Пользователь добавлен
ADMIN-USER_ADD_FAIL = ❌ Не удалось добавить пользователя

# Удалить пользователя
ADMIN-DELETE_USER = Введите ID пользователя:
ADMIN-USER_NO_EXIST = ⚠️ Такого пользователя нет в базе
ADMIN-DELETE_USER_SUCCESS = ✅ Пользователь успешно удален
ADMIN-DELETE_USER_FAIL = ❌ Не удалось удалить пользователя

# Информация о пользователе
ADMIN-GET_USER_INFO = <b>📋 Телеграм ID:</b> <code>{$tg}</code>
    <b>Имя:</b> {$nickname}
    <b>Телеграм имя:</b> {$firstname}
    <b>Юзернейм:</b> {$username}
    <b>Роль:</b> {$dep}
    <b>TDS ID:</b> <code>{$tds}</code>

# Рассылка
ADMIN-INPUT_TEXT_MAILING = Введите текст для рассылки:
ADMIN-RESULT_NOTIFICATION = <b>-📊 Результат рассылки-</b>

    Получили сообщение: {$send}\{$users}
    Заблокировали бота: {$block}
    Другое: {$other}

# Дедлайн
DEADLINE = ⏰ Ориентировочный дедлайн:

    Например, <b>17:00 26.09.24</b>
DEADLINE_ERROR = ❌ Неправильный формат, проверьте на наличие лишних пробелов, введите в формате
    ЧАСЫ:МИНУТЫ ДЕНЬ.МЕСЯЦ.ГОД

    Например, <b>17:00 26.09.24</b>

# Создание задания
ERROR_CREATE_CARD = ❌ Ошибка при создании карточки
TASK_SEND_SUCCESS = ✅ Задание успешно отправлено
