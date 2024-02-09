from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
import logging
import os

# Пользовательские
from config import TOKEN_API, ADMIN_ID
import func
from keyboards import (
    start_kb, calculations_kb,
    statistic_kb, stat_back_kb,
    administrator_kb
)
from msgs import (
    START_MSG, CALC_MSG, STAT_MSG,
    PLOT_1_CAPTION, PLOT_2_CAPTION,
    HYDROGEN_INFO, ADMIN_MSG, HELP_MSG,
    CORRECT_MSG
)

import statistic_module
from news_module import news, URL_1, URL_2
from log_func import read_last_logs
from links import SAVE_PLOT_PATH

# настройка бота
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


# точка входа в диалог с ботом
@dp.message_handler(commands="start")
async def start(msg: Message):
    await msg.answer(START_MSG, reply_markup=start_kb())


# обработка функции администрирования
@dp.message_handler(commands="admin")
async def admin(msg: Message):
    if str(msg.from_user.id) == ADMIN_ID:
        mes = read_last_logs(filename="py_log.log")
        await msg.answer(text=(ADMIN_MSG+'\n'+mes),
                         reply_markup=administrator_kb())
    else:
        await msg.answer('Нет прав администрирования.')


# обработка функции help
@dp.message_handler(commands="help")
async def help(msg: Message):
    await msg.answer(HELP_MSG)


# ГЛАВНОЕ МЕНЮ
# обработка нажатия кнопки "Краткая справка о водороде" главного меню
@dp.message_handler(Text(equals="💧 Краткая справка о водороде"))
async def brief_hydrogen(msg: Message):
    await msg.answer(text=HYDROGEN_INFO, parse_mode=ParseMode.HTML)


# обработка нажатия кнопки "Аналитика" главного меню
@dp.message_handler(Text(equals="📊 Аналитика"))
async def proc_analysys(msg: Message):
    await msg.answer(text=STAT_MSG, reply_markup=statistic_kb())


# обработка нажатия кнопки "Аналитика" главного меню
@dp.message_handler(Text(equals="🧮 Водородный калькулятор"))
async def proc_clac(msg: Message):
    await msg.answer(text=CALC_MSG, reply_markup=calculations_kb())


# обработка нажатия кнопки "Новости" главного меню
@dp.message_handler(Text(equals="🌐 Новости"))
async def news_message(msg: Message):
    news1 = news(URL_1)
    news2 = news(URL_2)
    news1_message = (
        f"<b>Последние новости из мира водородной энергетики</b>\n\n"
        f"<a href='{news1['url']}'>{news1['title']}</a>\n"
        f"{news1['data']}\n\n"
        )
    news2_message = (
        f"<a href='{news2['url']}'>{news2['title']}</a>\n"
        f"{news2['data']}"
        )
    await msg.answer(text=news1_message + news2_message,
                     parse_mode=ParseMode.HTML)


# КАЛЬКУЛЯТОР
# Функция для рассчета массы через ввод объема, температуры и давления.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 1')
async def process_calculation_1(callback_query: types.CallbackQuery,
                                state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода объема
        await bot.send_message(callback_query.from_user.id,
                               text="Введите объем, л:")
        # сохранение статуса для построения цепочки послед. ввода данных
        await state.set_state("volume")
    except ValueError as e:
        # обработка ошибки ввода
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=CORRECT_MSG)


# сохранение данных объема и ввод давления
@dp.message_handler(state="volume")
async def process_volume(message: types.Message, state: FSMContext):
    try:
        volume = float(message.text)
        await state.update_data(volume=volume)
        await message.answer("Введите давление, бар:")
        await state.set_state("pressure")
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=message.from_user.id,
                               text=CORRECT_MSG)


# сохранение данных давления и ввод температуры
@dp.message_handler(state="pressure")
async def process_pressure(message: types.Message, state: FSMContext):
    try:
        pressure = float(message.text)
        await state.update_data(pressure=pressure)
        await message.answer("Введите температуру, градусы Цельсия:")
        await state.set_state("temperature")
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=message.from_user.id,
                               text=CORRECT_MSG)


