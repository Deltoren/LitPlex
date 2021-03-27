from time import time
import requests
from bs4 import BeautifulSoup


def parse(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')


def get_info_wikipedia(author):
    search_url = 'https://ru.wikipedia.org/w/index.php?search=' \
                 + '+'.join(author.split(' ')) \
                 + '&title=Служебная%3AПоиск&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'

    search_page = parse(search_url)

    author_url = search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                         div.mw-search-result-heading > a').get('href')

    author_url = 'https://ru.wikipedia.org' + author_url
    author_page = parse(author_url)

    for block_info in author_page.select('table.infobox > tbody > tr'):
        title = block_info.select_one('th')
        if title:
            info = title.select_one('span')
            print(title)


def main():
    author_list = ['Федор Достоевский',
                   'Михаил Булгаков',
                   'Александр Пушкин',
                   'Лев Толстой',
                   'Николай Гоголь',
                   'Антон Чехов',
                   'Иван Тургенев',
                   'Александр Дюма',
                   'Эрих Мария Ремарк',
                   'Артур Конан Дойль',
                   'Виктор Гюго',
                   'Михаил Шолохов',
                   'Джек Лондон']

    for author in author_list:
        get_info_wikipedia(author)


if __name__ == '__main__':
    main()
