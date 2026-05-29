from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import StateFilter
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.user_keyboard import reviews_keyboard
from database.requests import user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


class FsmReviewUser(StatesGroup):
    get_review = State()
    get_suggestion = State()


@router.message(F.text == 'Помощь и отзывы 👋')
async def reviews_handler(message: types.Message, state: FSMContext):
    """Раздел с отзывами"""
    logging.info(f'reviews_handler {message.from_user.id}')
    markup = await reviews_keyboard.select_category()
    await message.answer('💜 Выбери раздел', reply_markup=markup)
    await state.clear()
    await state.set_state(default_state)



#############################################################
######################## Отзывы мам #########################
#############################################################


@router.callback_query(F.data == 'select-category-reviews-user_reviews')
async def watch_reviews(callback: types.CallbackQuery, state: FSMContext):
    """Просмотр отзывов мам"""
    logging.info(f'watch_reviews {callback.from_user.id}')
    reviews_data = await user_requests.select_reviews_to_watch()
    if reviews_data:
        markup = await reviews_keyboard.pagination_reviews_buttons(reviews_data, 0)
        review = reviews_data[0].__dict__
        text = (f'💜 Отзыв № {review["id"]}\n'
                f'Оценка: {"⭐️" * review["grade"]}\n'
                f'Комментарий: {review["comment"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)
    else:
        markup = await reviews_keyboard.back_button('back-user-reviews_main')
        await callback.message.edit_text('💜 Отзывов еще нет', reply_markup=markup)

    await state.clear()
    await state.set_state(default_state)


@router.callback_query(F.data.startswith('pagination-user-reviews_'))
async def pagination(callback: types.CallbackQuery):
    """Пагинация отзывов"""
    logging.info(f'pagination {callback.from_user.id}')
    page = int(str(callback.data).split('_')[1])
    reviews_data = await user_requests.select_reviews_to_watch()
    markup = await reviews_keyboard.pagination_reviews_buttons(reviews_data, page)

    review = reviews_data[page].__dict__
    text = (f'💜 Отзыв № {review["id"]}\n'
            f'Оценка: {"⭐️" * review["grade"]}\n'
            f'Комментарий: {review["comment"]}')

    await callback.message.edit_text(text=text, reply_markup=markup)


#############################################################
###################### Написать отзыв #######################
#############################################################


@router.callback_query(F.data == 'select-category-reviews-user_send-review')
async def write_review(callback: types.CallbackQuery):
    """Написать отзыв"""
    logging.info('write_review')
    user_id = int(callback.from_user.id)
    user_write_review = await user_requests.check_user_review(user_id)
    if user_write_review:
        markup = await reviews_keyboard.back_button('back-user-reviews_main')
        await callback.message.edit_text('💜 Ты уже написала отзыв', reply_markup=markup)
    else:
        markup = await reviews_keyboard.select_grade_buttons()
        await callback.message.edit_text('💜 Выбери оценку', reply_markup=markup)


@router.callback_query(F.data.startswith('select-grade-user_'))
async def select_grade(callback: types.CallbackQuery, state: FSMContext):
    """Выбор оценка"""
    logging.info('select_grade')
    grade = int(str(callback.data).split('_')[1])
    markup = await reviews_keyboard.back_button('back-user-reviews_get-grade')
    await callback.message.edit_text('💜 Введи комментарий к оценке', reply_markup=markup)
    await state.set_state(FsmReviewUser.get_review)
    await state.update_data(grade=grade)


@router.message(StateFilter(FsmReviewUser.get_review))
async def get_review_comment(message: types.Message, state: FSMContext):
    """Получение комментария к отзыву"""
    logging.info('get_review_comment')
    comment = str(message.text)
    state_data = await state.get_data()
    markup = await reviews_keyboard.yes_or_no_or_back_review()
    text = (f'💜 Ты уверена что хочешь оставить отзыв?\n'
            f'Оценка: {"⭐️" * state_data["grade"]}\n'
            f'Комментарий: {comment}')

    await message.answer(text=text, reply_markup=markup)
    await state.update_data(comment=comment)
    await state.set_state(default_state)



@router.callback_query(F.data.startswith('send-review-or-not_'))
async def send_review_or_not(callback: types.CallbackQuery, state: FSMContext):
    """Отправить отзыв или нет"""
    logging.info('send_review_or_not')
    flag = str(callback.data).split('_')[1]
    if flag == 'yes':
        user_id = int(callback.from_user.id)
        username = str(callback.from_user.username)
        state_data = await state.get_data()
        await user_requests.add_new_review(user_id, username, state_data)
        await callback.message.edit_text('Отзыв успешно отправлен ✅')
    else:
        await callback.message.edit_text('Добавление отзыва отменено ❌')

    await state.clear()
    await state.set_state(default_state)


#############################################################
################### Оставить предложение ####################
#############################################################


@router.callback_query(F.data == 'select-category-reviews-user_suggestion')
async def add_suggestions(callback: types.CallbackQuery, state: FSMContext):
    """Оставить предложение"""
    logging.info('add_suggestion')
    markup = await reviews_keyboard.back_button('back-user-reviews_main')
    await callback.message.edit_text('💜 Расскажи что бы ты хотела в будущем увидеть в боте', reply_markup=markup)
    await state.set_state(FsmReviewUser.get_suggestion)


@router.message(StateFilter(FsmReviewUser.get_suggestion))
async def get_suggestion(message: types.Message, state: FSMContext):
    """Получение предложения"""
    logging.info('get_suggestion')
    suggestion = str(message.text)
    markup = await reviews_keyboard.yes_or_no_or_back_suggestion()
    text = (f'💜 Ты уверена что хочешь оставить пожелание?\n\n'
            f'{suggestion}')

    await message.answer(text=text, reply_markup=markup)
    await state.set_state(default_state)
    await state.update_data(suggestion=suggestion)


@router.callback_query(F.data.startswith('send-suggestion-or-not_'))
async def send_suggestion_or_not(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Отправить предложение или нет"""
    logging.info('send_suggestion_or_not')
    flag = str(callback.data).split('_')[1]
    if flag == 'yes':
        username = str(callback.from_user.username)
        state_data = await state.get_data()

        text = (f'Пожелание от пользователя: @{username}\n\n'
                f'* {state_data["suggestion"]}')

        for admin_id in admin_ids:
            try:
                await bot.send_message(int(admin_id), text=text)
            except Exception as e:
                logging.info(f'Не удалось отправить пожеление админам: {e}')
                pass

        await callback.message.edit_text('Предложение успешно отправлено ✅')
    else:
        await callback.message.edit_text('Отправка предложения отменена ❌')

    await state.clear()
    await state.set_state(default_state)



#############################################################
################# Обработка кнопок назад ####################
#############################################################


@router.callback_query(F.data.startswith('back-user-reviews_'))
async def back_buttons(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопок назад"""
    logging.info(f'back_buttons {callback.from_user.id}')
    flag = str(callback.data).split('_')[1]

    if flag == 'main':
        markup = await reviews_keyboard.select_category()
        await callback.message.edit_text('💜 Выбери раздел', reply_markup=markup)
        await state.clear()
        await state.set_state(default_state)

    if flag == 'get-grade':
        markup = await reviews_keyboard.select_grade_buttons()
        await callback.message.edit_text('💜 Выбери оценку', reply_markup=markup)
        await state.set_state(default_state)

    if flag == 'get-comment':
        markup = await reviews_keyboard.back_button('back-user-reviews_get-grade')
        await callback.message.edit_text('💜 Введи комментарий к оценке', reply_markup=markup)
        await state.set_state(FsmReviewUser.get_review)

    if flag == 'get-suggestion':
        markup = await reviews_keyboard.back_button('back-user-reviews_main')
        await callback.message.edit_text('💜 Расскажи что бы ты хотела в будущем увидеть в боте', reply_markup=markup)
        await state.set_state(FsmReviewUser.get_suggestion)







