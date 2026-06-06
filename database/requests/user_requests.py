from database.models import (async_session, Users, Tarifs, WeeksTextsBer,
                             WeeksTextsMom, Reviews, Challenges, UsersChallenges, Diary,
                             Payments, Referal, UserRemindsDate, UserRemindsOneDay,
                             UserRemindsIntervals)
from sqlalchemy import select, or_, and_, delete, func, case, cast, Integer, String
from datetime import datetime, timedelta
import logging


async def get_user_data(user_id: int) -> dict:
    """Получение информации о пользователе"""
    logging.info('get_user_data')
    async with async_session() as session:
        user_data = await session.scalar(select(Users).where(Users.user_id == user_id))
        return user_data.__dict__



async def check_user(user_id: int) -> bool:
    """Проверка наличия пользователя в бд"""
    logging.info('check_user')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        if user:
            return user.__dict__
        else:
            return False


async def get_tarifs_data(flag: str) -> dict:
    """Получение данных о тарифе"""
    logging.info('get_tarifs_data')
    async with async_session() as session:
        # flag = standart/pro
        tarif_data = await session.scalar(select(Tarifs).where(Tarifs.tarif_type == flag))
        return tarif_data.__dict__


async def add_new_user(data: dict, user_id: int, username: str) -> None:
    """Добавление нового пользователя"""
    logging.info('add_new_user')
    async with async_session() as session:
        date_now = datetime.now()
        date_of_end = (date_now + timedelta(days=3)).strftime('%d.%m.%Y')

        new_user = Users(
            user_id=user_id,
            username=username,
            name=data['name'],
            week=data['week'],
            days=data['days'],
            mom_or_not=data['mom_or_not'],
            subscription_type=data['subscription_type'],
            subscription_date_end=date_of_end,
            time_zone=data['time_zone']
        )
        session.add(new_user)
        await session.commit()


async def get_text_by_days_cnt(days_cnt: int, type: str) -> str:
    """Получение текста в зависимости от дня беременности"""
    logging.info('get_text_by_days_cnt')
    async with async_session() as session:
        if type == 'mom':
            text = await session.scalar(select(WeeksTextsMom.text).where(WeeksTextsMom.day == days_cnt))
            return text
        else:
            text = await session.scalar(select(WeeksTextsBer.text).where(WeeksTextsBer.day == days_cnt))
            return text


async def select_reviews_to_watch() -> list:
    """Получение отзывово для просмотра"""
    logging.info('select_reviews_to_watch')
    async with async_session() as session:
        reviews_data = await session.scalars(select(Reviews).where(Reviews.moderation == True))
        if reviews_data:
            reviews_data = reviews_data.all()
            return reviews_data[::-1]
        else:
            return []


async def check_user_review(user_id: int) -> bool:
    """Проверка на то, оставил ли пользователь отзыв"""
    logging.info('check_user_review')
    async with async_session() as session:
        check = await session.scalar(select(Reviews).where(Reviews.user_id == user_id))
        if check:
            return True
        else:
            return False


async def add_new_review(user_id: int, username: str, review_data: dict) -> None:
    """Добавление нового отзыва"""
    logging.info('add_new_review')
    async with async_session() as session:
        new_review = Reviews(
            user_id=user_id,
            username=username,
            grade=review_data['grade'],
            comment=review_data['comment']
        )
        session.add(new_review)
        await session.commit()


async def get_challenges_by_status(status: str, week: int) -> list:
    """Получение заданий"""
    logging.info('get_challenges_by_status')
    async with async_session() as session:
        challenges = await session.scalars(select(Challenges).where(Challenges.category == status, Challenges.week == week))
        if challenges:
            return challenges.all()
        else:
            return []


