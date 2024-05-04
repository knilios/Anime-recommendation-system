import tkinter as tk
from tkinter import ttk
import visualize_tools as vt
import control
import pandas as pd

class MenuFrame(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Main Program")
        self.font = ("consolus", 25)

    def init_components(self) -> None:
        self.frame = tk.Frame(self)
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 
        self.frame.pack(fill=tk.BOTH, expand=True, anchor="center")
        self.frame2 = tk.Frame(self)
        # Label
        self.label = self.make_label("Menu")
        self.label.pack(anchor="center")
        # menu's button
        self.button_scatter = self.make_button(self.frame, "Data Story Telling", self.button_scatter)
        self.button_scatter.pack(anchor="center", side="top")

    def make_label(self, name:str) -> tk.Label:
        _label = tk.Label(self.frame, text=name, font=self.font)
        _label.configure(justify="center")
        return _label
    
    def make_frame(self, parent:tk.Frame | tk.Tk) -> tk.Frame:
        frame = tk.Frame(parent)
    
    def make_button(self, parent:tk.Frame | tk.Tk, name:str, command) -> tk.Frame:
        button = tk.Button(parent, text=name, command=command)
        return button
    
    def button_scatter(self, *args):
        """Leads to the scatterplot window"""
        scatter = ScatterWindow(self)
        scatter.run()

    def run(self) -> None:
        self.init_components()
        self.mainloop()


class ScatterWindow(tk.Tk):
    def __init__(self, old_window:tk.Tk) -> None:
        super().__init__()
        self.title("Main Program")
        self.old = old_window
        self.font = ("consolus", 25)
        self.backend = control.Control()

    def init_components(self):
        self.right_frame = tk.Frame(self)
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 
        self.scatter = vt.ScatterChart(self)
        self.entry = vt.EntryTextView(self)
        self.scatter.display(*tuple(self.backend.get_scatter_plot()))
        self.scatter.pack(side="left", expand=True, fill="both")
        _key = tuple(self.backend.get_unique_genre() + ["All genres"])
        self.option = self.make_option_menu(self.right_frame, "All genres", _key)
        self.option.pack(side='top', fill='x')
        self.entry.pack(side="top", expand=True, fill="both")
        self.right_frame.pack(side="left")
        self.entry.display(self.create_descriptive(*tuple(self.backend.get_scatter_plot())))
        # bind the menu bar
        self.option_value.trace_add('write', self.change_in_menu)
        
    def make_option_menu(self, parent, default_text:str, values:tuple):
        self.option_value = tk.StringVar(parent) 
        self.option_value.set(default_text) 
        option = tk.OptionMenu(self, self.option_value, *values)
        return option
    
    def change_in_menu(self, *args):
        """Update the scatter plot and the descriptive statistic"""
        value = self.option_value.get()
        if value == "All genres":
            value = None
        scatter_plot_data = self.backend.get_scatter_plot(value)
        self.scatter.update(*tuple(scatter_plot_data))
        self.entry.display(self.create_descriptive(*tuple(scatter_plot_data)))

    def create_descriptive(self, score:pd.Series, dropr:pd.Series):
        des1 = score.describe()
        des2 = dropr.describe()
        key1 = des1.keys()
        key2 = des2.keys()
        return ["-----Score-----"] + [f"{i} : {des1[i]}" for i in key1] + ["-----Drop Rate-----"] + [f"{i} : {des2[i]}" for i in key2] + ["-----Correlation-----", f"Correlation : {score.corr(dropr)}"]

    def run(self):
        self.old.destroy()
        self.init_components()
        self.mainloop()

    


if __name__ == "__main__":
    test = MenuFrame()
    test.run()
