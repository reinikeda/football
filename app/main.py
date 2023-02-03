from tkinter import *


class MainApp():
    def __init__(self, main):
        self.main = main
        self.test = Label(self.main, text='THIS IS TEST TEXT').pack()