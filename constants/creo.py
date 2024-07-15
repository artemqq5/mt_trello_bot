DESIGN = "Креатив"
# ---------------------------------------------------------------------------
DESIGN_FORMAT = "Виберіть формат креативу"

VIDEO_FORMAT = "Відео"
STATIC_FORMAT = "Статика"
GIF_ANIM_FORMAT = "GIF-анімація"

FORMAT_CREO_LIST = (VIDEO_FORMAT, STATIC_FORMAT, GIF_ANIM_FORMAT)
# ---------------------------------------------------------------------------
DESIGN_CATEGORY = "Виберіть категорію креативу"

NUTRA = "Нутра (Nutra)"
BETTING = "Беттінг (Betting)"
I_GAMING = "Гемблінг (iGaming)"
DATING = "Дейтинг (Dating)"
DEEP_FAKE = "DeepFake"
FINANCE = "Фінанси (Finance)"  # sub 3 categories
E_COMMERCE = "Товарка (E-commerce)"
SWEEPSTAKES = "Свіпстейки (Sweepstakes)"
ESSAY = "Освіта (Essay)"
GAMING = "Геймінг (Gaming)"
LANDING_UI_UX = "UI/UX лендінг"
APP_DESIGN = "APP Design"
OTHER = "Інше (Other)"

CATEGORY_CREO_LIST_VIDEO = (NUTRA, BETTING, I_GAMING, DATING, DEEP_FAKE, FINANCE, E_COMMERCE, SWEEPSTAKES, ESSAY,
                            GAMING, APP_DESIGN, OTHER)
CATEGORY_CREO_LIST_STATIC = (NUTRA, BETTING, I_GAMING, DATING, FINANCE, E_COMMERCE, SWEEPSTAKES, ESSAY, GAMING,
                             LANDING_UI_UX, APP_DESIGN, OTHER)
CATEGORY_CREO_LIST_GIF_ANIM = (NUTRA, BETTING, I_GAMING, DATING, FINANCE, E_COMMERCE, SWEEPSTAKES, ESSAY, GAMING,
                               LANDING_UI_UX, APP_DESIGN, OTHER)

FORMAT_TO_CATEGORY = {
    VIDEO_FORMAT: CATEGORY_CREO_LIST_VIDEO,
    STATIC_FORMAT: CATEGORY_CREO_LIST_STATIC,
    GIF_ANIM_FORMAT: CATEGORY_CREO_LIST_GIF_ANIM
}

CRYPTO = "Крипта (Crypto Finance)"
FOREX = "Форекс (Forex Finance)"
OTHER_FINANCE = "Інше (Other Finance)"

FINANCE_CATEGORY_LIST = (CRYPTO, FOREX, OTHER_FINANCE)
# ---------------------------------------------------------------------------
DESIGN_TYPE = "Виберіть тип креативу"

NEW_CREATIVE = "З нуля (New)"
ADAPTIVE_CREATIVE = "Адаптив (Adaptive)"

TYPE_CREO_LIST = (NEW_CREATIVE, ADAPTIVE_CREATIVE)

# ---------------------------------------------------------------------------
# Creative Default
GEO_MESSAGE = "Змінити ГЕО (Change country):"
LANGUAGE_MESSAGE = "Мова (Language):"
CURRENCY_MESSAGE = "Валюта (Currency):"
FORMAT_MESSAGE = ("Формат креативу: розширення (наприклад 1000х1000px), формат файлу"
                  " (наприклад, mp4), розмір файлу (наприклад до 10mb), тривалість у секундах:")
OFFER_MESSAGE = "Оффер(Offer), слоган/бонуси/текст для заклику до дії (CTA):"
VOICE_MESSAGE = "Озвучення(VoiceOver):"
SOURCE_MESSAGE = "Вкладення/джерела: посилання на файл (відео/фото) наприклад: https://fex.net/"
DESCRIPTION_MESSAGE = "Опис завдання(детально опишіть ваші вимоги до креативу, наприклад кадр за кадром):"
#
# Creative APP
PLATFORM_MESSAGE = "Виберіть платформу або введіть вручну:"
# type
APP_STORE_TYPE = "AppStore"
GOOGLE_PLAY_TYPE = "Google Play"

# Check task view -----------------------------
ALL_TASK_GOOD = "Все правильно"
ORDER_AGAIN_RETURN = "Заповнити спочатку"

# format
WRONG_FORMAT_INPUT_CREO = "Неправильний формат введення для кількості крео"
COUNT_OF_CREO = "Вкажіть кількість креативів, за замовчуванням 1"
SUB_DESC_FOR_OTHER_CREO = "Вкажіть додатковий опис для наступних крео"


