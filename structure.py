import tkinter as tk
from tkinter import ttk

class LoginFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login!")

    def init_components(self):
        self.frame = tk.Frame(self, width=int(self.winfo_width()*0.5), height=int(self.winfo_height()*0.5))
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 
        self.frame.pack(fill=tk.BOTH)
        self.login_button = self.make_button("Login")

    def make_button(self,name:str):
        button = tk.Button(self.frame, text=name, command=self.open_main)
        button.pack(side="left")
        return button
    
    def run(self):
        self.init_components()
        self.mainloop()
    
    def open_main(self,*args):
        main = MainFrame(self)
        main.run()

class MainFrame(tk.Tk):
    def __init__(self, old_frame:tk.Tk) -> None:
        super().__init__()
        self.title("Main Program")
        self.old = old_frame

    def init_components(self):
        self.frame = tk.Frame(self)
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 
        self.frame.pack(fill=tk.BOTH)

    def run(self):
        self.old.destroy()
        self.init_components()
        self.mainloop()


if __name__ == "__main__":
    test = LoginFrame()
    test.run()
