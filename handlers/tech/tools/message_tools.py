from repository.model.trello_card import TrelloCard


def parse_to_trello_card_format_tech(id_, task_tech, task_type, user, user_tg, tech):
    desk = ""

    for param in task_tech:
        if param is not None and param != "deadline":
            desk += f"{param}: {task_tech[param]}\n"

    desk += "\n"
    desk += f"username: @{user_tg}\n"
    desk += f"telegram id: {user.id}\n\n"
    desk += f"task for {tech}\n"

    trello_card = TrelloCard(
        name=f"#{id_} {task_type}",
        desc=desk,
        date=task_tech.get('deadline', "")
    )

    return trello_card
