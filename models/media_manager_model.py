model_media = {
    "currency_type": None,
    "geo": None,
    "timing_video": None,
    "format": None,
    "source": None,
    "count": None,
    "offer": None,
    "title": None,
    "desc": None
}

# step (0-currency_type, 1-geo, 2-timing_video, 3-format, 4-source, 5-count, 6-offer, 7-title, 8-desc)
media_step = {"step": 0, }


def set_media_step(step):
    global media_step
    media_step["step"] = step


def reset_media():
    model_media.clear()
