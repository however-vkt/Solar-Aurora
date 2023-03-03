import tkinter as tk

import Components.MainPage as m
class ProMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # устанавливаем параметры фона
        self.configure(bg='#5e5970')

        label = tk.Label(self, text="This is the PRO MODE")
        label.pack(padx=10, pady=10)

        button_return = tk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(m.MainPage)
        )
        button_return.pack(side="bottom", fill=tk.X)

        # кнопка для работы с данными таблицы
        button_tableRefresh = tk.Button(
            self,
            text="Обновить данные таблицы",
            # command=BackAurora.takeInfo(),
        )
        button_tableRefresh.pack(side="bottom", fill=tk.X)