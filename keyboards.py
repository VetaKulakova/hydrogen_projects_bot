from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# стартовая клавиатура с выбором модуля бота (аналитика и калькулятор)
def start_kb():
    start_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_menu_kb.add(KeyboardButton("Аналитика"), KeyboardButton("Калькулятор"))
    return start_menu_kb

def calculations_kb():
    vpt_btn = InlineKeyboardButton('V, P, T -> m', callback_data='calc button 1')
    tp_m_btn = InlineKeyboardButton('Const(P, T), m -> V', callback_data='calc button 2')
    tp_v_btn = InlineKeyboardButton('Const(P, T), V -> m', callback_data='calc button 3')
    calc_inline_kb = InlineKeyboardMarkup().add(vpt_btn, tp_m_btn, tp_v_btn)
    return calc_inline_kb

def statistic_kb():
    countries_btn = InlineKeyboardButton('Распределение проектов по странам', callback_data='stat_button_1')
    years_btn = InlineKeyboardButton('Распределение проектов по годам', callback_data='stat_button_2')
    stat_inline_kb = InlineKeyboardMarkup(row_width=1).add(countries_btn, years_btn)
    return stat_inline_kb


back_btn_stat = InlineKeyboardButton('Назад', callback_data='stat_back')
stat_back_kb = InlineKeyboardMarkup().add(back_btn_stat)


def back_to_calc_kb():
    back_btn_calc = InlineKeyboardButton('Назад', callback_data='calc_back')
    calc_back_kb = InlineKeyboardMarkup().add(back_btn_calc)
    return calc_back_kb
