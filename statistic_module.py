import matplotlib.pyplot as plt
import io
from db import df as projects_data
import os
PATH_TO_PLOTS = '/Users/elizavetakulakova/Desktop/GAZPROM_CPS/Bots/namesbot/bots/hydrogen_projects_bot/PLOTS'


def dublicates(list_of_smth):
    duplicates = []
    for item in list_of_smth:
        if list_of_smth.count(item) > 1 and item not in duplicates:
            duplicates.append(item)
    return duplicates

countries_full = list(projects_data['Country'])
years_full = list(projects_data['Date online'])
 
countries = dublicates(countries_full)
years = dublicates(years_full)

def countries_plot(SAVE_PATH):
    # Создание и сохранение графика
    plt.subplots(figsize=(40,15)) # поле для графика
    
    for country in countries:
        plt.bar(country, countries_full.count(country))
    
    plt.grid() # сетка 
    plt.xticks(rotation=60)
    plt.title('Распределение стран по количеству проектов', fontdict={'size':46})
    plt.ylabel('Количество проектов')
    plt.xlabel('Страны')
    
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
    plt.subplots(figsize=(40,15)) # поле для графика
    
    for year in years:
        plt.bar(year, years_full.count(year))
    
    plt.grid() # сетка 
    plt.title('Распределение проектов по годам', fontdict={'size':46})
    plt.ylabel('Год')
    plt.xlabel('Количество')
    
    # Проверка существования папки сохранения и создание, если не существует
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    # Сохранение графика в файл
    file_path = os.path.join(SAVE_PATH, 'plot2.png')
    plt.savefig(file_path)
    
    # Очистка текущего графика
    plt.clf()
    
    return file_path
'''
import os 
import matplotlib.pyplot as plt
SAVE_PATH = '/Users/elizavetakulakova/Desktop/GAZPROM_CPS/Bots/namesbot/bots/hydrogen_projects_bot'

@dp.callback_query_handler(lambda plots: plots.data == 'stat button 1')
async def send_countries_plot(callback_query1: types.CallbackQuery):   
    # Создание и сохранение графика
    plt.subplots(figsize=(40,15)) # поле для графика
    plt.grid() # сетка
    for country in statistic_module.countries:
        plt.bar(country, statistic_module.countries_full.count(country))
    plt.xticks(rotation=60)
    
    # Проверка существования папки сохранения и создание, если не существует
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    # Сохранение графика в файл
    file_path = os.path.join(SAVE_PATH, 'plot.png')
    plt.savefig(file_path)
    
    # Очистка текущего графика
    plt.clf()

    # Отправка графика через телеграм-бота
    with open(file_path, 'rb') as photo:
        await bot.send_photo(callback_query1.from_user.id, photo=photo, caption=PLOT_1_CAPTION)

    # Удаление файла после отправки (по желанию)
    os.remove(file_path)
'''