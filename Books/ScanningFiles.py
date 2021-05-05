import csv
import os

def ScanningFilePath(s):
    s = os.listdir(path=s)
    return s

def ScanningFiles():
    a = ScanningFilePath("C:\\Users\gibne\Библиотека\Антон Павлович Чехов")
    print(a, "\n")

    with open("books.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for file in a:
            file_writer.writerow([file])

if __name__ == "__main__":
    ScanningFiles()