async def get_user_completed_challenges(user_id: int) -> list:
    """Получение выполненых пользователем заданий"""
    logging.info('get_user_completed_challenges')
    async with async_session() as session:
        completed_challenges = await session.scalars(select(UsersChallenges.task_id).where(UsersChallenges.user_id == user_id))
        if completed_challenges:
            return completed_challenges.all()
        else:
            return []


async def user_completed_task(user_id: int, task_id: int) -> None:
    """Отметка что пользователь выполнил задание"""
    logging.info('user_completed_task')
    async with async_session() as session:
        task = await session.scalar(select(Challenges).where(Challenges.id == task_id))
        user_data = await session.scalar(select(Users).where(Users.user_id == user_id))

        # Добавляем пользователю баллы
        user_data.bonus_cnt += task.bonus_cnt

        #Добавляем задачу как выполненную
        new_complited_task = UsersChallenges(
            user_id=user_id,
            task_id=task_id
        )
        session.add(new_complited_task)

        await session.commit()


async def user_uncompleted_task(user_id: int, task_id: int) -> None:
    """Отметка что пользователь выполнил задание"""
    logging.info('user_completed_task')
    async with async_session() as session:
        task = await session.scalar(select(Challenges).where(Challenges.id == task_id))
        user_task = await session.scalar(select(UsersChallenges).where(UsersChallenges.task_id == task_id))
        user_data = await session.scalar(select(Users).where(Users.user_id == user_id))

        # Убрираем пользователю баллы
        user_data.bonus_cnt -= task.bonus_cnt

        # Удаляем задачу
        await session.delete(user_task)

        await session.commit()


async def get_diary_by_week(user_id: int, week: int) -> dict:
    """Получение данных о заполнении дневника"""
    logging.info('get_diary_by_week')
    async with async_session() as session:
        diary_data = await session.scalar(select(Diary).where(Diary.user_id == user_id, Diary.week == week))
        if diary_data:
            return diary_data.__dict__
        else:
            return {}


async def insert_diary_data(user_id: int, week: int, part: str, value: str) -> None:
    """Обновление данных о дневнике"""
    logging.info('insert_diary_data')
    async with async_session() as session:
        diary_data = await session.scalar(select(Diary).where(Diary.user_id == user_id, Diary.week == week))
        if diary_data:
            if part == 'photo':
               diary_data.photo = value
            if part == 'mood':
                diary_data.mood = value
            if part == 'bad-point':
                diary_data.bad_point = value
            if part == 'good-point':
                diary_data.good_point = value

        else:
            if part == 'photo':
                new_diary = Diary(
                    user_id=user_id,
                    week=week,
                    photo=value
                )
            if part == 'mood':
                new_diary = Diary(
                    user_id=user_id,
                    week=week,
                    mood=value
                )
            if part == 'bad-point':
                new_diary = Diary(
                    user_id=user_id,
                    week=week,
                    bad_point=value
                )
            if part == 'good-point':
                new_diary = Diary(
                    user_id=user_id,
                    week=week,
                    good_point=value
                )
            session.add(new_diary)

        await session.commit()


async def get_photos_diary(user_id: int) -> list:
    """Получение фотографий живота по неделям"""
    logging.info('get_photos_diary')
    async with async_session() as session:
        photos = await session.scalars(select(Diary).where(Diary.user_id == user_id))
        if photos:
            return photos.all()
        else:
            return []


async def update_time_zone(user_id: int, time_zone: int) -> None:
    """Обновление часового пояса"""
    logging.info('update_time_zone')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        user.time_zone = time_zone
        await session.commit()


async def update_days_and_weeks(days: int, week: int, user_id: int) -> None:
    """Обновление дней и недель пользователя"""
    logging.info('update_days_and_weeks')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        user.week = week
        user.days = days
        await session.commit()


async def update_user_status(user_id: int, status: bool) -> None:
    """Изменение стаутса пользователя мама/не мама"""
    logging.info('update_user_status')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        user.mom_or_not = status
        await session.commit()


