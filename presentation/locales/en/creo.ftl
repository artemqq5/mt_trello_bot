CREO-SET_TYPE = 🎨 Select the type of creative
CREO-VIDEO = 🎥 Video
CREO-STATIC = 🖼️ Static
CREO-GIF = 🎞️ GIF Animation

CREO-SET_CATEGORY = 🗂️ Vertical:
CREO-SET_GEO = 🌍 Geo:
CREO-SET_LANG = 🗣️ Language:
CREO-SET_CURRENCY = 💰 Currency:
CREO-SET_FORMAT = 📏 Creative format. Dimensions (e.g., 1000x1000px), file format (e.g., mp4), file size (e.g., up to 10mb), duration in seconds:
CREO-SET_OFFER = 🎯 Offer, slogan/bonuses/CTA text:
CREO-SET_VOICE = 🎙️ Voice-over:
CREO-SET_SOURCE = 📂 Attachments/sources: link to file (video/photo), e.g., https://fex.net/
CREO-SET_DESCRIPTION = 📝 Task description (please detail your requirements for the creative or creatives, if there are several, for example, frame by frame):
CREO-SET_DESCRIPTION_ERORR = ❗ Description is too long, currently (<b>{$size}</b>) characters. Reduce to 800:

CREO-SET_PLATFORM = 📱 Select the platform or enter manually:
CREO-APPSTORE = 🛒 AppStore
CREO-GOOGLEPLAY = 🛒 Google Play

CREO-COUNT = 🔢 Number of creatives:
CREO-COUNT_ERROR = ❗ The number must be an integer, e.g., 1 or 7:

CREO-PREVIEW = 🖼️ Creative
    ━━━━━━━━━━━━━━━━
    <b>Vertical:</b> {$category}
    <b>Type:</b> {$type}
    <b>Platform:</b> {$platform}
    <b>Geo:</b> {$geo}
    <b>Language:</b> {$lang}
    <b>Currency:</b> {$currency}
    <b>Format:</b> {$format}
    <b>Offer:</b> {$offer}
    <b>Voice-over:</b> {$voice}
    <b>Attachments/sources:</b> {$source}
    <b>Quantity:</b> {$count}

    <b>Description:</b>
    {$desc}

CREO-PREVIEW_SEND = ✅ Everything is correct
CREO-PREVIEW_RETURN = 🔄 Fill out again

CREO-CARD_NAME = #{$id} {$type} | {$category}
CREO-CARD_DESC =
    Creative type: {$type}
    Vertical: {$category}
    Platform: {$platform}
    GEO: {$geo}
    Language: {$lang}
    Currency: {$currency}
    Format: {$format}
    Offer: {$offer}
    Voice-over: {$voice}
    Source: {$source}
    Quantity: {$count}

    Task from: @{$username}

    Description:
    {$desc}
CREO-NOTIFICATION_CARD =
    #{$id} {$type} ({$category})
    ━━━━━━━━━━━━━━━━
    {$desc}

    Task from: @{$username}
    Link in Trello: {$url}
