from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging

from utils import utils
from config_data.config_data import Config, load_config
from keyboard.user_keyboard import settings_keyboard
from keyboard.admin_keyboard import start_keyboard
from database.requests import user_requests

config: Config = load_config()
router = Router()

admin_ids = str(config.tg_bot.admin_ids).split(',')


@router.message(F.text == 'Настройки ⚙')
async def settings(message: types.Message):
    user_id = int(message.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    date = await utils.calculate_date(user_data['days'])
    markup = await settings_keyboard.settings_buttons(user_data['mom_or_not'])

    if user_data['mom_or_not']: # Для мам
        text = (f'💜 Настройки\n\n'
                f'Период - я уже родила\n'
                f'Дата рождения малыша - {date}\n'
                f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

    else: # Для беременных
        text = (f'💜 Настройки\n\n'
                f'Период - я еще не родила\n'
                f'Дата последней менструации - {date}\n'
                f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

    await message.answer(text=text, reply_markup=markup)


######################################
###### Изменение часового пояса ######
######################################

@router.callback_query(F.data == 'user-settings-change-time-zone')
async def change_time_zone(callback: types.CallbackQuery):
    """Изменение часового пояса"""
    logging.info('change_time_zone')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.time_zone_buttons(user_data['time_zone'])
    await callback.message.edit_text('💜 Выбери свой часовой пояс для напоминаний', reply_markup=markup)


@router.callback_query(F.data.startswith('change_time_zone_MSK'))
async def select_new_tyme_zone(callback: types.CallbackQuery):
    """Выбор нового часового пояса"""
    logging.info('select_new_tyme_zone')
    user_id = int(callback.from_user.id)
    new_time_zone = int(str(callback.data).split('MSK')[1])

    await user_requests.update_time_zone(user_id, new_time_zone)

    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.time_zone_buttons(user_data['time_zone'])
    await callback.message.edit_text('💜 Выбери свой часовой пояс для напоминаний', reply_markup=markup)


###########################################################
### Изменение даты послежней менстр или рождения малыша ###
###########################################################


@router.callback_query(F.data.startswith('user-settings-change-date'))
async def change_date(callback: types.CallbackQuery):
    """Изменение даты последней меструации/рождения малыша"""
    logging.info('change_date')
    current_month = datetime.now().month
    current_year = datetime.now().year
    user_id = int(callback.from_user.id)

    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.days_buttons(current_month, current_year)

    if user_data['mom_or_not']:
        text = '💜 Введи дату рождения малыша'
    else:
        text = '💜 Введи дату последней менструации'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('edit-mom-start-date_'))
async def pagination(callback: types.CallbackQuery):
    """Пагинация даты"""
    logging.info('pagination')
    current_month = int(str(callback.data).split('_')[1])
    current_year = int(str(callback.data).split('_')[2])
    user_id = int(callback.from_user.id)

    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.days_buttons(current_month, current_year)

    if user_data['mom_or_not']:
        text = '💜 Введи дату рождения малыша'
    else:
        text = '💜 Введи дату последней менструации'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('edit-date-settings_'))
async def delect_new_date(callback: types.CallbackQuery):
    """Выбор новой даты"""
    logging.info('delect_new_date')
    user_id = int(callback.from_user.id)
    year = int(str(callback.data).split('_')[1])
    month = int(str(callback.data).split('_')[2])
    day = int(str(callback.data).split('_')[3])

    days, week = await utils.calculate_days(year, month, day)

    if days != -1:
        await user_requests.update_days_and_weeks(days, week, user_id)

        user_data = await user_requests.get_user_data(user_id)
        date = await utils.calculate_date(user_data['days'])
        markup = await settings_keyboard.settings_buttons(user_data['mom_or_not'])

        if user_data['mom_or_not']:  # Для мам
            text = (f'💜 Настройки\n\n'
                    f'Период - я уже родила\n'
                    f'Дата рождения малыша - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        else:  # Для беременных
            text = (f'💜 Настройки\n\n'
                    f'Период - я еще не родила\n'
                    f'Дата последней менструации - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)
    else:
        await callback.answer('Выбрана некорректная дата, попробуйте еще раз ❌')


############################################
############ Изменение периода #############
############################################


@router.callback_query(F.data == 'user-settings-change-period')
async def edit_period(callback: types.CallbackQuery):
    """Изменение периода"""
    logging.info('edit_period')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.edit_period_buttons(user_data['mom_or_not'])
    await callback.message.edit_text('💜 Выбери свой период', reply_markup=markup)


@router.callback_query(F.data.startswith('edit-mom-status_'))
async def get_new_status(callback: types.CallbackQuery, state: FSMContext):
    """Выбор нового статутса"""
    logging.info('get_new_status')
    user_id = int(callback.from_user.id)
    status_string = str(callback.data).split('_')[1]
    status = False if status_string == 'False' else True
    current_month = datetime.now().month
    current_year = datetime.now().year

    markup = await settings_keyboard.days_period_buttons(current_month, current_year)
    user_data = await user_requests.get_user_data(user_id)
    if user_data['mom_or_not']:
        text = '💜 Введи дату рождения малыша'
    else:
        text = '💜 Введи дату последней менструации'

    await state.update_data(status=status)
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('edit-period-mom-start-date_'))
async def pagination_period(callback: types.CallbackQuery):
    """Пагинация даты для смены периода"""
    logging.info('pagination_period')
    current_month = int(str(callback.data).split('_')[1])
    current_year = int(str(callback.data).split('_')[2])
    user_id = int(callback.from_user.id)

    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.days_period_buttons(current_month, current_year)

    if user_data['mom_or_not']:
        text = '💜 Введи дату рождения малыша'
    else:
        text = '💜 Введи дату последней менструации'
    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data.startswith('edit-period-date-settings_'))
async def select_date_for_new_period(callback: types.CallbackQuery, state: FSMContext):
    """Получение новой даты при смене периода"""
    logging.info('select_date_for_new_period')
    user_id = int(callback.from_user.id)
    year = int(str(callback.data).split('_')[1])
    month = int(str(callback.data).split('_')[2])
    day = int(str(callback.data).split('_')[3])

    state_data = await state.get_data()
    days, week = await utils.calculate_days(year, month, day)

    if days != -1:
        await user_requests.update_days_and_weeks(days, week, user_id)
        await user_requests.update_user_status(user_id, state_data['status'])

        user_data = await user_requests.get_user_data(user_id)
        date = await utils.calculate_date(user_data['days'])
        markup = await settings_keyboard.settings_buttons(user_data['mom_or_not'])
        main_markup = await start_keyboard.main_user_buttons(state_data['status'])

        if user_data['mom_or_not']:  # Для мам
            text = (f'💜 Настройки\n\n'
                    f'Период - я уже родила\n'
                    f'Дата рождения малыша - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        else:  # Для беременных
            text = (f'💜 Настройки\n\n'
                    f'Период - я еще не родила\n'
                    f'Дата последней менструации - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        await callback.message.delete()
        await callback.message.answer('Данные сохранены ✅', reply_markup=main_markup)
        await callback.message.answer(text=text, reply_markup=markup)

    else:
        await callback.answer('Выбрана некорректная дата, попробуйте еще раз ❌')


###############################################
############ Настройка подписки ###############
###############################################


@router.callback_query(F.data == 'user-settings-change-subscription')
async def subscription_settings(callback: types.CallbackQuery):
    """Настройка подписки"""
    logging.info('subscription_settings')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    markup = await settings_keyboard.subscription_buttons()
    tarif_name = await user_requests.get_subcription_name_by_type(user_data['subscription_type'])

    text = (f'💜 Твоя подписка: {tarif_name}\n'
            f'💜 Подписка активна до {user_data["subscription_date_end"]}')

    await callback.message.edit_text(text=text, reply_markup=markup)


@router.callback_query(F.data == 'change-subscription-type')
async def change_subscription_type(callback: types.CallbackQuery):
    """Изменение типа подписки"""
    logging.info('change_subscription_type')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    pro_tarif_name = await user_requests.get_subcription_name_by_type('pro')
    dafault_tarif_name = await user_requests.get_subcription_name_by_type('standart')
    markup = await settings_keyboard.select_new_subscription_type(user_data['subscription_type'], pro_tarif_name, dafault_tarif_name)

    await callback.message.edit_text('💜 Выбери тариф', reply_markup=markup)


@router.callback_query(F.data.startswith('select-new-tarif-type-user_'))
async def select_new_tarif_type(callback: types.CallbackQuery):
    """Выбор нового тарифного плана"""
    logging.info('select_new_tarif_type')
    new_type = str(callback.data).split('_')[1]
    old_type = 'pro' if new_type == 'standart' else 'standart'
    user_id = int(callback.from_user.id)
    tarif_data = await user_requests.get_tarifs_data(new_type)

    new_payment = {
        'user_id': user_id,
        'cost': tarif_data['cost'],
        'comment': f'Смена тарифного плана c {old_type} на {new_type}'
    }

    index = await user_requests.add_new_payment(new_payment)
    link = await utils.create_payment_link(new_payment['cost'], index)
    markup = await settings_keyboard.go_to_pay_or_back(link)

    text = ('💜 Обращаем твое внимание, что при смене тарифного плана срок действия тарифа начинается с момента оплаты'
            ' а не суммируется с текущим\n\n'
            'Если ты согласна с условиями то жми на кнопку для оплаты 👇')

    await callback.message.edit_text(text=text, reply_markup=markup)


####################################
##### Простая оплата подписки ######
####################################


@router.callback_query(F.data == 'user-go-to-pay')
async def basic_pay(callback: types.CallbackQuery, state: FSMContext):
    """Простая оплата подписки"""
    logging.info('basic_pay')
    user_id = int(callback.from_user.id)
    user_data = await user_requests.get_user_data(user_id)
    tarif_data = await user_requests.get_tarifs_data(user_data['subscription_type'])

    new_payment = {
        'user_id': user_id,
        'cost': tarif_data['cost'],
        'comment': f'Продление тарифа'
    }

    index = await user_requests.add_new_payment(new_payment)
    link = await utils.create_payment_link(new_payment['cost'], index)
    markup = await settings_keyboard.go_to_pay_or_back_main(link)

    text = (f'💜 Твоя подписка активна до {user_data["subscription_date_end"]}\n\n'
            f'Ссылка на оплату для продления подписки 👇')

    await callback.message.edit_text(text=text, reply_markup=markup)


#######################################
####### Реферальная программа #########
#######################################


@router.callback_query(F.data == 'referal-data-user')
async def refaral(callback: types.CallbackQuery):
    """Реферальная программа"""
    logging.info('refaral')
    user_id = int(callback.from_user.id)
    invite_data = await user_requests.get_user_referal(user_id)
    markup = await settings_keyboard.back_button()

    text = (f'💜 Ваша ссылка для приглашения: \n'
            f'<code>https://t.me/{config.tg_bot.bot_username}?start=ref_{user_id}</code>\n')

    if invite_data:
        text += '\nВаши приглашенные пользователи:\n'
        for user_data in invite_data:
            text += f'{invite_data.index(user_data) + 1}) {user_data["name"]} {user_data["username"]}\n'

    text += '\nПри приглашении подруги вы получите 2 недели бесплатно'

    await callback.message.edit_text(text=text, reply_markup=markup)


####################################
##### Обработка кнопок назад #######
####################################


@router.callback_query(F.data.startswith('settings-user-back_'))
async def back_buttons(callback: types.CallbackQuery):
    """Обработка кнопок назад"""
    logging.info('back_buttons')
    flag = str(callback.data).split('_')[1]

    if flag == 'main':
        user_id = int(callback.from_user.id)
        user_data = await user_requests.get_user_data(user_id)
        date = await utils.calculate_date(user_data['days'])
        markup = await settings_keyboard.settings_buttons(user_data['mom_or_not'])

        if user_data['mom_or_not']:  # Для мам
            text = (f'💜 Настройки\n\n'
                    f'Период - я уже родила\n'
                    f'Дата рождения малыша - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        else:  # Для беременных
            text = (f'💜 Настройки\n\n'
                    f'Период - я еще не родила\n'
                    f'Дата последней менструации - {date}\n'
                    f'Подписка - {user_data["subscription_type"]}, активна до {user_data["subscription_date_end"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)

    if flag == 'tarif-settings':
        user_id = int(callback.from_user.id)
        user_data = await user_requests.get_user_data(user_id)
        markup = await settings_keyboard.subscription_buttons()
        tarif_name = await user_requests.get_subcription_name_by_type(user_data['subscription_type'])

        text = (f'💜 Твоя подписка: {tarif_name}\n'
                f'💜 Подписка активна до {user_data["subscription_date_end"]}')

        await callback.message.edit_text(text=text, reply_markup=markup)

    if flag == 'select-new-tarif':
        user_id = int(callback.from_user.id)
        user_data = await user_requests.get_user_data(user_id)
        pro_tarif_name = await user_requests.get_subcription_name_by_type('pro')
        dafault_tarif_name = await user_requests.get_subcription_name_by_type('standart')
        markup = await settings_keyboard.select_new_subscription_type(user_data['subscription_type'], pro_tarif_name, dafault_tarif_name)

        await callback.message.edit_text('💜 Выбери тариф', reply_markup=markup)




















@router.callback_query(F.data == '---')
async def scip(callback: types.CallbackQuery):
    await callback.answer()

















