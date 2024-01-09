from constants.dep import *

TECH_FORMAT = "Виберіть формат технічного завдання"

ADD_OFFER = "Додати оффер ➕"
EDIT_OFFER = "Редагувати оффер 🔧"
SHARE_APP = "Розшарити прілу 📲"
CREATE_CAMPAIGN = "Створити кампанію 🔖"
PWA_ = "PWA пріла 💣"
OTHER_TECH = "Інше завдання 💻"
PREPARE_VAIT = "Підготувати вайт 🎁"
SETTING_CLOAK = "Налаштувати клоаку 📡"
SET_DOMAIN = "Припаркувати домен 🅿️"
TASK_MT_PARTNERS = "(MT PARTNERS) 🪄"

TECH_TASK_LIST = (
    ADD_OFFER,
    EDIT_OFFER,
    SHARE_APP,
    CREATE_CAMPAIGN,
    PWA_,
    OTHER_TECH,
    PREPARE_VAIT,
    SETTING_CLOAK,
    SET_DOMAIN,
    TASK_MT_PARTNERS
)

TECH_DEP_TASK = {
    GAMBLE_PPC: (PREPARE_VAIT, SETTING_CLOAK, SET_DOMAIN, CREATE_CAMPAIGN, OTHER_TECH),
    GAMBLE_FB or GAMBLE_UAC: (SHARE_APP, CREATE_CAMPAIGN, PWA_, OTHER_TECH),
    AFMNGR: (ADD_OFFER, EDIT_OFFER),
    MT_PARTNERS: (TASK_MT_PARTNERS,),
    DESIGNER_ or MEDIA_ or TECH_: (),
    GAMBLE_UAC_PPC: (PREPARE_VAIT, SETTING_CLOAK, SET_DOMAIN, SHARE_APP, CREATE_CAMPAIGN, PWA_, OTHER_TECH),
    ADMIN_: TECH_TASK_LIST,
}

ADD_OFFER_ACCESS = (ADMIN_, AFMNGR)
CREATE_CAMPAIGN_ACCESS = (ADMIN_, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC)
EDIT_OFFER_ACCESS = (ADMIN_, AFMNGR)
MT_PARTNERS_ACCESS = (ADMIN_, MT_PARTNERS)
OTHER_TECH_ACCESS = (ADMIN_, GAMBLE_PPC, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC)
PREPARE_VAIT_ACCESS = (ADMIN_, GAMBLE_PPC, GAMBLE_UAC_PPC)
PWA_ACCESS = (ADMIN_, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC)
SET_DOMAIN_ACCESS = (ADMIN_, GAMBLE_PPC, GAMBLE_UAC_PPC)
SETTING_CLOAK_ACCESS = (ADMIN_, GAMBLE_PPC, GAMBLE_UAC_PPC)
SHARE_APP_ACCESS = (ADMIN_, GAMBLE_FB, GAMBLE_UAC, GAMBLE_UAC_PPC)

# ADD OFFER
INPUT_TYPE_ADVERTISER = "Новий рекламодавець чи існуючий?"
TYPE_TECH_NEW = "Новий"
TYPE_TECH_EXIST = "Існуючий"

INPUT_TELEGRAM_GROUP = "Група в telegram:"
INPUT_ADVERTISER_NAME = "Ім'я рекламодавця:"
INPUT_OFFER_NAME = "Назва офферу:"
INPUT_GEO = "Гео:"
INPUT_GEO_DEDUCATION = "Відрахування з гео:"
INPUT_PROMO_LINK = "Промо посилання:"
#

# CREATE CAMPAIN
# GEO -- already have --
INPUT_APP_NAME = "Назва пріли"
#

# EDIT OFFER
INPUT_OFFER_ID = "Введіть оффер ID:"
INPUT_DESC = "Введіть опис, що зробити:"
#

# MT PARTNERS
INPUT_NAME_TASK = "Введіть назву для таску:"
# DESC -- already have --

# OTHER TASK
# NAME_TASK -- already have --
# DESC -- already have --
#

# PREPARE VAIT
# GEO -- already have --
INPUT_SOURCE = "Введіть джерело:"
INPUT_TECHNICAL_TASK = "Введіть ТЗ/посилання на ТЗ:"
# DESC -- already have --
#

# PWA
# GEO -- already have --
# NAME_TASK -- already have --
# DESC -- already have --
#

# SET DOMAIN
INPUT_OFFERS_NAME = "Введіть назви доменів:"
# DESC -- already have --
#

# SETTING CLOAK
# GEO -- already have --
INPUT_OFFER = "Введіть оффер:"
INPUT_DOMAINS = "Введіть домени:"
# DESC -- already have --
#

# SHARE APP
# APP_NAME -- already have --
INPUT_ID_CABINETS = "Введіть ID кабінетів:"
#
