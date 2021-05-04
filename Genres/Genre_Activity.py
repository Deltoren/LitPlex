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

mainLayout = BoxLayout()


class GenreApp(App):
    def build(self):
        return mainLayout


if __name__ == "__main__":
    GenreApp().run()