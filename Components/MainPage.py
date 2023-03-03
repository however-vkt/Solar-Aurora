import tkinter as tk

import Components.BasicMode as b
import Components.ProMode as p

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # устанавливаем параметры фона
        self.configure(bg='#5e5970')

        # метка - выбор режима
        label = tk.Label(self, text="Выберите режим работы", font='Times 28', bg='#5e5970')
        label.pack(padx=100, pady=50)

        # кнопка - переход к базовому уровню
        button_basic = tk.Button(
            self,
            bg="#a29bb8",
            height=10, width=10,
            text="Базовый", font='Times 14',
            command=lambda: controller.show_frame(b.BaseMode),
        )
        button_basic.pack(side="left", fill=tk.BOTH, padx=15, pady=15, ipadx=25, ipady=25, expand=True)

        # кнопка - переход к профессиональному уровню
        button_pro = tk.Button(
            self,
            bg="#a29bb8",
            height=10, width=10,
            text="Профессиональный", font='Times 14',
            command=lambda: controller.show_frame(p.ProMode),
        )
        button_pro.pack(side="right", fill=tk.BOTH, padx=15, pady=15, ipadx=25, ipady=25, expand=True)