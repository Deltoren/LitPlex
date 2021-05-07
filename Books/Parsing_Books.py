from time import time
import requests
from bs4 import BeautifulSoup
import threading
import csv
import psutil

lock = threading.Lock()
thread_number = psutil.cpu_count()


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
    books = load()
    data = []
    for book in books:
        data.append(parsing(book))

    save(data)


def parsing(book):
    book = book.split(".")[0]
    search_url = 'https://ru.wikipedia.org/w/index.php?search=' \
                 + '+'.join(book.split(' ')) \
                 + '&title=Служебная%3AПоиск&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'
    search_page = parse(search_url)
    book_url = search_page.select_one('div.searchresults > ul.mw-search-results > li.mw-search-result > \
                                             div.mw-search-result-heading > a').get('href')

    book_url = 'https://ru.wikipedia.org' + book_url
    book_page = parse(book_url)

    name = book_page.select_one('table.infobox > tbody > tr > th').getText()

    genre = book_page.select_one('[data-wikidata-property-id="P136"]').getText()
    if "[" in genre:
        genre = genre[:genre.index("[")]

    if name:
        data = {"name": name}

    if genre:
        data = {"name": name, "genre": genre}

    return data

def main():
    start_search()

if __name__ == '__main__':
    main()
    print(psutil.cpu_count())

