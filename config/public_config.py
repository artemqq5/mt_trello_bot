from config import private_config
from constants.dep import *

is_development = True

# the same
API_KEY_TRELLO = private_config._api_key_trello
TOKEN_TRELLO = private_config._token_trello

if is_development:
    HOSTENAME_ = private_config.test_hostname
    PASSWORD_DATABASE = private_config.test_database_password
    NAME_DATABASE = private_config.test_database_name
    #
    BOT_TOKEN = private_config.test_bot_token
    #
    # Trello #
    ID_BOARD_TECH = "657349bfd5dd7da8739e6058"  # the same
    ID_BOARD_CREO = "657349bfd5dd7da8739e6058"  # the same
    #
    ID_LIST_TECH = "658bdfb79109634c42cdfb7c"
    ID_LIST_CREO = "658bddfabd1bbd024833641c"

    ID_LIST_TECH_GLEB = "6691678871a5be4f5dd4e689"
    ID_LIST_TECH_EGOR = "669167941c8f949834c119e8"

    # cards label
    card_labels_tech = {
        ADMIN_: "658be00755bc04065d2f97e3",
        GAMBLE_PPC: "658be1eb7716db4de92082e7",
        GAMBLE_UAC: "658be1f3dbf8ba3d96034010",
        GAMBLE_FB: "658be1fbcc224c23f824165b",
        AFMNGR: "658be203472d643a8835230c",
        MEDIA_: "658be20d9945e2fbaace5b6b",
        GAMBLE_UAC_PPC: "658be21423314a72eba3188f",
        MT_PARTNERS: "658be21ebddcbb8049622ebb",
        DEV_TECH: "65f2d01ce002749f00e3842a"
    }
    card_labels_creo = {
        ADMIN_: "658be00755bc04065d2f97e3",
        GAMBLE_PPC: "658be1eb7716db4de92082e7",
        GAMBLE_UAC: "658be1f3dbf8ba3d96034010",
        GAMBLE_FB: "658be1fbcc224c23f824165b",
        AFMNGR: "658be203472d643a8835230c",
        MEDIA_: "658be20d9945e2fbaace5b6b",
        GAMBLE_UAC_PPC: "658be21423314a72eba3188f",
    }
else:
    HOSTENAME_ = private_config._hostname
    PASSWORD_DATABASE = private_config._database_password
    NAME_DATABASE = private_config._database_name
    #
    BOT_TOKEN = private_config._bot_token
    #
    # Trello #
    ID_BOARD_TECH = "63453d2e8f5c5c00831d85e7"
    ID_BOARD_CREO = "633c5216d400ad00dfdc62c4"
    #
    ID_LIST_TECH = "63454557e3731b04b58bf1b0"
    ID_LIST_CREO = "656ee887fd55c6e59e4a0df8"

    ID_LIST_TECH_GLEB = ""
    ID_LIST_TECH_EGOR = ""

    # cards label
    card_labels_tech = {
        ADMIN_: "634eba07598e200171c9c440",
        GAMBLE_PPC: "637cd15bc7f02600b406622a",
        GAMBLE_UAC: "635e88d84e89fc02a1fed322",
        GAMBLE_FB: "635cfb6e71b54701df49070c",
        AFMNGR: "63ab08faaf2cb403e4f5516b",
        MEDIA_: "6404832e79e458c4683a9c77",
        GAMBLE_UAC_PPC: "647e383b9a078c0f54f34754",
        MT_PARTNERS: "64da0c7e54116f260b35ee32",
        DEV_TECH: "65f2d27c51bad73486e51485"
    }
    card_labels_creo = {
        ADMIN_: "63886c84a055ba018fd0f714",
        GAMBLE_PPC: "64048133310cdfcb6037f91e",
        GAMBLE_UAC: "63b7f64fbaad5d00c2a14fb2",
        GAMBLE_FB: "63d12587d8379f44194d4501",
        AFMNGR: "6404835b966d3b4c25e92a5b",
        MEDIA_: "640480f372fb31ec890d8631",
        GAMBLE_UAC_PPC: "647e38d6831410f5804efb87",
    }

