from time import time
import requests
from bs4 import BeautifulSoup
import threading
import csv
import psutil


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


def init_modal_no_authors(folder_name):
    with lock:
        while True:
            answer = input('Create custom author (1) OR change folder\'s name (2): ')
            if answer in {'1', '2'}:
                if answer == '1':
                    print('init Изменить название')
                else:
                    print('init Создать кастомного автора')
                break


def init_modal_many_results(data):
    with lock:
        while True:
            print('\n'.join([f"{i + 1}. {author}" for (i, author) in enumerate(data)]))
            answer = input("Выберите подходящего вам автора: ")
            if answer.isdigit() and 0 < int(answer) < len(data) + 1:
                print("OK")
                return int(answer)
            else:
                print("init ВИ")
                return 0


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

            # Если не найдено ни одного автора
            if not search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a'):
                init_modal_no_authors(author)
                return 0

            author_url = search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a').get('href')

            # Если найдено несколько авторов
            if len(search_page.select('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a')) > 1:
                all_result = search_page.select('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a')
                result_arr = [] + [all_result[0]]
                result_arr_name = [all_result[0].getText()]
                for result in all_result[1:]:
                    for word in author.split(" "):
                        if word in result.getText():
                            result_arr.append(result)
                            result_arr_name.append(result.getText())
                if len(result_arr) == 1:
                    author_url = result_arr[0].get('href')
                else:
                    index = init_modal_many_results(result_arr_name)
                    if index:
                        author_url = result_arr[index - 1].get('href')
                    else:
                        return 0
            else:
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


def start_search():
    global thread_number

    for author in load():
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
    print(psutil.cpu_count())
