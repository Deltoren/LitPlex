import csv
import os

def ScanningPath(s):
    s = os.listdir(path=s)
    return s

def ScanningNames():
    a = ScanningPath("C:\\Users\gibne\Библиотека")

    # Исключение "скрытых" папок
    a = [name for name in a if name[0] != '.']

    print(a, "\n")

    with open("library.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for dir in a:
            file_writer.writerow([dir])
