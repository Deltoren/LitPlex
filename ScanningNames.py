import csv
import os

def ScanningPath(s):
    s = os.listdir(path=s)
    return s

def ScanningNames():
    a = ScanningPath(input("Введите путь к корневой папке "))
    print(a, "\n")

    with open("library.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for dir in a:
            file_writer.writerow([dir])

    with open("library.csv", encoding='utf-8') as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter=",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            print(row[0])
            count += 1
        print(f'Всего в файле {count + 1} строк.')
