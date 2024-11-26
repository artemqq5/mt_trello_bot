# Navigation buttons
BACK = ⬅️ Back
SKIP = ⏭️ Skip

# Access messages
ACCESS_DENIED = 🚫 Access denied. Please contact the admin to get access.

# get user id
GET_USER_ID = Your Telegram ID (<code>{$telegram_id}</code>)

# Greetings
START = 👋 Hello, please select a task type
START_ADMIN = 👋 Hello, you are an administrator with full access
START_SPECIAL = 👋 Hello, you have only push-notifications functionality

# Tasks
MY_TASK = 📝 My tasks
TASK_CREO = 🎨 Creative
TASK_TECH = 🛠️ Technical
TASK_AFF = 🤝 Affiliate

# admin menu
ADMIN-ADD = ➕ Add
ADMIN-DELETE = 🔻 Delete
ADMIN-MAILING = 📩 Messaging
ADMIN-USERS = 👨‍👩‍👦 Users

# Add user
ADMIN-ADD_USER-NAME = Enter the user's name:
ADMIN-ADD_USER-TELEGRAM_ID = Enter the user's Telegram ID. The user to be added can find their ID by typing the /get_id command in this bot:
ADMIN-ADD_USER-ROLE = Select the user's role:
ADMIN-ADD_USER-TDS_ID = Enter the user's TDS ID:
ADMIN-USER_ALREADY_EXIST = ⚠️ The user already exists in the database
ADMIN-USER_ADD_SUCCESS = ✅ User successfully added
ADMIN-USER_ADD_FAIL = ❌ Failed to add user

# Delete user
ADMIN-DELETE_USER = Enter user ID:
ADMIN-USER_NO_EXIST = ⚠️ No such user in the database
ADMIN-DELETE_USER_SUCCESS = ✅ User deleted successfully
ADMIN-DELETE_USER_FAIL = ❌ Failed to delete user

# User information
ADMIN-GET_USER_INFO = <b>📋 Telegram ID:</b> <code>{$tg}</code>
    <b>Name:</b> {$nickname}
    <b>Telegram Name:</b> {$firstname}
    <b>Username:</b> {$username}
    <b>Role:</b> {$dep}
    <b>TDS ID:</b> <code>{$tds}</code>

# Mailing
ADMIN-INPUT_TEXT_MAILING = Enter text for mailing:
ADMIN-RESULT_NOTIFICATION = <b>-📊 Mailing Result-</b>

    Received messages: {$send}\{$users}
    Blocked the bot: {$block}
    Other: {$other}

# Deadline
DEADLINE = ⏰ Approximate deadline:

    For example, <b>17:00 26.09.24</b>
DEADLINE_ERROR = ❌ Incorrect format, check for extra spaces, enter in format
    HOUR:MINUTE DAY.MONTH.YEAR

    For example, <b>17:00 26.09.24</b>

# Create task
ERROR_CREATE_CARD = ❌ Error creating card
TASK_SEND_SUCCESS = ✅ Task sent successfully
