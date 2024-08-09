import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext, L

from data.const import CREO_ACCESS
from data.repository.CreoRepository import CreoRepository
from data.repository.TrelloRepository import TrelloRepository
from data.repository.UserRepository import UserRepository
from domain.middleware.IsRoleMiddleware import IsRoleMiddleware
from domain.state.creo.OrderCreoState import OrderCreoState
from domain.use_case.NotificationUsers import NotificationUsers
from presentation.keyboards.creo.kb_order_creo import kb_set_type_creo, TypeCreo, kb_set_platform_creo, PlatformCreo, \
    kb_preview_creo, SendTaskCreo, StartAgainCreo, kb_skip_creo, SkipDeadlineCreo

router = Router()

router.message.middleware(IsRoleMiddleware(CREO_ACCESS))
router.callback_query.middleware(IsRoleMiddleware(CREO_ACCESS))


@router.callback_query(TypeCreo.filter(), OrderCreoState.Type)
async def type_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    creo_type = callback.data.split(":")[1]
    await state.update_data(type=creo_type)
    await state.set_state(OrderCreoState.Category)
    await callback.message.answer(i18n.CREO.SET_CATEGORY())


@router.message(OrderCreoState.Category)
async def category(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(category=message.text)
    await state.set_state(OrderCreoState.Geo)
    await message.answer(i18n.CREO.SET_GEO())


@router.message(OrderCreoState.Geo)
async def geo(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(geo=message.text)
    await state.set_state(OrderCreoState.Lang)
    await message.answer(i18n.CREO.SET_LANG())


@router.message(OrderCreoState.Lang)
async def lang(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(lang=message.text)
    await state.set_state(OrderCreoState.Currency)
    await message.answer(i18n.CREO.SET_CURRENCY())


@router.message(OrderCreoState.Currency)
async def currency(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(currency=message.text)
    await state.set_state(OrderCreoState.Format)
    await message.answer(i18n.CREO.SET_FORMAT())


@router.message(OrderCreoState.Format)
async def format(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(format=message.text)
    await state.set_state(OrderCreoState.Offer)
    await message.answer(i18n.CREO.SET_OFFER())


@router.message(OrderCreoState.Offer)
async def offer(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(offer=message.text)
    await state.set_state(OrderCreoState.Voice)
    await message.answer(i18n.CREO.SET_VOICE())


@router.message(OrderCreoState.Voice)
async def voice(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(voice=message.text)
    await state.set_state(OrderCreoState.Source)
    await message.answer(i18n.CREO.SET_SOURCE())


@router.message(OrderCreoState.Source)
async def source(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(source=message.text)
    await state.set_state(OrderCreoState.Desc)
    await message.answer(i18n.CREO.SET_DESCRIPTION())


@router.message(OrderCreoState.Desc)
async def desc(message: Message, state: FSMContext, i18n: I18nContext):
    if len(message.text) > 800:
        await message.answer(i18n.CREO.SET_DESCRIPTION_ERORR(size=len(message.text)))
        return
    await state.update_data(desc=message.text)
    await state.set_state(OrderCreoState.Platform)
    await message.answer(i18n.CREO.SET_PLATFORM(), reply_markup=kb_set_platform_creo)


@router.callback_query(PlatformCreo.filter(), OrderCreoState.Platform)
async def platform_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    platform_data = callback.data.split(":")[1]
    await state.update_data(platform=platform_data)
    await state.set_state(OrderCreoState.Count)
    await callback.message.answer(i18n.CREO.COUNT())


@router.message(OrderCreoState.Platform)
async def platform(message: Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(platform=message.text)
    await state.set_state(OrderCreoState.Count)
    await message.answer(i18n.CREO.COUNT())


@router.message(OrderCreoState.Count)
async def count(message: Message, state: FSMContext, i18n: I18nContext):
    try:
        num = int(message.text)
        if num <= 0:
            raise ValueError
    except ValueError as e:
        await message.answer(i18n.CREO.COUNT_ERROR())
        return

    await state.update_data(count=num)
    await state.set_state(OrderCreoState.DeadLine)
    await message.answer(i18n.DEADLINE(), reply_markup=kb_skip_creo)


@router.callback_query(SkipDeadlineCreo.filter(), OrderCreoState.DeadLine)
async def deadline_creo_skip(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    await state.set_state(OrderCreoState.Preview)
    data = await state.get_data()

    await callback.message.answer(
        text=i18n.CREO.PREVIEW(
            category=data['category'],
            type=data['type'],
            platform=data['platform'],
            geo=data['geo'],
            lang=data['lang'],
            currency=data['currency'],
            format=data['format'],
            offer=data['offer'],
            voice=data['voice'],
            source=data['source'],
            count=data['count'],
            desc=data['desc']
        ),
        reply_markup=kb_preview_creo(data)
    )


@router.message(OrderCreoState.DeadLine)
async def deadline_creo(message: Message, state: FSMContext, i18n: I18nContext):
    try:
        date_time = datetime.datetime.strptime(message.text + " +0300", '%H:%M %d.%m.%y %z')
        await state.update_data(deadline=str(date_time))
    except Exception as e:
        print(f"set_deadline_default_creative - {e}")
        await message.answer(i18n.DEADLINE_ERROR(), reply_markup=kb_skip_creo)
        return

    await state.set_state(OrderCreoState.Preview)
    data = await state.get_data()

    await message.answer(
        text=i18n.CREO.PREVIEW(
            category=data['category'],
            type=data['type'],
            platform=data['platform'],
            geo=data['geo'],
            lang=data['lang'],
            currency=data['currency'],
            format=data['format'],
            offer=data['offer'],
            voice=data['voice'],
            source=data['source'],
            count=data['count'],
            desc=data['desc']
        ),
        reply_markup=kb_preview_creo(data)
    )


@router.callback_query(SendTaskCreo.filter(), OrderCreoState.Preview)
async def send_callback(callback: CallbackQuery, state: FSMContext, i18n: I18nContext, bot: Bot):
    data = await state.update_data()
    user = UserRepository().user(callback.from_user.id)

    if not (card_id := TrelloRepository().create_creo_task(data, user, i18n)):
        await callback.answer(i18n.ERROR_CREATE_CARD(), show_alert=True)
        return

    card = CreoRepository().card(card_id)

    await NotificationUsers.notify_new_creo(callback, card, i18n)
    await callback.message.answer(i18n.TASK_SEND_SUCCESS())

