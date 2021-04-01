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

    data = dict()

    name = author_page.select_one('table.infobox > tbody > tr > th').getText()
    data["Имя"] = name

    career_a = author_page.select('[data-wikidata-property-id="P106"] > a')
    if career_a:
        career = [a.get('title') for a in career_a]
        data["Род деятельности"] = career

    date_of_birthday = author_page.select_one('[data-wikidata-property-id="P569"]').getText()
    if "[" in date_of_birthday:
        date_of_birthday = date_of_birthday[:date_of_birthday.index("[")]
    data['Дата рождения'] = date_of_birthday

    language_a = author_page.select('[data-wikidata-property-id="P1412"] > a')
    if language_a:
        language = [a.get('title') for a in language_a]
        data['Язык произведений'] = language

    genres_a = author_page.select('[data-wikidata-property-id="P136"] > a')
    if genres_a:
        genres = [a.get('title') for a in genres_a]
        data['Жанр'] = genres

    return data


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
        print(get_info_wikipedia(author))


if __name__ == '__main__':
    main()
