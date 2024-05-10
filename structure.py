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
        self.backend = control.Control()
        self.filters_list = []

    def init_components(self):

        # Create a title label
        self.label = tk.Label(self, font=self.title_font, text="Show Recommendation Page")
        self.label.pack(anchor="center", side="top")

        # Make the window big enough
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}') 

        # create all frames
        self.main_frame = tk.Frame(self)
        self.left_frame = tk.Frame(self.main_frame)
        self.right_frame = tk.Frame(self.main_frame)
        self.upper_right_frame = tk.Frame(self.right_frame)
        self.lower_right_frame = tk.Frame(self.right_frame)
        self.chooser_frame = tk.Frame(self.upper_right_frame)
        self.button_frame = tk.Frame(self.upper_right_frame)

        # create a histogram
        self.histogram = vt.Histogram(self.left_frame)

        # create a filter bar and buttons
        self.filter_screen = vt.TreeView(self.upper_right_frame, ("Type of filter", "Attribute", "Value"))
        self.type1_option, self.type1_value = self.make_option_menu(self.chooser_frame, "Inclusive", ["Inclusive", "Exclusive"])
        self.type2_option, self.type2_value = self.make_option_menu(self.chooser_frame, "Genres", ["Genres", "Episodes", "Type"])
        self.type3_option, self.type3_value = self.make_option_menu(self.chooser_frame, "", ["1","2"])
        self.type4_option, self.type4_value = self.make_option_menu(self.chooser_frame, "", ["1","2"])
        self.type3_option.configure(state="disabled")
        self.type4_option.configure(state="disabled")
        self.add_button = tk.Button(self.button_frame, text="Add filter", command='')
        self.delete_button = tk.Button(self.button_frame, text="Delete", command='')
        self.go_button = tk.Button(self.button_frame, text="Search", comman="")

        # packing
        self.main_frame.pack(expand=True, side="top", fill="both")
        self.left_frame.pack(expand=True, side="left", fill="both")
        self.right_frame.pack(expand=True, side="left", fill="both")
        self.type1_option.pack(expand=True, side="left", fill="x")
        self.type2_option.pack(expand=True, side="left", fill="x")
        self.type3_option.pack(expand=True, side="left", fill="x")
        self.type4_option.pack(expand=True, side="left", fill="x")
        self.upper_right_frame.pack(expand=True, side="top", fill="both")
        self.lower_right_frame.pack(expand=True, side="top", fill="both")
        self.filter_screen.pack(expand=True, side="top", fill="both")
        self.chooser_frame.pack(expand=True, side="top")
        self.filter_screen.start()
        self.add_button.pack(expand=True, side="left")
        self.delete_button.pack(expand=True, side="left")
        self.button_frame.pack(expand=True, side="top", fill="both")
        self.histogram.pack(expand=True, side="top", fill="both")

        # histogram show
        _data = self.backend.get_data_for_histogram_page()["Score"].to_list()
        self.histogram.show(_data, 5, "The spread of the data", self.histogram.onClick(self.histogram_clicked_handler))

        # binding 
        self.type2_value.trace_add("write", self.type2_change_handler)

    def bind_chooser(self, event):
        """
        A method for binding the chooser tree.
        """
        # activate the button
        self.delete_button.configure(state="active")

        # Put the selected item into the selected item list
        try:
            item = self.filter_screen.tree.item(event.widget.selection()[0])
        except IndexError:
            # If item unselected, disable the button
            self.delete_button.configure(state="disabled")
            return
        for i in self.filters_list:
            if i == item["values"]:
                self.filters_list.remove(i)
                break

    def histogram_clicked_handler(self, bar_index, *args):
            # Get the index of the clicked bar
            print(int(bar_index))

    def type2_change_handler(self, *args):
        self.type3_value.set("")
        self.type3_option.configure(state="disabled")
        self.type4_value.set("")
        self.type4_option.configure(state="disabled")
        value = self.type2_value.get()
        if value == "Genres":
            self.type3_value.set("Action")
            self.type3_option.configure(state="normal")
            self.type3_option["menu"].delete(0, tk.END)
            for i in self.backend.get_unique_genre():
                command=tk._setit(self.type3_value, i)
                self.type3_option["menu"].add_command(label=i, command=command)
        elif value == "Type":
            self.type3_value.set("TV")
            self.type3_option.configure(state="normal")
            self.type3_option["menu"].delete(0, tk.END)
            for i in self.backend.get_unique_type():
                command=tk._setit(self.type3_value, i)
                self.type3_option["menu"].add_command(label=i, command=command)
        else:
            self.type3_value.set(0)
            self.type3_option.configure(state="normal")
            self.type4_value.set(0)
            self.type4_option.configure(state="normal")
            self.type3_option["menu"].delete(0, tk.END)
            self.type4_option["menu"].delete(0, tk.END)
            for i in range(300):
                command=tk._setit(self.type3_value, i)
                self.type3_option["menu"].add_command(label=i, command=command)
            for i in range(300):
                command=tk._setit(self.type4_value, i)
                self.type4_option["menu"].add_command(label=i, command=command)

    def add_button_handler(self, *args):
        _filters = [
            self.type1_value.get(),
            self.type2_value.get(),
            self.type3_value.get(),
            self.type4_value.get()
        ]
        for i in self.filters_list:
            if i[1] == "Episodes":
                return
            if i == _filters:
                return
        self.filters_list.append(_filters)

    def search_button_handler(self, *args):
        _data = self.backend.get_data_for_histogram_page(self.filters_list)
        []

    def show_histogram(self):
        pass

    def make_option_menu(self, parent, default_text:str, values:tuple):
        option_value = tk.StringVar(parent) 
        option_value.set(default_text) 
        option = tk.OptionMenu(parent, option_value, *values)
        return option, option_value

    def run(self):
        self.old.destroy()
        self.init_components()
        self.mainloop()


