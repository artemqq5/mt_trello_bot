from repository.model.trello_card import TrelloCard


def check_view_order(order_params: dict[str, str]) -> str:
    formated_order = ""

    for param in order_params:
        if param != 'general':
            formated_order += f"<b>{param}:</b> {order_params[param]}\n"
        else:
            for param_general in order_params[param]:
                formated_order += f"<b>{param_general}:</b> {order_params[param][param_general]}\n"

    return formated_order


def parse_to_trello_card_format_creo(task_creo, user, user_tg):
    desk = ""

    for i in task_creo:
        if i not in ('id',):
            if task_creo[i] is not None:
                desk += f"{i}: {task_creo[i]}\n"

    desk += "\n"
    desk += f"username: @{user_tg}\n"
    desk += f"telegram id: {user.id}\n"

    trello_card = TrelloCard(
        name=f"#{task_creo['id']} {task_creo['category']} | {task_creo['format']}",
        desc=desk,
        date=task_creo.get('deadline', "")
    )

    return trello_card

