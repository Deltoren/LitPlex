import csv
import os

def ScanningFilePath(s):
    s = os.listdir(path=s)
    return s

def ScanningFiles():
    a = ScanningFilePath("C:\\Users\gibne\Библиотека\Антон Павлович Чехов")

    with open("books.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for file in a:
            file_writer.writerow([file])

    with open("books.csv", encoding='utf-8') as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(r_file, delimiter="\n")
        # Считывание данных из CSV файла
        count = 0
        for row in file_reader:
            print(row)

if __name__ == "__main__":
    ScanningFiles()