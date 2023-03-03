import tkinter as tk

import Components.MainPage as m

class BaseMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # устанавливаем параметры фона
        self.configure(bg='#5e5970')

        label = tk.Label(self, text="This is the BASIC MODE")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(m.MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)