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
    admin_card_dep_tech = "63f11b61964c04a585f18843"
    admin_card_dep_creo = "63f13a1d58e626baa8577a1b"
else:
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    # нужно взять аккаунт !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    idBoard_tech = ""
    idBoard_creo = ""
    idList_tech = ""
    idList_creo = ""
    # cards label
    admin_card_dep_tech = ""
    admin_card_dep_creo = ""

# dict for every request
default_key_dict = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

# dict labels to card
card_labels_tech = {
    'admin': admin_card_dep_tech
}
card_labels_creo = {
    'admin': admin_card_dep_creo
}

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

    requests.request(
        "POST",
        url=urlCard,
        headers={"Accept": "application/json"},
        params=query | default_key_dict
    )


# create card 2
def create_card_creo(card, owner_dep, owner_name, date):
    query = {
        'idList': idList_creo,
        'name': card.name,
        'desc': card.desc,
        'idLabels': [card_labels_creo[owner_dep], owner_name],
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
    if len(tasks_l) == 0:
        return TaskResult("У вас нет активных заданий")
    else:
        markup = types.InlineKeyboardMarkup()
        for card in tasks_l:
            markup.add(types.InlineKeyboardButton(card.name, callback_data=f"card_{card.id}"))

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
        url=urlCard+f"/{id_card}",
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
