from ast import literal_eval

from telebot import types
from trello import TrelloClient
import requests

from config import DEBUG_MODE
from private_config import server_api_key_trello, server_token_trello, server_secret_trello

# key, token, secret key
if DEBUG_MODE:
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    #####
    idBoard_tech = "657349bfd5dd7da8739e6058"  # the same
    idBoard_creo = "657349bfd5dd7da8739e6058"  # the same
    #
    idList_tech = "658bdfb79109634c42cdfb7c"
    #
    id_creo_new = "658bddfabd1bbd024833641c"
    # cards label
    card_labels_tech = {
        'admin': "658be00755bc04065d2f97e3",
        'gambleppc': "658be1eb7716db4de92082e7",
        'gambleuac': "658be1f3dbf8ba3d96034010",
        'gamblefb': "658be1fbcc224c23f824165b",
        'afmngr': "658be203472d643a8835230c",
        'media': "658be20d9945e2fbaace5b6b",
        'gambleuac_gambleppc': "658be21423314a72eba3188f",
        'mt_partners': "658be21ebddcbb8049622ebb"
    }
    card_labels_creo = {
        'admin': "658be00755bc04065d2f97e3",
        'gambleppc': "658be1eb7716db4de92082e7",
        'gambleuac': "658be1f3dbf8ba3d96034010",
        'gamblefb': "658be1fbcc224c23f824165b",
        'afmngr': "658be203472d643a8835230c",
        'media': "658be20d9945e2fbaace5b6b",
        'gambleuac_gambleppc': "658be21423314a72eba3188f",
        'mt_partners': "658be21ebddcbb8049622ebb"
    }
else:
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    #####
    idBoard_tech = "63453d2e8f5c5c00831d85e7"
    idBoard_creo = "633c5216d400ad00dfdc62c4"
    #
    idList_tech = "63454557e3731b04b58bf1b0"
    #
    id_creo_new = "656ee887fd55c6e59e4a0df8"
    # cards label
    card_labels_tech = {
        'admin': "634eba07598e200171c9c440",
        'gambleppc': "637cd15bc7f02600b406622a",
        'gambleuac': "635e88d84e89fc02a1fed322",
        'gamblefb': "635cfb6e71b54701df49070c",
        'afmngr': "63ab08faaf2cb403e4f5516b",
        'media': "6404832e79e458c4683a9c77",
        'gambleuac_gambleppc': "647e383b9a078c0f54f34754",
        'mt_partners': "64da0c7e54116f260b35ee32"
    }
    card_labels_creo = {
        'admin': "63886c84a055ba018fd0f714",
        'gambleppc': "64048133310cdfcb6037f91e",
        'gambleuac': "63b7f64fbaad5d00c2a14fb2",
        'gamblefb': "63d12587d8379f44194d4501",
        'afmngr': "6404835b966d3b4c25e92a5b",
        'media': "640480f372fb31ec890d8631",
        'gambleuac_gambleppc': "647e38d6831410f5804efb87",
    }

# dict for every request
default_key_dict = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

# url for working with cards
urlCard = "https://api.trello.com/1/cards"
# url for working with labels
urlLabels = "https://api.trello.com/1/labels"

# client make get requests for components of trello boards
clientTrelloApi = TrelloClient(
    api_key=API_KEY_TRELLO,
    api_secret=API_SECRET_TRELLO,
    token=TOKEN_TRELLO
)


# create label
def create_label(name, type_board):
    if type_board == "creo":
        idBoard = idBoard_creo
    else:
        idBoard = idBoard_tech

    query = {
        'name': f'{name}',
        'color': 'black',
        'idBoard': idBoard
    }

    response = requests.request(
        "POST",
        url=urlLabels,
        params=query | default_key_dict
    )

    return literal_eval(response.text)


# create card 1
def create_card_tech(card, labels, date=""):
    query = {
        'idList': idList_tech,
        'name': card.name,
        'desc': card.desc,
        'idLabels': labels,
        'due': date
    }

    return requests.request(
        "POST",
        url=urlCard,
        headers={"Accept": "application/json"},
        params=query | default_key_dict
    )


# create card 2
def create_card_creo(card, labels, date):
    query = {
        'idList': id_creo_new,
        'name': card.name,
        'desc': card.desc,
        'idLabels': labels,
        'due': date,
    }

    return requests.request(
        "POST",
        url=urlCard,
        headers={"Accept": "application/json"},
        params=query | default_key_dict
    )


# attachment
def add_attachments_to_card(card_id, source):
    for i in source:
        query = {
            'url': i
        }

        requests.request(
            "POST",
            url=f"https://api.trello.com/1/cards/{card_id}/attachments",
            headers={"Accept": "application/json"},
            params=query | default_key_dict
        )
    return True


# get all tasks
def get_tasks(type, userlabel):
    if type == "creo":
        tasks_l = clientTrelloApi.get_list(id_creo_new).list_cards()
    else:
        tasks_l = clientTrelloApi.get_list(idList_tech).list_cards()
    markup = types.InlineKeyboardMarkup()
    for card in tasks_l:
        for label in card.idLabels:
            if str(label) == userlabel:
                markup.add(types.InlineKeyboardButton(card.name, callback_data=f"card_{card.id}"))

    if len(markup.to_dict()['inline_keyboard']) == 0:
        return TaskResult("У вас немає активних завдань")
    else:
        return TaskResult("Успішно", markup)


def get_callback_cards():
    tech_tasks = clientTrelloApi.get_list(idList_tech).list_cards()
    creo_tasks = clientTrelloApi.get_list(id_creo_new).list_cards()
    tasks_l = tech_tasks + creo_tasks
    list_callback = []
    for card in tasks_l:
        list_callback.append(f"card_{card.id}")
    return list_callback


def get_card(id_card):
    card = clientTrelloApi.get_card(id_card)
    return card


def delete_card(id_card):
    return requests.request(
        "DELETE",
        url=urlCard + f"/{id_card}",
        headers={"Accept": "application/json"},
        params=default_key_dict
    ).ok


def write_comment(id_card, text):
    comment_link = f"https://api.trello.com/1/cards/{id_card}/actions/comments"
    query = {
        'text': text,
    }
    return requests.request(
        "POST",
        url=comment_link,
        headers={"Accept": "application/json"},
        params=query | default_key_dict
    ).ok


class TrelloCard:
    def __init__(self, name, desc, date=None):
        self.name = name
        self.desc = desc
        self.final_date = date


class TaskResult:
    def __init__(self, message, markup=None):
        self.message = message
        self.markup = markup
