from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton
                           )


# стартовая клавиатура с выбором модуля бота (аналитика и калькулятор)
def start_kb():
    start_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_menu_kb.add(
        KeyboardButton("💧 Краткая справка о водороде"),
        KeyboardButton("📊 Аналитика")
    ).add(
        KeyboardButton("🌐 Новости"),
        KeyboardButton("🧮 Водородный калькулятор")
    )
    return start_menu_kb


def calculations_kb():
    vpt_btn = InlineKeyboardButton('Массу водорода (зная P, V, T)',
                                   callback_data='calc button 1')
    tp_m_btn = InlineKeyboardButton('Объем водорода '
                                    '(при стандартных условиях)',
                                    callback_data='calc button 2')
    tp_v_btn = InlineKeyboardButton('Массу водорода '
                                    '(при стандартных условиях)',
                                    callback_data='calc button 3')
    calc_inline_kb = InlineKeyboardMarkup(row_width=1).add(vpt_btn,
                                                           tp_m_btn,
                                                           tp_v_btn)
    return calc_inline_kb


def statistic_kb():
    countries_btn = InlineKeyboardButton('Распределение проектов по странам',
                                         callback_data='stat_button_1')
    years_btn = InlineKeyboardButton('Ввод проектов по годам',
                                     callback_data='stat_button_2')
    stat_inline_kb = InlineKeyboardMarkup(row_width=1).add(countries_btn,
                                                           years_btn)
    return stat_inline_kb


def stat_back_kb():
    back_btn_stat = InlineKeyboardButton('Назад', callback_data='stat_back')
    stat_back_kb = InlineKeyboardMarkup().add(back_btn_stat)
    return stat_back_kb


def back_to_calc_kb():
    back_btn_calc = InlineKeyboardButton('Назад', callback_data='calc_back')
    calc_back_kb = InlineKeyboardMarkup().add(back_btn_calc)
    return calc_back_kb


def administrator_kb():
    admin_btn = InlineKeyboardButton('Кнопочка админа (coming soon...)',
                                     callback_data='adm_btn')
    admin_kb = InlineKeyboardMarkup().add(admin_btn)
    return admin_kb
