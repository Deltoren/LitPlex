import kivy

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

class ProgramApp(App):
    def build(self):
        mainLayout = BoxLayout()
        fileLayout = fileLayoutMacket
        for i in range(5):
            btn = Button(text="Александр Сергеевич Пушкин")
            btn.bind(on_press=self.on_press_button)
            fileLayout.add_widget(btn)
        mainLayout.add_widget(authorLayout)
        mainLayout.add_widget(fileLayout)
        return mainLayout

    def on_press_button(self, instance):
        print('Вы нажали на кнопку!')

if __name__ == "__main__":
    ProgramApp().run()
