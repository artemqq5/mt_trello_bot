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
else:
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello


# list id (Нужно сделать, В процессе, Готово)
if DEBUG_MODE:
    idList_NEED_TO_DO = "63dee8451b098dbb297364d5"
    idList_IN_PROCCESS = "63dee8451b098dbb297364d6"
    idList_READY = "63dee8451b098dbb297364d7"
else:
    # нужно взять аккаунт !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    idList_NEED_TO_DO = ""
    idList_IN_PROCCESS = ""
    idList_READY = ""


# dict for every request
default_key_dict = {'key': API_KEY_TRELLO, 'token': TOKEN_TRELLO}

# url for working with cards
urlCard = "https://api.trello.com/1/cards"


# client make get requests for components of trello boards
# clientTrelloApi = TrelloClient(
#     api_key=API_KEY_TRELLO,
#     api_secret=API_SECRET_TRELLO,
#     token=TOKEN_TRELLO
# )


# create card
def create_card(name_card):
    requests.request(
        "POST",
        urlCard,
        headers={"Accept": "application/json"},
        params={'idList': idList_NEED_TO_DO, 'name': name_card} | default_key_dict
    )
