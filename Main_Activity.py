import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty

main_activity = Builder.load_file("program.kv")

class MainScreen(BoxLayout):
    pass

class ProgramApp(App):
    def build(self):
        return main_activity

if __name__ == "__main__":
    ProgramApp().run()