async def get_subcription_name_by_type(type: str) -> str:
    """Получение названия пописки по ее типу"""
    logging.info('get_subcription_name_by_type')
    async with async_session() as session:
        tarif_name = await session.scalar(select(Tarifs.name).where(Tarifs.tarif_type == type))
        return tarif_name


async def add_new_payment(data: dict) -> int:
    """Добавление нового платежа и получение его индекса"""
    logging.info('add_new_payment')
    async with async_session() as session:
        new_payment = Payments(**data)
        session.flush()
        index = new_payment.id
        await session.commit()
        return index


async def get_user_referal(user_id: int) -> list:
    """Получение списка рефералов"""
    logging.info('get_user_referal')
    async with async_session() as session:
        invitee_data = await session.scalar(select(Referal.user_id_invitee).where(Referal.user_id_inviter == user_id))
        if invitee_data:

            users_data = []
            invitee_data = invitee_data.all()
            for user_id in invitee_data:
                user_data = await session.scalar(select(Users).where(Users.user_id == user_id))
                users_data.append({
                    'user_id': user_id,
                    'username': user_data['username'],
                    'name': user_data['name']
                })

            return user_data

        else:
            return []


async def add_new_remind(data: dict) -> None:
    """Добавление нвого напоминания"""
    logging.info('add_new_remind')
    async with async_session() as session:
        if data['time_type'] == 'Интервальное напоминание':
            new_remind = UserRemindsIntervals(
                user_id=data['user_id'],
                comment=data['comment'],
                category=data['category'],
                days=data['days'],
                times=data['selected_times']
            )

        if data['time_type'] == 'Определенная дата':
            new_remind = UserRemindsDate(
                user_id=data['user_id'],
                comment=data['comment'],
                category=data['category'],
                date=data['date'],
                time=data['selected_times']
            )

        if data['time_type'] == 'Раз в день':
            new_remind = UserRemindsOneDay(
                user_id=data['user_id'],
                comment=data['comment'],
                category=data['category'],
                time=data['selected_times']
            )

        session.add(new_remind)
        await session.commit()


async def get_my_reminds_by_category(user_id: int, category: str) -> list:
    """Получение списка напомианний пользователя по категории"""
    logging.info('get_my_reminds_by_category')
    async with async_session() as session:
        if category == 'interval':
            remind_data = await session.scalars(select(UserRemindsIntervals).where(UserRemindsIntervals.user_id == user_id))

        elif category == 'one':
            remind_data = await session.scalars(select(UserRemindsOneDay).where(UserRemindsOneDay.user_id == user_id))

        else:
            remind_data = await session.scalars(select(UserRemindsDate).where(UserRemindsDate.user_id == user_id))

        if remind_data:
            return remind_data.all()
        else:
            return []


async def get_remind_by_index_and_category(category: str, index: str) -> list:
    """Получение напоминания по категории и индексу"""
    logging.info('get_remind_by_index_and_category')
    async with async_session() as session:
        if category == 'interval':
            remind_data = await session.scalar(select(UserRemindsIntervals).where(UserRemindsIntervals.id == index))

        elif category == 'one':
            remind_data = await session.scalar(select(UserRemindsOneDay).where(UserRemindsOneDay.id == index))

        else:
            remind_data = await session.scalar(select(UserRemindsDate).where(UserRemindsDate.id == index))

        return remind_data.__dict__


async def delete_remind(category: str, index: str) -> None:
    """Удаление напоминания"""
    logging.info('delete_remind')
    async with async_session() as session:
        if category == 'interval':
            remind_data = await session.scalar(select(UserRemindsIntervals).where(UserRemindsIntervals.id == index))

        elif category == 'one':
            remind_data = await session.scalar(select(UserRemindsOneDay).where(UserRemindsOneDay.id == index))

        else:
            remind_data = await session.scalar(select(UserRemindsDate).where(UserRemindsDate.id == index))

        await session.delete(remind_data)
        await session.commit()














