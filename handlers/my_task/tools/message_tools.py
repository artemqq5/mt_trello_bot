from repository.trello_.trello_repository import TrelloRepository


def info_about_card(id_card):
    desc = ""
    card_model = TrelloRepository().get_card(id_card)
    print(card_model)

    desc += f"<b>{card_model['name']}</b>\n\n"
    desc += f"{card_model['desc']}\n\n"
    desc += card_model['shortUrl']

    return desc
