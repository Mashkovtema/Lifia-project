from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter

import logging
import os
import tempfile
import img2pdf

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.user_keyboard import pregnancy_diary_keyboard
from database.requests import user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


class FsmDiary(StatesGroup):
    get_good_point = State()
    get_bad_point = State()

    get_photo = State()


@router.message(F.text == 'Дневник беременности 📖')
async def pregnancy_diary(message: types.Message):
    """Дневник беременности"""
    logging.info('pregnancy_diary')
    user_id = int(message.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    text = await user_requests.get_text_by_days_cnt(user_data['days'], 'not-mom')
    diary_data = await user_requests.get_diary_by_week(user_id, user_data['week'])
    markup = await pregnancy_diary_keyboard.diary_main_buttons(diary_data)
    await message.answer(text=text, reply_markup=markup)


#####################################
############ Настроение #############
#####################################


@router.callback_query(F.data.startswith('how-im-feeling_'))
async def how_im_feelling(callback: types.CallbackQuery):
    """Запрос настроения"""
    logging.info('how_im_feelling')
    flag = str(callback.data).split('_')[1]
    if flag == 'yes':
        markup = await pregnancy_diary_keyboard.mood_buttons()
        await callback.message.edit_text('💜 Какое у тебя сейчас настроение ?', reply_markup=markup)
    else:
        await callback.answer('💜 На этой неделе ты уже отмечала настроение')


@router.callback_query(F.data.startswith('select-my-mood_'))
async def select_mood(callback: types.CallbackQuery, state: FSMContext):
    """Получение настроения"""
    logging.info('select_mood')
    mood = str(callback.data).split('_')[1]
    await state.set_state(FsmDiary.get_bad_point)
    await state.update_data(mood=mood)
    await callback.message.edit_text('💜 Что тебя сейчас беспокоит ?')


@router.message(StateFilter(FsmDiary.get_bad_point))
async def get_bad_point(message: types.Message, state: FSMContext):
    """Получение причины беспокойства"""
    logging.info('get_bad_point')
    bad_point = str(message.text)
    await state.set_state(FsmDiary.get_good_point)
    await state.update_data(bad_point=bad_point)
    await message.answer('💜 Было что то хорошее за неделю?')


@router.message(StateFilter(FsmDiary.get_good_point))
async def get_good_point(message: types.Message, state: FSMContext):
    """Получение хороших впечатлений"""
    logging.info('get_good_point')
    good_point = str(message.text)
    user_id = int(message.from_user.id)
    await state.set_state(default_state)
    await state.update_data(good_point=good_point)

    user_data = await user_requests.get_user_data(user_id)
    state_data = await state.get_data()

    await user_requests.insert_diary_data(user_id, user_data['week'], 'mood', state_data['mood'])
    await user_requests.insert_diary_data(user_id, user_data['week'], 'bad-point', state_data['bad_point'])
    await user_requests.insert_diary_data(user_id, user_data['week'], 'good-point', state_data['good_point'])

    user_data = await user_requests.get_user_data(user_id)
    text = await user_requests.get_text_by_days_cnt(user_data['days'], 'not-mom')
    diary_data = await user_requests.get_diary_by_week(user_id, user_data['week'])
    markup = await pregnancy_diary_keyboard.diary_main_buttons(diary_data)
    await message.answer(text=text, reply_markup=markup)\


##############################
### Добавление фото недели ###
##############################


@router.callback_query(F.data.startswith('add-week-photo_'))
async def add_week_photo(callback: types.CallbackQuery, state: FSMContext):
    """Обновить фото недели"""
    logging.info('add_week_photo')
    flag = str(callback.data).split('_')[1]
    if flag == 'yes':
        markup = await pregnancy_diary_keyboard.back_button('back-diary-user_main')
        await state.set_state(FsmDiary.get_photo)
        await callback.message.edit_text('💜 Отправь мне фото животика', reply_markup=markup)
    else:
        await callback.answer('💜 Ты уже добавила фото недели')


@router.message(StateFilter(FsmDiary.get_photo))
async def get_photo(message: types.Message, state: FSMContext):
    """Получение фотографии"""
    logging.info('get_photo')
    try:
        photo = str(message.photo[-1].file_id)
        user_id = int(message.from_user.id)

        user_data = await user_requests.get_user_data(user_id)
        await user_requests.insert_diary_data(user_id, user_data['week'], 'photo', photo)

        user_data = await user_requests.get_user_data(user_id)
        text = await user_requests.get_text_by_days_cnt(user_data['days'], 'not-mom')
        diary_data = await user_requests.get_diary_by_week(user_id, user_data['week'])
        markup = await pregnancy_diary_keyboard.diary_main_buttons(diary_data)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(default_state)
        await state.clear()

    except Exception as e:
        logging.info(e)
        await message.answer('Ты отправила не фото, попробуй еще раз')


######################################
### Просмотр фотографий в карусели ###
######################################


@router.callback_query(F.data == 'get-my-album')
async def get_my_album(callback: types.CallbackQuery):
    """Фото живота в карусели"""
    logging.info('get_my_album')
    user_id = int(callback.from_user.id)
    photos_data = await user_requests.get_photos_diary(user_id)
    if photos_data:
        current_photo = photos_data[0].__dict__
        markup = await pregnancy_diary_keyboard.pagination_buttons(photos_data, 0)
        await callback.message.delete()
        await callback.message.answer_photo(photo=current_photo['photo'], reply_markup=markup, caption=f'💜 {current_photo["week"]} неделя')
    else:
        await callback.answer('💜 Ты еще не добавила ни одной фотографии животика')


@router.callback_query(F.data.startswith('pagination-user-photos_'))
async def pagination(callback: types.CallbackQuery):
    """Пагинация фото"""
    logging.info('pagination')
    index = int(str(callback.data).split('_')[1])
    user_id = int(callback.from_user.id)
    photos_data = await user_requests.get_photos_diary(user_id)
    current_photo = photos_data[index].__dict__
    markup = await pregnancy_diary_keyboard.pagination_buttons(photos_data, index)

    await callback.message.delete()
    await callback.message.answer_photo(photo=current_photo['photo'], reply_markup=markup, caption=f'💜 {current_photo["week"]} неделя')


###############################
##### pdf документ с фото #####
###############################


@router.callback_query(F.data == 'create-album')
async def create_album(callback: types.CallbackQuery, bot: Bot):
    """Создание пдф документа с фотографиями"""
    logging.info('create_album')
    user_id = int(callback.from_user.id)
    photos_data = await user_requests.get_photos_diary(user_id)
    if photos_data:
        # Контекстный менеджер auto-remove=True удалит папку с файлами после выхода из блока 'with'
        with tempfile.TemporaryDirectory() as temp_dir:
            downloaded_images_paths = []

            # 2. Скачиваем каждое фото по его file_id
            for i, file in enumerate(photos_data):
                try:
                    # Получаем объект файла от Telegram
                    file = file.__dict__
                    file = await bot.get_file(file['photo'])

                    # Создаем путь для сохранения (например, /tmp/.../photo_1.jpg)
                    # Используем оригинальное расширение файла или jpg по умолчанию
                    file_extension = os.path.splitext(file.file_path or "photo.jpg")[1]
                    if not file_extension:
                        file_extension = ".jpg"
                    file_path = os.path.join(temp_dir, f"photo_{i}{file_extension}")

                    # Скачиваем файл
                    await bot.download_file(file.file_path, destination=file_path)
                    downloaded_images_paths.append(file_path)

                except Exception as e:
                    logging.info(f"Ошибка при скачивании файла {file['photo']}: {e}")

            # 3. Конвертируем скачанные изображения в один PDF
            pdf_output_path = os.path.join(temp_dir, "output.pdf")
            try:
                # img2pdf.convert принимает список путей к изображениям и возвращает байты PDF
                with open(pdf_output_path, "wb") as pdf_file:
                    pdf_file.write(img2pdf.convert(downloaded_images_paths))

                # 4. Отправляем готовый PDF пользователю
                with open(pdf_output_path, "rb") as pdf_file:
                    await callback.message.delete()
                    await bot.send_document(
                        chat_id=callback.message.chat.id,
                        document=types.BufferedInputFile(
                            pdf_file.read(),
                            filename="my_photos.pdf"
                        ),
                        caption=f"✅ Ваш PDF из {len(downloaded_images_paths)} фото готов!"
                    )

            except Exception as e:
                logging.info(f"Ошибка конвертации в PDF: {e}")
    else:
        await callback.answer('💜 Ты еще не добавила ни одной фотографии животика')


##############################
######## Кнопки назад ########
##############################


@router.callback_query(F.data.startswith('back-diary-user_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]
    user_id = int(callback.from_user.id)

    if flag == 'main':
        user_data = await user_requests.get_user_data(user_id)
        text = await user_requests.get_text_by_days_cnt(user_data['days'], 'not-mom')
        diary_data = await user_requests.get_diary_by_week(user_id, user_data['week'])
        markup = await pregnancy_diary_keyboard.diary_main_buttons(diary_data)

        try:
            await callback.message.edit_text(text=text, reply_markup=markup)
        except:
            await callback.message.delete()
            await callback.message.answer(text=text, reply_markup=markup)













