"""
Модуль расчета массы и объема водорода.
"""

R = 0.08206  # Gas constant, (liter * atm) / (K * mol).
M = 0.002  # Molar mass of hydrogen, kg / mol.
K_TEMP = 273  # Coef. for converting temperature from degrees Celsius to degrees Kelvin.
K_PRESS = 0.986923  # Coef. for converting pressure from bar to atm.
K_VALUE = 0.001  # Coef. for converting value from liters to cubic meters.


def calculator_1(value: float, 
                 temperature: float, 
                 pressure: float) -> str:
    # Функция № 1 для вычисления массы водорода (в кг.).
    # Пользователь вводит с интерфейса следующие параметры:
    # объем, л
    # температура, градусы Цельсия
    # давление, бар

    pressure = pressure * K_PRESS  # Converted pressure from bar to atm.
    temperature = temperature + K_TEMP  # Converted temperature from Celsia to Kelvin.

    mass = ((pressure * value * M)
            / (R * temperature))  # Clapeyron-Mendeleev equation.

    return f'{mass:.2f}'


def calculator_2(mass: float) -> str:
    # Функция № 2 для вычисления объема водорода (в м куб.) при стандартных условиях:
    # температура: 21 градус цельсия
    # давление: 1 атм
    # масса: вводится пользователем в кг.

    pressure = 1  # Давление, атм
    temperature = 21 + K_TEMP  # Температура, К

    value = ((mass * R * temperature)
             / (pressure * M))
    value = value * K_VALUE  # Перевод литров в м куб.

    return f'{value:.2f}'


def calculator_3(value: float) -> str:
    # Функция № 3 для вычисления массы водорода (в кг) при стандартных условиях:
    # температура: 21 градус цельсия
    # давление: 1 атм
    # объем: вводится пользователем в м куб.

    pressure = 1  # Давление, атм
    temperature = 21 + K_TEMP  # Температура, К
    value = value / K_VALUE  # Перевод м куб. в литры

    mass = ((pressure * value * M)
            / (R * temperature))  # Clapeyron-Mendeleev equation.

    return f'{mass:.2f}'
