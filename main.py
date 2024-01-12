from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

# пользовательские
import func 
from keyboards import start_kb, calculations_kb, statistic_kb, stat_back_kb
from msgs import START_MSG, CALC_MSG, STAT_MSG, PLOT_1_CAPTION, PLOT_2_CAPTION
import statistic_module

# настройка бота
TOKEN_API = "TOKEN" # токен бота (нужно указать свой)
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


# точка входа в диалог с ботом
@dp.message_handler(commands="start")
async def start(msg: Message):
    await msg.answer(START_MSG, reply_markup=start_kb())

# ГЛАВНОЕ МЕНЮ
# обработка нажатия кнопки "Аналитика" главного меню
@dp.message_handler(Text(equals="Аналитика"))
async def proc_analysys(msg: Message):
    await msg.answer(text=STAT_MSG, reply_markup = statistic_kb())
# обработка нажатия кнопки "Аналитика" главного меню
@dp.message_handler(Text(equals="Калькулятор"))
async def proc_clac(msg: Message):
    await msg.answer(text=CALC_MSG, reply_markup=calculations_kb())


# КАЛЬКУЛЯТОР
# Функция для рассчета массы через ввод объема, температуры и давления.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 1')
async def process_calculation_1(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода объема
        await bot.send_message(callback_query.from_user.id, "Введите объем:")
        await state.set_state("volume") # сохранение статуса для построения цепочки последовательного ввода данных
    except ValueError:
        # обработка ошибки ввода
        await bot.send_message("Пожалуйста, введите корректное число для объема.")

# сохранение данных объема и ввод давления
@dp.message_handler(state="volume")
async def process_volume(message: types.Message, state: FSMContext):
    try:
        volume = float(message.text)
        await state.update_data(volume=volume)
        await message.answer("Введите давление:")
        await state.set_state("pressure")
    except ValueError:
        await bot.send_message("Пожалуйста, введите корректное число для давления.")

# сохранение данных давления и ввод температуры
@dp.message_handler(state="pressure")
async def process_pressure(message: types.Message, state: FSMContext):
    try:
        pressure = float(message.text)
        await state.update_data(pressure=pressure)
        await message.answer("Введите температуру:")
        await state.set_state("temperature")
    except ValueError:
        await bot.send_message("Пожалуйста, введите корректное число для температуры.")

# сохранение температуры и вызов функции рассчета массы
@dp.message_handler(state="temperature")
async def process_temperature(message: types.Message, state: FSMContext):
    temperature = float(message.text)
    data = await state.get_data()
    volume = data.get("volume")
    pressure = data.get("pressure")

    # Вызываем функцию calculator_1 для расчетов
    result = func.calculator_1(volume, temperature, pressure)
    await message.answer(f"Масса: {result}")

    # Сбрасываем состояние
    await state.finish()
    
    

# Функция для рассчета объема через массу.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 2')
async def process_calculation_2(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода массы
        await bot.send_message(callback_query.from_user.id, "Введите массу:")
        await state.set_state("mass")
    except ValueError:
        await bot.send_message("Пожалуйста, введите корректное число для массы.")

# сохранение введенной массы и вызов функции расчета давления
@dp.message_handler(state="mass")
async def process_mass(message: types.Message, state: FSMContext):
    mass = float(message.text)
    # Вызываем функцию calculator_2 для расчетов
    result = func.calculator_2(mass)
    await message.answer(f"Объем: {result}")

    # Сбрасываем состояние
    await state.finish()



# Функция для рассчета массы через объем.
# обработка нажатия на инлайн-кнопку выбора типа расчета
@dp.callback_query_handler(lambda c: c.data == 'calc button 3')
async def process_calculation_3(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query.id)
        # запрос ввода объема
        await bot.send_message(callback_query.from_user.id, "Введите объем:")
        await state.set_state("volume1")
    except ValueError:
        await bot.send_message("Пожалуйста, введите корректное число для объема.")

# сохранение введенного объема и вызов функции расчета массы 
@dp.message_handler(state="volume1")
async def process_vol1(message: types.Message, state: FSMContext):
    vol1 = float(message.text)
    # Вызываем функцию calculator_2 для расчетов
    result = func.calculator_2(vol1)
    await message.answer(f"Масса: {result}")

    # Сбрасываем состояние
    await state.finish()


# АНАЛИТИЧЕСКИЙ МОДУЛЬ

import os

# Путь к папке, где будут сохраняться графики
SAVE_PATH = '/Users/elizavetakulakova/Desktop/GAZPROM_CPS/Bots/namesbot/bots/hydrogen_projects_bot'

# обработка нажатия на инлайн-кнопку выбора графика "Распределение проектов по странам"
@dp.callback_query_handler(lambda c: c.data == 'stat_button_1')
async def send_plot1(callback_query: types.CallbackQuery):
    # вызов функции построения графика
    file_path = statistic_module.countries_plot(SAVE_PATH)
    
    await bot.answer_callback_query(callback_query.id)
    # Отправка графика через телеграм-бота
    await bot.send_photo(callback_query.from_user.id, photo=open(file_path, 'rb'), reply_markup=stat_back_kb, caption=PLOT_1_CAPTION)
    # Удаление файла после отправки (по желанию)s
    os.remove(file_path)
        
# обработка нажатия на инлайн-кнопку выбора графика "Распределение проектов по странам"
@dp.callback_query_handler(lambda s: s.data == 'stat_button_2')
async def send_plot2(callback_query1: types.CallbackQuery):
    # вызов функции построения графика
    file_path = statistic_module.years_plot(SAVE_PATH)
    
    await bot.answer_callback_query(callback_query1.id)
    # Отправка графика через телеграм-бота
    await bot.send_photo(callback_query1.from_user.id, photo=open(file_path, 'rb'), reply_markup=stat_back_kb, caption=PLOT_2_CAPTION)
    # Удаление файла после отправки (по желанию)
    os.remove(file_path)
    
# обработка нажатия на инлайн-кнопку "Назад" к меню аналитического блока
@dp.callback_query_handler(lambda b: b.data == 'stat_back')
async def back_to_stat(callback_query1: types.CallbackQuery):
    await bot.answer_callback_query(callback_query1.id)
    await bot.send_message(callback_query1.from_user.id, text=STAT_MSG, reply_markup = statistic_kb())


#ЗАПУСК БОТА
if __name__ == '__main__':
    storage = MemoryStorage()
    dp.storage = storage
    executor.start_polling(dp, skip_updates=True, on_startup=print('Бот запущен'))