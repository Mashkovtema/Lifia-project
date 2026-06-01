from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter, or_f
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.user_keyboard import preparation_recovery_keyboard
from database.requests import user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


@router.message(F.text == 'Подготовка к родам 🧘')
async def preparation(message: types.Message):
    """Восстанлвние"""
    logging.info(f'preparation: {message.from_user.id}')
    user_id = int(message.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    challenges = await user_requests.get_challenges_by_status('Для беременных', user_data['week'])
    completed_challenges = await user_requests.get_user_completed_challenges(user_id)
    if challenges:
        markup = await preparation_recovery_keyboard.challenges_buttons(challenges, completed_challenges)
        text = (f'💜 Твоя программа на {user_data["week"]} неделю:\n\n'
                f'💜 За выполнение какого либо задания начисляется по 1 баллу, '
                'которые потом можно будет обменять на приз\n\n')

        for task in challenges:
            index = challenges.index(task) + 1
            task = task.__dict__
            text += f'{index}. {task["name"]}\n'

        text += '\nОтметь что ты уже выполнила 👇'
        await message.answer(text=text, reply_markup=markup)

    else:
        await message.answer('💜 К сожалению доступных заданий еще нет ')


@router.message(F.text == 'Восстановление 🌸')
async def recovery(message: types.Message):
    """Восстанлвние"""
    logging.info(f'recovery: {message.from_user.id}')
    user_id = int(message.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    challenges = await user_requests.get_challenges_by_status('Для родивших', user_data['week'])
    completed_challenges = await user_requests.get_user_completed_challenges(user_id)
    if challenges:
        markup = await preparation_recovery_keyboard.challenges_buttons(challenges, completed_challenges)
        text = (f'💜 Твоя программа на {user_data["week"]} неделю:\n\n'
                f'💜 За выполнение какого либо задания начисляется по 1 баллу, '
                'которые потом можно будет обменять на приз\n\n')

        for task in challenges:
            index = challenges.index(task) + 1
            task = task.__dict__
            text += f'{index}. {task["name"]}\n\n'

        text += '\nОтметь что ты уже выполнила 👇'
        await message.answer(text=text, reply_markup=markup)

    else:
        await message.answer('💜 К сожалению доступных заданий еще нет ')


@router.callback_query(F.data == 'back-to-my-tasks')
async def back_to_my_tasks(callback: types.CallbackQuery):
    """Назад к заданиям"""
    logging.info('back_to_my_tasks')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    if user_data['mom_or_not']:
        challenges = await user_requests.get_challenges_by_status('Для родивших', user_data['week'])
    else:
        challenges = await user_requests.get_challenges_by_status('Для беременных', user_data['week'])

    completed_challenges = await user_requests.get_user_completed_challenges(user_id)
    markup = await preparation_recovery_keyboard.challenges_buttons(challenges, completed_challenges)
    text = (f'💜 Твоя программа на {user_data["week"]} неделю:\n\n'
            f'💜 За выполнение какого либо задания начисляется по 1 баллу, '
            'которые потом можно будет обменять на приз\n\n')

    for task in challenges:
        index = challenges.index(task) + 1
        task = task.__dict__
        text += f'{index}. {task["name"]}\n\n'

    text += '\nОтметь что ты уже выполнила 👇'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('complete-challenge-user_'))
async def complete_task(callback: types.CallbackQuery):
    """Выполнение задания"""
    logging.info('complete_task')
    user_id = int(callback.from_user.id)
    task_id = int(str(callback.data).split('_')[1])

    await user_requests.user_completed_task(user_id, task_id)

    user_data = await user_requests.get_user_data(user_id)
    if user_data['mom_or_not']:
        challenges = await user_requests.get_challenges_by_status('Для родивших', user_data['week'])
    else:
        challenges = await user_requests.get_challenges_by_status('Для беременных', user_data['week'])
    completed_challenges = await user_requests.get_user_completed_challenges(user_id)

    markup = await preparation_recovery_keyboard.challenges_buttons(challenges, completed_challenges)
    text = (f'💜 Твоя программа на {user_data["week"]} неделю:\n\n'
            f'💜 За выполнение какого либо задания начисляется по 1 баллу, '
            'которые потом можно будет обменять на приз\n\n')

    for task in challenges:
        index = challenges.index(task) + 1
        task = task.__dict__
        text += f'{index}. {task["name"]}\n\n'

    text += '\nОтметь что ты уже выполнила 👇'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('uncomplete-challenge-user_'))
async def uncomplete_task(callback: types.CallbackQuery):
    """Отмена выполнения задания"""
    logging.info('uncomplete_task')
    user_id = int(callback.from_user.id)
    task_id = int(str(callback.data).split('_')[1])

    await user_requests.user_uncompleted_task(user_id, task_id)

    user_data = await user_requests.get_user_data(user_id)
    if user_data['mom_or_not']:
        challenges = await user_requests.get_challenges_by_status('Для родивших', user_data['week'])
    else:
        challenges = await user_requests.get_challenges_by_status('Для беременных', user_data['week'])
    completed_challenges = await user_requests.get_user_completed_challenges(user_id)

    markup = await preparation_recovery_keyboard.challenges_buttons(challenges, completed_challenges)
    text = (f'💜 Твоя программа на {user_data["week"]} неделю:\n\n'
            f'💜 За выполнение какого либо задания начисляется по 1 баллу, '
            'которые потом можно будет обменять на приз\n\n')

    for task in challenges:
        index = challenges.index(task) + 1
        task = task.__dict__
        text += f'{index}. {task["name"]}\n\n'

    text += '\nОтметь что ты уже выполнила 👇'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == 'how-many-points')
async def how_many_points(callback: types.CallbackQuery):
    """Просмотр кол-ва баллов"""
    logging.info('how_many_points')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    markup = await preparation_recovery_keyboard.back_button()

    if user_data['bonus_cnt'] > 300:
        await callback.message.edit_text('💜 Бонусов хватает - ссылка на подарок', reply_markup=markup)
    else:
        await callback.message.edit_text(f'💜 У тебя сейчас {user_data["bonus_cnt"]} очков, '
                                         f'до подарка необходимо заработать еще {300-user_data["bonus_cnt"]}',
                                            reply_markup=markup)


















