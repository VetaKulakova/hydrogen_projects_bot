import matplotlib.pyplot as plt
from db import df as projects_data
import os
PATH_TO_PLOTS = '/Users/elizavetakulakova/Desktop/GAZPROM_CPS/Bots/namesbot/bots/hydrogen_projects_bot/PLOTS'


def list_for_rate(list_of_smth):
    duplicates = []
    quantity = []
    for item in list_of_smth:
        if list_of_smth.count(item) > 1 and item not in duplicates:
            duplicates.append(item)
            
    for item in duplicates:
        quantity.append(int(list_of_smth.count(item))) 
        
    rate = dict(zip(duplicates, quantity))       
    return rate

years_full_list = list_for_rate(list(projects_data['Date online']))
countries_full_list = list_for_rate(list(projects_data['Country']))


sorted_countries = sorted(countries_full_list.items(), key=lambda x: x[1], reverse=True)[:20]
sorted_countries = sorted_countries[-1::-1]
countries, projects = zip(*sorted_countries)

sorted_years = sorted(years_full_list.items(), key=lambda x: x[1], reverse=True)
years, projects_y = zip(*sorted_years)

def countries_plot(SAVE_PATH):
    # Строим столбчатую диаграмму
    fig, ax = plt.subplots(figsize=(20, 8), dpi=80)

    # настройка градиента
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    # Нормализуем значения количества проектов для создания градиента
    norm = Normalize(vmin=min(projects), vmax=max(projects))
    # Создаем градиентную цветовую карту от #56B9F2 до #002033
    cmap = LinearSegmentedColormap.from_list('custom', ['#56B9F2', '#002033'], N=256)
    # Преобразуем нормализованные значения в цвета из градиента
    colors = [cmap(norm(value)) for value in projects]

    ax.bar(countries, projects, color=colors)
    ax.set_xlabel('Страна', fontsize=14)
    ax.set_ylabel('Количество проектов', fontsize=14)
    ax.set_title('Распределение стран по количеству проектов', fontsize=16)
    ax.tick_params(axis='x', color = '#D9D9D9')
    ax.tick_params(axis='y', color = '#D9D9D9')

    # Добавляем подписи на столбцах
    for i, value in enumerate(projects):
        ax.text(i, value + 0.1, str(value), ha='center',  va = 'bottom', fontsize=12)
    ax.text(-1, 197, r'Источник: International Energy Agency, 2023', fontsize=11, color = '#6A7880')

    # Изменяем цвет рамки (границы) подложки
    ax.spines['bottom'].set_color('#D9D9D9')
    ax.spines['top'].set_color('#D9D9D9')
    ax.spines['right'].set_color('#D9D9D9')
    ax.spines['left'].set_color('#D9D9D9')
    
    # Проверка существования папки сохранения и создание, если не существует
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    # Сохранение графика в файл
    file_path = os.path.join(SAVE_PATH, 'plot.png')
    plt.savefig(file_path)
    
    # Очистка текущего графика
    plt.clf()
    
    return file_path


    

def years_plot(SAVE_PATH):
    fig, ax = plt.subplots(figsize=(20, 8), dpi=80)
    # Определяем цвета для каждого столбика
    colors = ['#56B9F2' if year < 2024 else ('#1476C6' if year == 2024 else '#C4C4C4') for year in years]

    ax.bar(years, projects_y, color=colors)
    ax.set_xlabel('Год', fontsize=14)
    ax.set_ylabel('Количество проектов', fontsize=14)
    ax.set_title('Ввод проектов по годам', fontsize=16)
    ax.tick_params(axis='x', color = '#D9D9D9')
    ax.tick_params(axis='y', color = '#D9D9D9')
    plt.text(x=2030, y=240, s = r'Источник: International Energy Agency, 2023', fontsize=11, color = '#6A7880')
    plt.xticks(years, rotation=60, fontsize=12)
    
    # Добавляем подписи на столбцах
    for i, value in enumerate(projects_y):
        plt.text(years[i], value + 0.1, str(value), ha='center', va='bottom', fontsize=11)

    # Изменяем цвет рамки (границы) подложки
    ax.spines['bottom'].set_color('#D9D9D9')
    ax.spines['top'].set_color('#D9D9D9')
    ax.spines['right'].set_color('#D9D9D9')
    ax.spines['left'].set_color('#D9D9D9')
        
    # Проверка существования папки сохранения и создание, если не существует
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    # Сохранение графика в файл
    file_path = os.path.join(SAVE_PATH, 'plot2.png')
    plt.savefig(file_path)
    
    # Очистка текущего графика
    plt.clf()
    
    return file_path