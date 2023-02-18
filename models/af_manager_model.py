model_offer = {
    "operation": None,
    "type": None,
    "tg_group": None,
    "adv_name": None,
    "offer_name": None,
    "geo": None,
    "reward_geo": None,
    "promo_link": None,

    "offer_id": None,
    "desc_offer": None
}

# step (0-type, 1-tg_group, 2-adv_name, 3-offer_name, 4-geo, 5-reward_geo, 6-promo_link)
offer_step = {"step": 0, }


def set_offer_step(step):
    global offer_step
    offer_step["step"] = step


def reset_offer():
    model_offer.clear()
