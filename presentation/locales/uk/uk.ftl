BACK = Назад
SKIP = Пропустити

ACCESS_DENIED = Доступ не видано. Напишіть адміну для отримання доступу

START = Привіт, оберіть тип завдання
START_ADMIN = Привіт, Ви адміністратор у вас повний доступ
START_SPECIAL = Привіт, у тебе з функціоналу лише push-повідомлення

MY_TASK = Мої завдання
TASK_CREO = Крео
TASK_TECH = Технічка
TASK_AFF = Оффер

# ADD USER
ADMIN-ADD_USER = Введіть користувача формат id name dep :
ADMIN-ADD_USER_ERROR_FORMAT = Неправильно! Використовуйте формат id name dep через пробіл, наприклад 66503250 Ігнат media
ADMIN-ADD_USER_ERROR_DEP = Вказаний вами dep відсутній. Оберіть з {$dep}
ADMIN-USER_ALREADY_EXIST = Користувач вже є в базі
ADMIN-USER_ADD_SUCCESS = Користувач доданий
ADMIN-USER_ADD_FAIL = Невдалося додати користувача

# DELETE USER
ADMIN-DELETE_USER = Введіть ID користувача :
ADMIN-USER_NO_EXIST = Такого користувача немає в базі
ADMIN-DELETE_USER_SUCCESS = Користувача видалено
ADMIN-DELETE_USER_FAIL = Не вдалося видалити користувача

# GET ALL
ADMIN-GET_USER_INFO = <b>Телеграм ID:</b> <code>{$tg}</code>
    <b>Видане ім'я:</b> {$nickname}
    <b>Телеграм ім'я:</b> {$firstname}
    <b>Юзернейм:</b> {$username}
    <b>Роль:</b> {$dep}

# MAILING ALL
ADMIN-INPUT_TEXT_MAILING = Введіть текст для розсилки:
ADMIN-RESULT_NOTIFICATION = <b>-Результат розсилки-</b>

    Отримали повідомлення: {$send}\{$users}
    Заблокували бота: {$block}
    Інше: {$other}

# DEAD LINE
DEADLINE = Орієнтовний дедлайн:

    Наприклад <b>17:00 26.09.24</b>
DEADLINE_ERROR = Неправильний формат, перевірте на наявність зайвих пробілів, введіть у форматі
    ГОДИНИ:ХВИЛИНИ ЧИСЛО.МІСЯЦЬ.РІК

    Наприклад <b>17:00 26.09.24</b>

# CREATE TASK
ERROR_CREATE_CARD = Помилка при створенні картки
