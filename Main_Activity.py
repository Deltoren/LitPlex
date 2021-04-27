import kivy
import ScanningNames
import csv
import os
import Pasring.ParsingAuthor

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty

import SingleAuthor
from SingleAuthor import SingleAuthorApp

authorLayout = Builder.load_file("authorLayout.kv")
fileLayoutMacket = Builder.load_file("fileLayout.kv")

mainLayout = BoxLayout()
fileLayout = fileLayoutMacket


class ProgramApp(App):
    def build(self):
        mainLayout.add_widget(authorLayout)
        mainLayout.add_widget(fileLayout)
        return mainLayout

    def on_press_buttonUpload(self):
        fileLayout.clear_widgets()
        ScanningNames.ScanningNames()
        with open("./data.csv", encoding='utf-8') as r_file:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(r_file)
            # Считывание данных из CSV файла
            count = 0
            for row in file_reader:
                if count > 5:
                    break
                count += 1
                info = 'Имя: ' + row['name']
                if row['careers']:
                    info += '\n' + 'Род деятельности: ' + ', '.join(row['careers'].split(','))
                if row['date_of_birthday']:
                    info += '\n' + 'Дата рождения: ' + row['date_of_birthday']
                if row['languages']:
                    info += '\n' + 'Языки произведений: ' + ', '.join(row['languages'].split(','))
                if row['genres']:
                    info += '\n' + 'Жанры: ' + ', '.join(row['genres'].split(','))
                btn = Button(text=info)
                btn.bind(on_press=self.on_press_button)
                fileLayout.add_widget(btn)
        Pasring.ParsingAuthor.start_search()

    def on_press_button(self, instance):
        mainLayout.clear_widgets()
        ProgramApp().stop()
        SingleAuthor.main()

if __name__ == "__main__":
    ProgramApp().run()
