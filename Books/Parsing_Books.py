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
        field_names = ['name', 'genres']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for book in data:
            writer.writerow(book)

def load():
    with open('books.csv', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter='\n')
        return [row for row in reader]





if __name__ == '__main__':
    # main()
    print(psutil.cpu_count())

