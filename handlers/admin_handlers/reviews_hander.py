from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.admin_keyboard import review_keyboard
from database.requests import admin_requests
from filters.admin_filter import IsSuperAdmin


config: Config = load_config()
router = Router()
router.message.filter(IsSuperAdmin())


@router.message(F.text == 'Модерация отзывов ⭐️')
async def reviews_handler(message: types.Message, state: FSMContext):
    """Модерация отзывов"""
    logging.info('reviews_handler')
    reviews_data = await admin_requests.get_reviews_for_moderation()
    if reviews_data:
        review = reviews_data[0].__dict__
        markup = await review_keyboard.reviews_pagination(reviews_data, 0)

        text = (f'Отзыв №{review["id"]}\n\n'
                f'@{review["username"]}\n'
                f'Оценка: {"⭐️" * review["grade"]}\n'
                f'Комментарий" {review["comment"]}')

        await message.answer(text=text, reply_markup=markup)
        await state.clear()
    else:
        await message.answer('Отзывов для модерации нет ❌')
        await state.clear()


@router.callback_query(F.data.startswith('pagination-admin-reviews-moderation_'))
async def pagination(callback: types.CallbackQuery):
    """Пагинация отзывов"""
    logging.info('pagination')
    index = int(str(callback.data).split('_')[1])
    reviews_data = await admin_requests.get_reviews_for_moderation()
    review = reviews_data[index].__dict__
    markup = await review_keyboard.reviews_pagination(reviews_data, index)

    text = (f'Отзыв №{review["id"]}\n\n'
            f'@{review["username"]}\n'
            f'Оценка: {"⭐️" * review["grade"]}\n'
            f'Комментарий" {review["comment"]}')

    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('delete-review_'))
async def delete_review(callback: types.CallbackQuery):
    """Запрос удаления отзыва"""
    logging.info('delete_review')
    index = int(str(callback.data).split('_')[1])
    reviews_data = await admin_requests.get_reviews_for_moderation()
    review = reviews_data[index].__dict__
    markup = await review_keyboard.yes_or_no_buttons(f'confirm-delete-review-admin_{index}',
                                                     f'pagination-admin-reviews-moderation_{index}')

    text = (f'Отзыв №{review["id"]}\n\n'
            f'@{review["username"]}\n'
            f'Оценка: {"⭐️" * review["grade"]}\n'
            f'Комментарий" {review["comment"]}\n\n'
            f'Вы уверены что хотите удалить отзыв?')

    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('confirm-delete-review-admin_'))
async def confirm_delete_review(callback: types.CallbackQuery):
    """Удаление отзыва"""
    logging.info('confirm_delete_review')
    index = int(str(callback.data).split('_')[1])
    reviews_data = await admin_requests.get_reviews_for_moderation()
    review = reviews_data[index].__dict__
    await admin_requests.delete_review(review['id'])

    reviews_data = await admin_requests.get_reviews_for_moderation()
    if reviews_data:
        review = reviews_data[0].__dict__
        markup = await review_keyboard.reviews_pagination(reviews_data, 0)

        text = (f'Отзыв №{review["id"]}\n\n'
                f'@{review["username"]}\n'
                f'Оценка: {"⭐️" * review["grade"]}\n'
                f'Комментарий" {review["comment"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)
    else:
        await callback.message.edit_text('Отзывов для модерации нет ❌')


@router.callback_query(F.data.startswith('confirm-moderation-review_'))
async def select_review_to_commit(callback: types.CallbackQuery):
    """Потверждение модерации отзыва"""
    logging.info('select_review_to_commit')
    index = int(str(callback.data).split('_')[1])
    reviews_data = await admin_requests.get_reviews_for_moderation()
    review = reviews_data[index].__dict__
    markup = await review_keyboard.yes_or_no_buttons(f'confirm-commit-review-admin_{index}', f'pagination-admin-reviews-moderation_{index}')

    text = (f'Отзыв №{review["id"]}\n\n'
            f'@{review["username"]}\n'
            f'Оценка: {"⭐️" * review["grade"]}\n'
            f'Комментарий" {review["comment"]}\n\n'
            f'Вы уверены что хотите подтвердить отзыв?')

    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('confirm-commit-review-admin_'))
async def confirm_commit_review(callback: types.CallbackQuery):
    """Окончательно подтверждение модерации отзыва"""
    logging.info('confirm_commit_review')
    index = int(str(callback.data).split('_')[1])
    reviews_data = await admin_requests.get_reviews_for_moderation()
    review = reviews_data[index].__dict__
    await admin_requests.confirm_review(review['id'])

    reviews_data = await admin_requests.get_reviews_for_moderation()
    if reviews_data:
        review = reviews_data[0].__dict__
        markup = await review_keyboard.reviews_pagination(reviews_data, 0)

        text = (f'Отзыв №{review["id"]}\n\n'
                f'@{review["username"]}\n'
                f'Оценка: {"⭐️" * review["grade"]}\n'
                f'Комментарий" {review["comment"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)
    else:
        await callback.message.edit_text('Отзывов для модерации нет ❌')









