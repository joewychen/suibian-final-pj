import tkinter as tk
import os
from PIL import ImageTk, Image
from lightfield import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_dropdown()
        self.create_widgets()
        self.create_canvas()
        self.lightfield = {}

    def create_dropdown(self):
        self.clicked = tk.StringVar()
        options = []
        with os.scandir("../scene/") as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    options.append(entry.name)
        if len(options) > 0: self.clicked.set(options[0])
        drop = tk.OptionMenu(self, self.clicked , *options )
        drop.pack()

    def create_widgets(self):
        def scale_labels(value):
            self.alpha.config(label=self.interval[int(value)])
        self.interval = [i * 0.2 + -5 for i in range(60)]
        self.alpha = tk.Scale(self, from_=0, to=len(self.interval) - 1, command=scale_labels,
          orient="horizontal", tickinterval=0.2, showvalue=False)
        self.radius = tk.Scale(self, from_=0, to=8, orient="horizontal")
        self.alpha.pack()
        tk.Label(self, text="alpha").pack()
        self.radius.pack()
        tk.Label(self, text="radius").pack()
        button = tk.Button(self , text = "OK" , command = self.show ).pack(side="bottom")

    def create_canvas(self):
        # iopen = Image.open("ball.png")
        # iopen = iopen.resize((450, 450))
        # img = ImageTk.PhotoImage(iopen)
        self.canvas = tk.Canvas(self, width = 600, height = 600)
        self.canvas.pack()
        # self.canvas.create_image(300,300,anchor = "center", image=img)
        # self.canvas.image = img

    def show(self):
        name = self.clicked.get()
        alpha = self.interval[self.alpha.get()]
        radius = self.radius.get()
        if name in self.lightfield:
            lf = self.lightfield[name]
        else:
            lf = Lightfield("../scene/" + name + "/", name)
        ret = lf.combine(alpha, radius)
        plt.imsave("one.png", ret)
        iopen = Image.open("one.png")
        iopen = iopen.resize((450, 450))
        img = ImageTk.PhotoImage(iopen)
        self.canvas.create_image(300,300,anchor = "center", image=img)
        self.canvas.image = img
        print("\nDone")

        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")
        #
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.pack(side="bottom")
        #
        # self.aa = tk.Button(self)
        # self.aa.pack(side="left")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
