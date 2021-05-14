import kivy
import ScanningNames
import csv
import os
import kivy
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
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import StringProperty


class BooksApp(App):
    def build(self):
        mainBL = BoxLayout()
        return mainBL

if __name__ == "__main__":
    BooksApp().run()