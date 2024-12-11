import config
from app.handler import router
from aiogram import Bot, Dispatcher
import asyncio


# Создаем объект класса bot и объект класса Dispatcher 
bot = Bot(config.API_KEY_TELEGRAM)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Запускам бота чтобы он работал бесконечно 
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')