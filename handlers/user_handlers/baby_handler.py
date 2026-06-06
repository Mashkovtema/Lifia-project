from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.user_keyboard import baby_keyboard
from database.requests import user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


@router.message(F.text == 'Уход за малышом 👶')
async def baby_handler(message: types.Message, state: FSMContext):
    """Уход за малышом"""
    logging.info('baby_handler')
    markup = await baby_keyboard.razdels_buttons()
    await message.answer('💜 Выбери раздел', reply_markup=markup)
    await state.clear()
    await state.set_state(default_state)


@router.callback_query(F.data == 'back-to-select-razdel-baby')
async def back_to_main(callback: types.CallbackQuery):
    """Назад к выбору раздела"""
    logging.info('back_to_main')
    markup = await baby_keyboard.razdels_buttons()
    await callback.message.edit_text('💜 Выбери раздел', reply_markup=markup)


@router.callback_query(F.data.startswith('select-baby-razdel_'))
async def select_razdel(callback: types.CallbackQuery, state: FSMContext):
    """Выбор раздела"""
    logging.info('select_razdel')
    flag = str(callback.data).split('_')[1]

    if flag == 'Кормление':
        markup = await baby_keyboard.feeding_buttons()
    if flag == 'Сон малыша':
        markup = await baby_keyboard.sleep_buttons()
    if flag == 'Гигиена и купание':
        markup = await baby_keyboard.gigiena_buttons()
    if flag == 'Здоровье без паники':
        markup = await baby_keyboard.health_buttons()
    if flag == 'Плач':
        markup = await baby_keyboard.plach_buttons()
    if flag == 'Ты не одна':
        markup = await baby_keyboard.mom_buttons()

    await state.update_data(razdel=flag)
    await callback.message.edit_text(text="💜 Выбери тему", reply_markup=markup)


@router.callback_query(F.data.startswith('get-baby-user-text_'))
async def show_text(callback: types.CallbackQuery, state: FSMContext):
    """Выбор текста для отображения"""
    logging.info('show_text')
    flag = int(str(callback.data).split('_')[1])
    text = await utils.get_text_by_razdel_mom(flag)
    markup = await baby_keyboard.back_or_ai_chat()
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == 'back-to-select-theme-baby')
async def back_to_select_them(callback: types.CallbackQuery, state: FSMContext):
    """Назад к выбору темы"""
    logging.info('back_to_select_them')
    state_data = await state.get_data()
    flag = state_data['razdel']

    if flag == 'Кормление':
        markup = await baby_keyboard.feeding_buttons()
    if flag == 'Сон малыша':
        markup = await baby_keyboard.sleep_buttons()
    if flag == 'Гигиена и купание':
        markup = await baby_keyboard.gigiena_buttons()
    if flag == 'Здоровье без паники':
        markup = await baby_keyboard.health_buttons()
    if flag == 'Плач':
        markup = await baby_keyboard.plach_buttons()
    if flag == 'Ты не одна':
        markup = await baby_keyboard.mom_buttons()

    await state.update_data(razdel=flag)
    await callback.message.edit_text(text="💜 Выбери тему", reply_markup=markup)














