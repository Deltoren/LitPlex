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

authorLayout = Builder.load_file("authorLayout.kv")
fileLayoutMacket = Builder.load_file("fileLayout.kv")

fileLayout = fileLayoutMacket

class ProgramApp(App):
    def build(self):
        mainLayout = BoxLayout()
        mainLayout.add_widget(authorLayout)
        mainLayout.add_widget(fileLayout)
        return mainLayout


if __name__ == "__main__":
    ProgramApp().run()