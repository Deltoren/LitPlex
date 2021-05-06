from time import time
import requests
from bs4 import BeautifulSoup
import threading
import csv
import psutil
import os


lock = threading.Lock()
thread_number = psutil.cpu_count()


def save(data):
    with open('data.csv', 'r+', encoding='UTF-8') as f:
        field_names = ['src_name', 'name', 'careers', 'date_of_birthday', 'languages', 'genres']
        writer = csv.DictWriter(f, fieldnames=field_names)
        reader = csv.DictReader(f, fieldnames=field_names)
        exist_authors = [i['src_name'] for i in reader]
        for author in data:
            if author['src_name'] not in exist_authors:
                writer.writerow(author)


def load():
    with open('../library.csv', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='\n')
        return [row[0] for row in reader]


def parse(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')


def custom_author():
    with lock:
        while True:
            name = input('Введите имя автора: ')
            if not os.path.exists(f'/Users/Admin/Downloads/Библиотека/{name}'):
                os.mkdir(f'/Users/Admin/Downloads/Библиотека/{name}')
                break
            else:
                print('Автор существует')

        career = input('Род деятельности (через ","): ')
        date_of_birthday = input('Дата рождения: ')
        language = input('Языки произведений (через ","): ')
        genres = input('Жанры произведений (через ","): ')
        author = {'name': name}
        if career:
            author['careers'] = career
        author['date_of_birthday'] = date_of_birthday
        if language:
            author['languages'] = language
        if genres:
            author['genres'] = genres
        save([author])
    pass


def get_info_wikipedia():

    while True:

        with lock:
            if pool:
                author_name = pool.pop()
                search_url = 'https://ru.wikipedia.org/w/index.php?search=' \
                             + '+'.join(author_name.split(' ')) \
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
                author = {'src_name': author_name, 'name': name}
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


def start_search():
    global thread_number

    author_arr = load()

    # Проверка на существование информации о авторе в системе
    with open('data.csv', mode='r', encoding='UTF-8') as f:
        field_names = ['src_name', 'name', 'careers', 'date_of_birthday', 'languages', 'genres']
        reader = csv.DictReader(f, fieldnames=field_names)
        exist_author = [i['src_name'] for i in reader]
        author_arr = [author for author in author_arr if author not in exist_author]

    for author in author_arr:
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

    #start_search(author_list)
    #print(data_wikipedia)
    #save(data_wikipedia)
    start_search()
    save(data_wikipedia)
    print(data_wikipedia)
    with open("data.csv", encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        print([row for row in reader])


if __name__ == '__main__':
    main()
