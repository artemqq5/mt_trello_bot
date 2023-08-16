from ast import literal_eval

from telebot import types
from trello import TrelloClient
import requests

from config import DEBUG_MODE
from private_config import local_secret_trello, local_token_trello, local_api_key_trello, server_api_key_trello, \
    server_token_trello, server_secret_trello

# key, token, secret key
if DEBUG_MODE:
    API_KEY_TRELLO = local_api_key_trello
    TOKEN_TRELLO = local_token_trello
    API_SECRET_TRELLO = local_secret_trello
    #####
    idBoard_tech = "63dee8451b098dbb297364ce"
    idBoard_creo = "63f1382831806175541ec243"
    idList_tech = "63dee8451b098dbb297364d5"
    idList_creo = "63f13834e8cccb4aadd9df57"
    # cards label
    card_labels_tech = {
        'admin': "63f11b61964c04a585f18843",
        'gambleppc': "6404850165d7ef9e460e4ff5",
        'gambleuac': "640484f407dd03c70ac1e6e4",
        'gamblefb': "640484eb648168166b969afc",
        'afmngr': "640484db11324cef2b6b24d2",
        'media': "640484d2b0f7e9d9e06e4617",
        'gambleuac_gambleppc': "647e3969f8ecd50ecf48e3bf",
        'mt_partners': "64da0c1ba5021e8081341910"
    }
    card_labels_creo = {
        'admin': "63f13a1d58e626baa8577a1b",
        'gambleppc': "6404843d6537b1e009267ff9",
        'gambleuac': "6404844caf2ec97c635166cb",
        'gamblefb': "64048456b3fa400da1d5e145",
        'afmngr': "6404846d85bbd09e92d1f715",
        'media': "64048477f9e3e14232c3430b",
        'gambleuac_gambleppc': "647e39146cdf6e588a62f2d6",
    }
else:
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    #####
    idBoard_tech = "63453d2e8f5c5c00831d85e7"
    idBoard_creo = "633c5216d400ad00dfdc62c4"
    idList_tech = "63454557e3731b04b58bf1b0"
    idList_creo = "633c563d00d9d7030833c807"
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
def create_card_tech(card, owner_dep, owner_name, date=""):

    query = {
        'idList': idList_tech,
        'name': card.name,
        'desc': card.desc,
        'idLabels': [card_labels_tech[owner_dep], owner_name, ],
        'due': date
    }

    return requests.request(
        "POST",
        url=urlCard,
        headers={"Accept": "application/json"},
        params=query | default_key_dict
    )


# create card 2
def create_card_creo(card, owner_dep, owner_name, date):

    # add label if user is not mt_partners
    mt_dep = [] if owner_name == 'mt_partners' else [card_labels_creo['mt_partners']]

    query = {
        'idList': idList_creo,
        'name': card.name,
        'desc': card.desc,
        'idLabels': [card_labels_creo[owner_dep], owner_name] + mt_dep,
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
def get_tasks(typeListId, userlabel):
    tasks_l = clientTrelloApi.get_list(typeListId).list_cards()
    markup = types.InlineKeyboardMarkup()
    for card in tasks_l:
        for label in card.idLabels:
            if str(label) == userlabel:
                markup.add(types.InlineKeyboardButton(card.name, callback_data=f"card_{card.id}"))

    if len(markup.to_dict()['inline_keyboard']) == 0:
        return TaskResult("У вас нет активных заданий")
    else:
        return TaskResult("Успешно", markup)


def get_callback_cards():
    tasks_l = clientTrelloApi.get_list(idList_tech).list_cards() + clientTrelloApi.get_list(idList_creo).list_cards()
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
