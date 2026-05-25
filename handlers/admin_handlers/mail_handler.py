from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter, or_f
from aiogram.types import InputMediaPhoto, InputMediaVideo

import logging
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import mail_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


class FsmNewsletter(StatesGroup):
    text = State()


@router.message(F.text == 'Создать рассылку 🗝')
async def create_newslatter(message: types.Message, state: FSMContext):
    """
    Начало создания рассылки
    :param message:
    :param state:
    :return:
    """
    logging.info('create_newslatter')
    markup = await mail_keyboard.select_users_type()
    await state.clear()
    await state.set_state(default_state)
    await message.answer('Выберите категорию пользователей, которым хотите отправить рассылку👇', reply_markup=markup)


@router.callback_query(F.data == 'back-mail-select-type')
async def back_to_select_type(callback: types.CallbackQuery, state: FSMContext):
    """
    Возврат к выбору категории пользователей для рассылки
    :param callback:
    :param state:
    :return:
    """
    logging.info('back_to_select_type')
    markup = await mail_keyboard.type_of_male()
    await state.clear()
    await state.set_state(default_state)
    await callback.message.edit_text('Выберите категорию пользователей, которым хотите отправить рассылку👇', reply_markup=markup)


@router.callback_query(F.data.startswith('select-user-to-mail-admin_'))
async def select_type(callback: types.CallbackQuery, state: FSMContext):
    """
    Выбор категории пользователей
    :param callback:
    :param state:
    :return:
    """
    logging.info('select_type')
    type = str(callback.data).split('_')[1]
    markup = await mail_keyboard.back_button('back-mail-select-type')

    await state.set_state(FsmNewsletter.text)
    await callback.message.edit_text(
        'Отправьте текст, фото, или файлы для рассылки (В том виде, в каком он должен дойти до пользователя)',
        reply_markup=markup)
    await state.set_state(FsmNewsletter.text)
    await state.update_data(type=type)
    await state.update_data(media='')
    await state.update_data(files='')


@router.message(StateFilter(FsmNewsletter.text))
async def get_post(message: types.Message, state: FSMContext):
    """Получение поста для рассылки"""
    logging.info('get_post')
    state_data = await state.get_data()
    markup = await mail_keyboard.send_or_back_or_delete(state_data['type'])

    media_data = state_data['media']
    files_data = state_data['files']
    if message.photo:
        file_id = message.photo[-1].file_id
        media_data += f'photo:{file_id}|'
        await state.update_data(media=media_data)

        if message.caption:
            await state.update_data(text=message.caption)
            await message.answer('Данные о рассылке загружены ✅\n\nВыберите действие', reply_markup=markup)


    elif message.video:
        file_id = message.video.file_id
        media_data += f'video:{file_id}|'
        await state.update_data(media=media_data)

        if message.caption:
            await state.update_data(text=message.caption)
            await message.answer('Данные о рассылке загружены ✅\n\nВыберите действие', reply_markup=markup)


    elif message.text:
        await state.update_data(text=message.text)
        await message.answer('Данные о рассылке загружены ✅\n\nВыберите действие', reply_markup=markup)

    else:
        file_id = message.document.file_id
        files_data += f'{file_id}|'
        await state.update_data(files=files_data)

        if message.caption:
            await state.update_data(text=message.caption)
            await message.answer('Данные о рассылке загружены ✅\n\nВыберите действие', reply_markup=markup)


@router.callback_query(F.data == 'cancel-mail-admin')
async def cancel_mail(callback: types.CallbackQuery, state: FSMContext):
    """
    Отмена создания рассылки
    :param callback:
    :param state:
    :return:
    """
    logging.info('cancel_mail')
    await state.clear()
    await state.set_state(default_state)
    await callback.message.edit_text('Создание рассылки отменено ❌')


@router.callback_query(F.data == 'send-mail-now')
async def send_mail_now(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """
    Отправка рассылки сразу
    :param callback:
    :param state:
    :return:
    """
    logging.info('send_mail_now')
    state_data = await state.get_data()
    media = state_data['media']
    text = state_data['text']
    files = state_data['files']
    type = state_data['type']

    user_ids = await admin_requests.get_user_ids_for_newsletter(type)
    cnt_users = len(user_ids)

    media_list = []
    media_input = media.split('|')[:-1]

    await callback.message.delete()
    await callback.message.answer('Начинаю отправлять рассылку ...')

    if media_input:
        for elem in media_input:
            if media_input.index(elem) != 0:
                if elem.split(':')[0] == 'photo':
                    photo = InputMediaPhoto(media=elem.split(':')[1])
                    media_list.append(photo)
                else:
                    video = InputMediaVideo(media=elem.split(':')[1])
                    media_list.append(video)
            else:
                if elem.split(':')[0] == 'photo':
                    photo = InputMediaPhoto(media=elem.split(':')[1], caption=text)
                    media_list.append(photo)
                else:
                    video = InputMediaVideo(media=elem.split(':')[1], caption=text)
                    media_list.append(video)

        cnt_false = 0
        for user_data in user_ids:
            try:
                await bot.send_media_group(chat_id=user_data, media=media_list)
                for file in files.split('|')[:-1]:
                    await bot.send_document(chat_id=user_data, document=file)
            except Exception as e:
                logging.info(f'Ошибка отправки рассылки: {e}')
                cnt_false += 1
                pass

    else:
        e = None
        cnt_false = 0
        for user_data in user_ids:
            try:
                await bot.send_message(chat_id=user_data, text=text)
                for file in files.split('|')[:-1]:
                    await bot.send_document(chat_id=user_data, document=file)
            except Exception as e:
                logging.info(f'Ошибка отправки рассылки: {e}')
                cnt_false += 1
                pass

    await callback.message.answer(f'✅ Рассылка отправлена на {cnt_users} пользователей\n\n'
                                     f'Получили: {cnt_users - cnt_false}/{cnt_users} пользователей')



















