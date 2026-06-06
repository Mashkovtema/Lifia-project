import asyncio
import logging
import ssl

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from notify_admin import on_startup_notify
from database.models import async_main
from config_data.config_data import Config, load_config

from handlers.sheduler_handlers.add_days_and_weeks import add_days_and_weeks_func
from handlers import start_handler
from handlers.admin_handlers import (reminders_handler, ai_token_handler, tarifs_handler, reviews_hander,
                                     ai_study_handler, users_handler, chelenges_handler, mail_handler)

from handlers.user_handlers import (reviews_handler, preparation_recovery_handler, pregnancy_diary_handler,
                                    baby_handler, settings_handler, reminder_handler)

# Инициализируем logger
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,

        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    sheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='23', minute='0', args=(-1,)) # Калининград
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='0', minute='0', args=(0,)) # Москва
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='1', minute='0', args=(1,)) # Самара
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='2', minute='0', args=(2,)) # Екатеринбург
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='3', minute='0', args=(3,)) # Омск
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='4', minute='0', args=(4,)) # Красноярск
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='5', minute='0', args=(5,)) # Иркутск
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='6', minute='0', args=(6,)) # Якутск
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='7', minute='0', args=(7,)) # Владивосток
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='8', minute='0', args=(8,)) # Магадан
    sheduler.add_job(add_days_and_weeks_func, 'cron', hour='9', minute='0', args=(9,)) # Камчатка
    sheduler.start()

    #Регистрация роутеров
    # Старт
    dp.include_router(start_handler.router)

    # Админ
    dp.include_router(reminders_handler.router)
    dp.include_router(ai_token_handler.router)
    dp.include_router(tarifs_handler.router)
    dp.include_router(reviews_hander.router)
    dp.include_router(ai_study_handler.router)
    dp.include_router(mail_handler.router)
    dp.include_router(users_handler.router)
    dp.include_router(chelenges_handler.router)

    # Пользователь
    dp.include_router(reviews_handler.router)
    dp.include_router(preparation_recovery_handler.router)
    dp.include_router(pregnancy_diary_handler.router)
    dp.include_router(baby_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(reminder_handler.router)


    await on_startup_notify(bot=bot)
    await async_main()

    # web_app = web.Application()
    # web_app.router.add_post("/webhook", handle_webhook)
    # web_app['bot'] = bot
    #
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # try:
    #     ssl_context.load_cert_chain(
    #         certfile='/etc/letsencrypt/live/viva-test.mashkovtemaa.ru/fullchain.pem',
    #         keyfile='/etc/letsencrypt/live/viva-test.mashkovtemaa.ru/privkey.pem'
    #     )
    # except FileNotFoundError:
    #     logging.error("SSL certificate files not found.  HTTPS will not work.")
    #     ssl_context = None
    #
    # runner = web.AppRunner(web_app)
    # await runner.setup()
    #
    # site = web.TCPSite(runner, "0.0.0.0", 7000, ssl_context=ssl_context)
    # await site.start()
    # logging.info('Webhook server started on port 8000 with HTTPS')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
