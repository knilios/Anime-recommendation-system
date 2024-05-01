import tkinter as tk

class WindowFrame(tk.Tk):
    def init(self, title:str):
        '''
        param: title :
        '''
        super.__init__()
        self.title(title)

    def init_basic_components(self):
        self.frame = tk.Frame(self)
    
    def run(self):
        self.init_basic_components()
        self.mainloop()

