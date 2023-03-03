import tkinter as tk

import Components.MainPage as m
import Components.BasicMode as b
import Components.ProMode as p

class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # добавление заголовка к окну
        self.wm_title("AuroraLight")

        # установление базовых размеров окна !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.wm_geometry("600x600")

        # установление иконки !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # self.iconbitmap(default="favicon.ico")

        # создание фрейма и назначение его контейнеру
        container = tk.Frame(self, height=600, width=600)
        # указываем region, куда упаковывается фрейм в root
        container.pack(side="top", fill="both", expand=True)

        # настройка расположения контейнера с помощью сетки (grid)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # создание словаря фреймов
        self.frames = {}
        # добавление компонентов в словарь
        for F in (m.MainPage, b.BaseMode, p.ProMode):
            frame = F(container, self)

            # класс windows действует как корневое окно для фреймов.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Использование метода для переключения фреймов
        self.show_frame(m.MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # поднимает текущий фрейм наверх
        frame.tkraise()