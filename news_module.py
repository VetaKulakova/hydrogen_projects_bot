from bs4 import BeautifulSoup
import requests

URL_1 = 'https://hydrogen.gazprom.ru/press/news/2021/12/roadmap/'
URL_2 = 'https://hydrogen.gazprom.ru/press/news/2021/10/agreement/'


def news(URL):
    url = URL
    page = requests.get(url)
    get_text = page.text
    soup = BeautifulSoup(get_text, "html.parser")
    for head in soup.find_all('h1'):
        title = head.get_text()
    date_of_news = []
    for dat in soup.find_all('time', class_='date'):
        date_of_news.append(dat.get_text())

    news_text = {'title': title,
                 'data': date_of_news[0],
                 'url': url}
    return news_text
