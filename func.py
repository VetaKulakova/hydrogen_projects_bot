import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

from db import df

country = df['Country']

# функция возвращает список всех стран без повторов
def list_of_countries(full_countries):
    countries = []
    c = list(full_countries)
    for item in c:
        if c.count(item) not in countries:
            countries.append(item)
    return countries

# функция для построения графика 
def countries_plot():
    fig, ax = plt.subplots(figsize=(40,15)) # поле для графика
    ax.grid() # сетка
    duplicates = list_of_countries(country)
    c = list(country)
    
    for item in duplicates:
        ax.bar(item, c.count(item))
        
    plt.xticks(rotation=60)
    plt.savefig('rate.png')
    
# функция составления рейтинга стран
def country_rate(country):
    quantity =[]
    duplicates = list_of_countries(country)
    c = list(country)
    
    for item in duplicates:
        quantity.append(int(c.count(item)))
    rate = dict(zip(duplicates, quantity))
    rating = []
    for i, (k, v) in enumerate(sorted(rate.items(), key=lambda n: n[1], reverse=True), 1):
        rating.append(f'{i}. {k} - {v}')
        
    return rating[:10]


import pycountry
def get_country(code):
    ru = pycountry.countries.get(alpha_3=code)
    return (ru)

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
