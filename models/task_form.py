model_task_list = {}

# step (0-type, 1-tg_group, 2-adv_name, 3-offer_name, 4-geo, 5-reward_geo, 6-promo_link) offer_edit\add
# step (0-name_app, 1-id_cabinets, 2-desc,) share app
# step (0-currency_type, 1-geo, 2-timing_video, 3-format, 4-source, 5-count, 6-offer, 7-title, 8-desc) order creo
# step (0-title, 1-desc, 2-time) custom task
# step (0-geo, 1-name, 2-desc, 3-time) pwa
# step (0-geo, 1-offer) create campaign

task_step = {"step": 0, }


def set_task_step(step):
    global task_step
    task_step["step"] = step


def reset_task_list():
    model_task_list.clear()
    set_task_step(0)