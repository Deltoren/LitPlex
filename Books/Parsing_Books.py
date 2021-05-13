from time import time
import requests
from bs4 import BeautifulSoup
import threading
import csv
import psutil

lock = threading.Lock()
thread_number = psutil.cpu_count()
data_wiki = []
pool = set()


def save(data):
    with open('book_data.csv', 'w', encoding='UTF-8') as f:
        field_names = ['name', 'genre']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for book in data:
            writer.writerow(book)

def load():
    with open('books.csv', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='\n')
        return [row[0] for row in reader]

def parse(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml')

def start_search():
    global thread_number

    for book in load():
        pool.add(book)

    thread_arr = []

    for i in range(thread_number):
        thread = threading.Thread(target=parsing)
        thread_arr.append(thread)
        thread.start()

    for thread in thread_arr:
        thread.join()

    thread_arr.clear()
    pool.clear()
    save(data_wiki)


def parsing():
    while True:
        with lock:
            if pool:
                book = pool.pop()
                format = book.split(".")[1]
                print(format)
                if format == "txt" or format == "fb2" or format == "epub" or format == "pdf":
                    book = book.split(".")[0]
                    search_url = 'https://ru.wikipedia.org/w/index.php?search=' \
                                 + '+'.join(book.split(' ')) \
                                 + '&title=Служебная%3AПоиск&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'
                else:
                    break
            else:
                break

        try:
            search_page = parse(search_url)
            book_url = search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                                     div.mw-search-result-heading > a').get('href')

            book_url = 'https://ru.wikipedia.org' + book_url
            book_page = parse(book_url)

            name = book_page.select_one('table.infobox > tbody > tr > th').getText()

            genre = book_page.select_one('[data-wikidata-property-id="P136"]').getText()
            if "[" in genre:
                genre = genre[:genre.index("[")]

            with lock:
                print(name, 'is done')
                book = {'name': name}
                if name:
                    book = {"name": name}

                if genre:
                    book = {"name": name, "genre": genre}
                data_wiki.append(book)

        except requests.exceptions.ConnectionError:
            print('Connection Error')
            continue

def main():
    start_search()

if __name__ == '__main__':
    main()
    print(psutil.cpu_count())

