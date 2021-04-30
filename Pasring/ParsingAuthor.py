from time import time
from random import randrange as rnd
import requests
from bs4 import BeautifulSoup
import threading
import csv
import psutil
import wikipedia
import matplotlib.pyplot as plt


wikipedia.set_lang('ru')

lock = threading.Lock()
thread_number = psutil.cpu_count()


def save(data):
    with open('data.csv', 'w', encoding='UTF-8') as f:
        field_names = ['name', 'careers', 'date_of_birthday', 'languages', 'genres']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for author in data:
            writer.writerow(author)


def load():
    with open('../library.csv', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='\n')
        return [row[0] for row in reader]


def parse(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')


def get_info_wikipedia_api():

    while True:

        with lock:
            if pool:
                author = pool.pop()

                try:
                    author_url = wikipedia.page(author).url
                except wikipedia.exceptions.PageError as e:
                    print(e)
                    continue

            else:
                break

        try:

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
                print(name, 'is done')
                author = {'name': name}
                if career_a:
                    author['careers'] = ",".join(career)
                author['date_of_birthday'] = date_of_birthday
                if language_a:
                    author['languages'] = ",".join(language)
                if genres_a:
                    author['genres'] = ",".join(genres)
                data_wikipedia.append(author)

        except requests.exceptions.ConnectionError:
            print('Connection Error')
            continue


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
                print(name, 'is done')
                author = {'name': name}
                if career_a:
                    author['careers'] = ",".join(career)
                author['date_of_birthday'] = date_of_birthday
                if language_a:
                    author['languages'] = ",".join(language)
                if genres_a:
                    author['genres'] = ",".join(genres)
                data_wikipedia.append(author)

        except requests.exceptions.ConnectionError:
            print('Connection Error')
            continue


data_wikipedia = []
pool = set()


def time_test():
    global pool

    time1_ax = []
    time2_ax = []
    count_ax = []

    for n in range(1, len(load())):

        author_set = set(load())

        count_ax.append(n)

        author_set_buf = set([author_set.pop() for i in range(n)])

        # Парсинг

        pool = author_set_buf.copy()
        thread_arr = []

        start = time()

        for i in range(thread_number):
            thread = threading.Thread(target=get_info_wikipedia)
            thread_arr.append(thread)
            thread.start()

        for thread in thread_arr:
            thread.join()

        end = time()
        time1_ax.append(end - start)

        thread_arr.clear()
        pool.clear()
        data_wikipedia.clear()

        # Парсинг + API

        pool = author_set_buf.copy()
        thread_arr = []

        start = time()

        for i in range(thread_number):
            thread = threading.Thread(target=get_info_wikipedia_api)
            thread_arr.append(thread)
            thread.start()

        for thread in thread_arr:
            thread.join()

        end = time()
        time2_ax.append(end - start)

        thread_arr.clear()
        pool.clear()
        data_wikipedia.clear()

    plt.plot(count_ax, time1_ax, label="Парсинг")
    plt.plot(count_ax, time2_ax, label="Парсинг + API")
    plt.xlabel('кол-во авторов')
    plt.ylabel('время, сек')
    plt.title('Сравнение времени работы алгоритмов')

    plt.legend()
    plt.show()


def start_search():
    global thread_number

    for author in load():
        pool.add(author)

    thread_arr = []

    for i in range(thread_number):
        thread = threading.Thread(target=get_info_wikipedia_api)
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

    #start_search(author_list)
    #print(data_wikipedia)
    #save(data_wikipedia)
    start_search()
    save(data_wikipedia)
    print(data_wikipedia)
    with open("data.csv", encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            info = 'Имя: ' + row['name']
            if row['careers']:
                info += '\n' + 'Род деятельности: ' + ', '.join(row['careers'].split(','))
            if row['date_of_birthday']:
                info += '\n' + 'Дата рождения: ' + row['date_of_birthday']
            if row['languages']:
                info += '\n' + 'Языки произведений: ' + ', '.join(row['languages'].split(','))
            if row['genres']:
                info += '\n' + 'Жанры: ' + ', '.join(row['genres'].split(','))
            print(info)


if __name__ == '__main__':
    # main()
    time_test()