# сохранение температуры и вызов функции рассчета массы
@dp.message_handler(state="temperature")
async def process_temperature(message: types.Message, state: FSMContext):
    try:
        temperature = float(message.text)
        data = await state.get_data()
        volume = data.get("volume")
        pressure = data.get("pressure")

        # Вызываем функцию calculator_1 для расчетов
        result = func.calculator_1(volume, temperature, pressure)
        await message.answer(f"Масса водорода: {result} кг")

        # Сбрасываем состояние
        await state.finish()
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=message.from_user.id,
                               text=CORRECT_MSG)


# Функция для рассчета объема через массу.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 2')
async def process_calculation_2(callback_query: types.CallbackQuery,
                                state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода массы
        await bot.send_message(callback_query.from_user.id,
                               text="Введите массу, кг:")
        await state.set_state("mass")
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=CORRECT_MSG)


# сохранение введенной массы и вызов функции расчета давления
@dp.message_handler(state="mass")
async def process_mass(message: types.Message, state: FSMContext):
    try:
        mass = float(message.text)
        # Вызываем функцию calculator_2 для расчетов
        result = func.calculator_2(mass)
        await message.answer(f"Объем водорода: {result} куб. м")

        # Сбрасываем состояние
        await state.finish()
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=message.from_user.id,
                               text=CORRECT_MSG)


# Функция для рассчета массы через объем.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 3')
async def process_calculation_3(callback_query: types.CallbackQuery,
                                state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода объема
        await bot.send_message(callback_query.from_user.id,
                               text="Введите объем, куб. м:")
        await state.set_state("volume1")
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=CORRECT_MSG)


# сохранение введенного объема и вызов функции расчета массы
@dp.message_handler(state="volume1")
async def process_vol1(message: types.Message, state: FSMContext):
    try:
        vol1 = float(message.text)
        # Вызываем функцию calculator_2 для расчетов
        result = func.calculator_2(vol1)
        await message.answer(f"Масса водорода: {result} кг")

        # Сбрасываем состояние
        await state.finish()
    except ValueError as e:
        logging.error(f"Ошибка ввода данных: {e}", exc_info=True)
        await bot.send_message(chat_id=message.from_user.id,
                               text=CORRECT_MSG)

# АНАЛИТИЧЕСКИЙ МОДУЛЬ
# Путь к папке, где будут сохраняться графики


# обработка нажатия на инлайн-кнопку выбора графика
# "Распределение проектов по странам"
@dp.callback_query_handler(lambda c: c.data == 'stat_button_1')
async def send_plot1(callback_query: types.CallbackQuery):
    # вызов функции построения графика
    file_path = statistic_module.countries_plot(SAVE_PLOT_PATH)
    await bot.answer_callback_query(callback_query.id)
    # Отправка графика через телеграм-бота
    await bot.send_photo(callback_query.from_user.id,
                         photo=open(file_path, 'rb'),
                         reply_markup=stat_back_kb(),
                         caption=PLOT_1_CAPTION)
    # Удаление файла после отправки (по желанию)
    os.remove(file_path)


# обработка нажатия на инлайн-кнопку выбора графика "Ввод проектов по годам"
@dp.callback_query_handler(lambda s: s.data == 'stat_button_2')
async def send_plot2(callback_query1: types.CallbackQuery):
    # вызов функции построения графика
    file_path = statistic_module.years_plot(SAVE_PLOT_PATH)
    await bot.answer_callback_query(callback_query1.id)
    # Отправка графика через телеграм-бота
    await bot.send_photo(callback_query1.from_user.id,
                         photo=open(file_path, 'rb'),
                         reply_markup=stat_back_kb(),
                         caption=PLOT_2_CAPTION)
    # Удаление файла после отправки (по желанию)
    os.remove(file_path)


# обработка нажатия на инлайн-кнопку "Назад" к меню аналитического блока
@dp.callback_query_handler(lambda b: b.data == 'stat_back')
async def back_to_stat(callback_query1: types.CallbackQuery):
    await bot.answer_callback_query(callback_query1.id)
    await bot.send_message(callback_query1.from_user.id,
                           text=STAT_MSG,
                           reply_markup=statistic_kb())

# ЗАПУСК БОТА
if __name__ == '__main__':
    storage = MemoryStorage()
    dp.storage = storage
    executor.start_polling(dp, skip_updates=True,
                           on_startup=print('Бот запущен'))
