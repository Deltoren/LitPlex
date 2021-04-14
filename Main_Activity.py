import kivy
import ScanningNames
import csv
import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

authorLayout = Builder.load_file("authorLayout.kv")
fileLayoutMacket = Builder.load_file("fileLayout.kv")

fileLayout = fileLayoutMacket

class ProgramApp(App):
    def build(self):
        mainLayout = BoxLayout()
        mainLayout.add_widget(authorLayout)
        mainLayout.add_widget(fileLayout)
        return mainLayout

    def on_press_buttonUpdate(self):
        ScanningNames.ScanningNames()
        with open("library.csv", encoding='utf-8') as r_file:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.reader(r_file, delimiter=",")
            # Счетчик для подсчета количества строк и вывода заголовков столбцов
            count = 0
            # Считывание данных из CSV файла
            for row in file_reader:
                btn = Button(text=row[0])
                btn.bind(on_press=self.on_press_button)
                fileLayout.add_widget(btn)

    def on_press_button(self, instance):
        print("f")

if __name__ == "__main__":
    ProgramApp().run()