class PreferenceShows(Window):
    def __init__(self, old_window:tk.Tk):
        super().__init__()
        self.old = old_window
        self.prefered_list = ListDatabase("prefered_list")
        self.title_font = ("consolus", 25)
        self.normal_font = ("consolus", 16)
        self.backend = control.Control()

    def init_components(self):

        # create a label
        tk.Label(self, text="Edit your preference shows", font=self.title_font).pack(side='top')

        # Make the window big enough
        self.geometry(f'{int(self.winfo_screenwidth()*0.5)}x{int(self.winfo_screenheight()*0.5)}')

        # create frames
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)

        # create a search bar and chooser element
        self.string_var = tk.StringVar(self)
        self.string_var.trace_add("write", lambda name, index, mode, sv=self.string_var: self.change_in_entry_handler(self.string_var))
        self.search_bar = tk.Entry(self.right_frame, textvariable=self.string_var)
        self.chooser = vt.TreeView(self.right_frame, ("id", 'name'))
        self.shows = self.backend.get_show_from_part_of_name()

        # create a list view
        self.list_view = vt.EntryTextView(self.left_frame)

        # pack
        self.list_view.pack(side="top", fill="both", expand=True, anchor="center")
        show_name_list = [self.backend.get_show_by_id(float(i))["Name"].to_list()[0] for i in self.prefered_list.data]
        self.list_view.display(["The shows will be listed bellow.", "-----------------------"] + show_name_list)

        
        self.add_button = tk.Button(self.right_frame, text="Add", command=self.bind_button)

        self.search_bar.pack(expand=True,side="top", fill="x")
        self.chooser.pack(expand=True, side="top", fill="both")
        self.add_button.pack(expand=True, side="top", fill="both")
        self.add_button.configure(state="disabled")
        self.chooser.display(self.shows)
        self.chooser.start()

        self.left_frame.pack(side="left", expand=True, fill="both")
        self.right_frame.pack(side="left", expand=True, fill="both")
        
        # Bind
        self.chooser.bind(self.bind_chooser)
    
    def bind_chooser(self, event):
        """
        A method for binding the chooser tree.
        """
        # activate the button
        self.add_button.configure(state="active")

        # Put the selected item into the selected item list
        try:
            item = self.chooser.tree.item(event.widget.selection()[0])
        except IndexError:
            # If item unselected, disable the button
            self.add_button.configure(state="disabled")
            return
        self.selected_item = item["values"][0]
        
    def bind_button(self, *args):
        item = self.chooser.tree.item(self.chooser.tree.selection()[0])
        # print("item: ", item["values"][0])
        # print(self.backend.get_show_by_id(float(item["values"][0]))["Name"].to_list()[0])
        if item["values"][0] in self.prefered_list.data:
            self.prefered_list.delete(item["values"][0])
        else:
            self.prefered_list.data.append(item["values"][0])
        self.prefered_list.save_data()

        # Update the show list
        show_name_list = [self.backend.get_show_by_id(float(i))["Name"].to_list()[0] for i in self.prefered_list.data]
        self.list_view.display(show_name_list)

    def change_in_entry_handler(self, str_var:tk.StringVar):

        # Update self.shows the search bar chooser
        self.shows = self.backend.get_show_from_part_of_name(str_var.get())
        self.chooser.display(self.shows)
        
    def run(self):
        self.old.destroy()
        self.init_components()
        self.mainloop()
    


if __name__ == "__main__":
    test = MenuFrame()
    test.run()
