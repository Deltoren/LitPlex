from time import time
import requests
from bs4 import BeautifulSoup
import threading


lock = threading.Lock()
thread_number = 16


def parse(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')


def get_info_wikipedia():

    while True:

        with lock:
            if pool:
                author = pool.pop()
                search_url = 'https://ru.wikipedia.org/w/index.php?search=' \
                             + '+'.join(author.split(' ')) \
                             + '&title=Служебная%3AПоиск&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'
            else:
                break

        try:

            search_page = parse(search_url)
            author_url = search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a').get('href')

            author_url = 'https://ru.wikipedia.org' + author_url
            author_page = parse(author_url)

            name = author_page.select_one('table.infobox > tbody > tr > th').getText()

            career_a = author_page.select('[data-wikidata-property-id="P106"] > a')
            if career_a:
                career = [a.get('title') for a in career_a]

            date_of_birthday = author_page.select_one('[data-wikidata-property-id="P569"]').getText()
            if "[" in date_of_birthday:
                date_of_birthday = date_of_birthday[:date_of_birthday.index("[")]

            language_a = author_page.select('[data-wikidata-property-id="P1412"] > a')
            if language_a:
                language = [a.get('title') for a in language_a]

            genres_a = author_page.select('[data-wikidata-property-id="P136"] > a')
            if genres_a:
                genres = [a.get('title') for a in genres_a]

            with lock:
                data_wikipedia[name] = dict()
                if career_a:
                    data_wikipedia[name]['Род деятельности'] = career
                data_wikipedia[name]['Дата рождения'] = date_of_birthday
                if language_a:
                    data_wikipedia[name]['Язык произведений'] = language
                if genres_a:
                    data_wikipedia[name]['Жанр'] = genres

        except requests.exceptions.ConnectionError:
            print('Connection Error')
            continue


data_wikipedia = dict()
pool = set()


def start_search(author_list):
    global thread_number

    for author in author_list:
        pool.add(author)

    thread_arr = []

    for i in range(thread_number):
        thread = threading.Thread(target=get_info_wikipedia)
        thread_arr.append(thread)
        thread.start()

    for thread in thread_arr:
        thread.join()

    thread_arr.clear()
    pool.clear()


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

    start_search(author_list)
    print(data_wikipedia)


if __name__ == '__main__':
    main()
