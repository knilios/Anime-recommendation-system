import tkinter as tk
from tkinter import ttk
import visualize_tools as vt
import control
import pandas as pd 
from csv_reader import *

class Window(tk.Tk):
    def init(self):
        super().__init__()
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)
    

class MenuFrame(Window):
    def __init__(self) -> None:
        super().__init__()
        self.title("Main Program")
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)


    def init_components(self) -> None:
        self.frame = tk.Frame(self)
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 
        self.frame.pack(fill=tk.BOTH, expand=True, side="right")
        self.frame2 = tk.Frame(self)
        self.frame2.pack(fill=tk.BOTH, expand=True, side="right")
        # Label
        self.label = self.make_label("Menu")
        self.label.pack(anchor="center")
        # menu's button
        self.button_scatter_win = self.make_button(self.frame, "Data Story Telling", self.button_scatter)
        self.button_exploration_win = self.make_button(self.frame, "Get a show recommendation", self.button_exploration)
        self.button_preference_win = self.make_button(self.frame, "Edit your preference shows", self.button_preference)
        self.button_scatter_win.pack(anchor="center", side="top")
        self.button_preference_win.pack(anchor="center", side="top")
        self.button_exploration_win.pack(anchor="center", side="top")
        self.button_preference_win.pack(anchor="center", side="top")

    def make_label(self, name:str) -> tk.Label:
        _label = tk.Label(self.frame, text=name, font=self.title_font)
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

    def button_exploration(self, *args):
        """Leads to the data exploration window"""
        exploration = DataExploration(self)
        exploration.run()
        
    def button_preference(self, *args):
        """Leads to the edit preference window
        """
        preference = PreferenceShows(self)
        preference.run()

    def run(self) -> None:
        self.init_components()
        self.mainloop()


class ScatterWindow(Window):
    def __init__(self, old_window:tk.Tk) -> None:
        super().__init__()
        self.title("Main Program")
        self.old = old_window
        self.font = ("consolus", 25)
        self.backend = control.Control()
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)


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


class DataExploration(Window):
    def __init__(self, old_window:tk.Tk):
        super().__init__()
        self.old = old_window
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)

    def init_components(self):

        # create all frames
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)
        self.upper_right_frame = tk.Frame(self.right_frame)
        self.lower_right_frame = tk.Frame(self.right_frame)

        # create a histogram
        self.histogram = vt.Histogram(self.right_frame)

        # create a filter bar
        self.filter_screen = vt.TreeView(self.upper_right_frame, ("Type of filter", "Attribute", "Value"))


        # packing
        self.left_frame.pack(expand=True, side="left", fill="both")
        self.right_frame.pack(expand=True, side="left", fill="both")


class PreferenceShows(Window):
    def __init__(self, old_window:tk.Tk):
        super().__init__()
        self.old = old_window
        self.prefered_list = ListDatabase("prefered_list")
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)

    def init_components(self):

        # create a label
        tk.Label(self, text="Edit your preference shows", font=self.title_font)

        # create frames
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)

        # create a search bar and chooser element
        self.search_bar = tk.Entry(self.right_frame)
        self.chooser = vt.TreeView(self.right_frame)
        self.add_button = tk.Button(self.right_frame, text="Add", command=self.bind_button)

        # TODO
        self.search_bar.pack(expand=True,side="top", fill="x")
        self.chooser.pack(expand=True, side="top", fill="x")
        self.add_button.pack(expand=True, side="top", fill="x")
        self.add_button.configure(state="disabled")
        
        # Bind
        self.chooser.bind(self.bind_chooser)
    
    def bind_chooser(self, event):
        """
        A method for binding the chooser tree.
        """
        # activate the button
        self.add_button.configure(state="active")

        # Put the selected item into the selected item list
        item = self.chooser.tree.item(event.widget.selection()[0])
        self.selected_item = item["values"][0]
        
    def bind_button(self, event, *args):
        # TODO
        # add self.selected_item to the prefered list
        pass
        print(event.widget.selection()[0])
        item = self.chooser.tree.item(event.widget.selection()[0])
        print("item: ", item["values"][0])
        
    def run(self):
        self.old.destroy()
        self.init_components()
        self.mainloop()
    


if __name__ == "__main__":
    test = MenuFrame()
    test.run()
