import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from math import ceil

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter.scrolledtext import ScrolledText

class Visualize(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self, new_data:list) -> None:
        pass #TODO create the update machanism


class Histogram(Visualize):
    #TODO Change this into a real histogram
    def __init__(self, parent, data_x:list, data_y:list, title:str, bar_clicked, ylabel:str=None):
        super().__init__(parent)
        self.bar_clicked = bar_clicked
        self.parent = parent
        #create a figure
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)
        # NavigationToolbar2Tk(self.figure_canvas, self)
        axes = self.figure.add_subplot()
        # create the barchart
        axes.bar(data_x, data_y)
        axes.set_title(title)
        if ylabel != None:
            axes.set_ylabel(ylabel)

    def start(self) -> None:
        self.figure_canvas.mpl_connect('button_press_event', self.bar_clicked)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class BoxPlot(Visualize):
    def __init__(self, parent, data_x:list, data_y:list, title:str, bar_clicked, ylabel:str=None):
        super().__init__(parent)
        self.bar_clicked = bar_clicked
        self.parent = parent
        #create a figure
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)
        # NavigationToolbar2Tk(self.figure_canvas, self)
        self.axes = self.figure.add_subplot()
        # create the barchart
        self.axes.bar(data_x, data_y)
        self.axes.set_title(title)
        if ylabel != None:
            self.axes.set_ylabel(ylabel)

    def start(self) -> None:
        """
        Draw the graph.
        """
        self.figure_canvas.mpl_connect('button_press_event', self.bar_clicked)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update(self, data_x:list, data_y:list):
        """
        Update the data in the box plot.
        :param data_x:  a list of 
        """
        self.axes.bar(data_x, data_y)


class TreeView(Visualize):
    """
    Create a clickable and scrollable treeview.
    """
    def __init__(self, parent, columns:tuple):
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for i in columns:
            self.tree.heading(i, text=str(i))
        # Create a scrollbar for the tree
        self.scrollbar = tk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        
    def start(self) -> None:
        """Make the tree visible (but not the frame that's containing it)"""
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def display(self, content:list) -> None:
        """Display specified list of contents.
        :param content: - a list of list containing a lines of data.
        """
        # Delete everything displaying at the moment
        for selected_item in self.tree.get_children():
            self.tree.delete(selected_item)
        # Fill the tree with new data
        for i in content:
            self.tree.insert('', tk.END, values=tuple(i))

    def bind(self, func) -> None:
        """Bind each lines of the tree with a function"""
        self.tree.bind('<<TreeviewSelect>>', func)

class EntryTextView(Visualize):
    """A textview that can only display texts"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.entry = ScrolledText(self)
    
    def display(self, text: list, color: str = "black"):
        '''
        Display the text on to the entry.
        :param text: - list of lines of text
        :param color: - the color of the text
        '''
        self.entry.configure(fg=color)
        self.entry.configure(state="normal")
        self.entry.delete("1.0", tk.END)
        for i in range(len(text)):
            self.entry.insert(f"{i + 1}.0", text[i] + "\n")
        self.entry.configure(fg=color)
        self.entry.configure(state="disabled")
        self.entry.pack(fill="both", expand=True, side=tk.LEFT)
        
class PieChart(Visualize):
    def __init__(self, parent:tk.Tk|tk.Frame):
        super().__init__(parent)
    
    def display(self, keys:list, values:list) -> None:
        """
        Display the pie graph from the parameters.
        :param keys: - a list containing the keys of each values.
        :param values: - a list containing the numerical values.
        """
        fig = Figure()
        ax = fig.add_subplot()
        ax.pie(values, radius=1, labels=keys, autopct="%0.2f%%")
        self.pie = FigureCanvasTkAgg(fig, self)

    def start(self) -> None:
        """Make the pie chart appear on the frame."""
        self.pie.get_tk_widget().pack(expand=True, fill="both")


class ScatterChart(Visualize):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def create_scatter(self, x_data:list, y_data:list) -> tuple:
        """
        :param x_data:
        :param y_data:
        :return: Figure, ax, scatter plot
        """
        minmax_x_data = (min(x_data), max(x_data))
        minmax_y_data = (min(y_data), max(y_data))
        # fig_size = (int(self.winfo_width()),int(self.winfo_height()))
        figure = Figure(figsize=(4, 6))
        figure_canvas = FigureCanvasTkAgg(figure, master=self)
        __ax = figure.add_subplot()
        _step_x = round((minmax_x_data[1] - minmax_x_data[0]) / 10)
        _step_y = round((minmax_y_data[1] - minmax_y_data[0]) / 10)
        if _step_x <= 0:
            _step_x = 1
        __ax.set_xticks(range(int(minmax_x_data[0]), ceil(minmax_x_data[1]) + _step_x, _step_x))
        __ax.set_yticks(range(int(minmax_y_data[0]), ceil(minmax_y_data[1]) + _step_y, _step_y))
        s = [0.5 for i in range(len(x_data))]
        scatter = __ax.scatter(x_data, y_data, s=s)
        return figure, figure_canvas, __ax, scatter
        
    def display(self, x_data:list, y_data:list) -> None:
        """
        Display the heatmap from the spicified array.
        :param x: - a list of data in the x axis.
        :param y: - a list of data in the y axis.
        """
        self.figure, self.figure_canvas, self.__ax, self.scatter = self.create_scatter(x_data, y_data)
        self.start()

    def update(self, x_data:list, y_data:list):
        """
        Update the heatmap from the spicified array.
        :param x: - a list of data in the x axis.
        :param y: - a list of data in the y axis.
        """
        # Delete all items in the frame
        for i in self.winfo_children():
            i.destroy()
        # Create new scatter plot
        self.figure, self.figure_canvas, self.__ax, self.scatter = self.create_scatter(x_data, y_data)
        self.start()

    def start(self):
        self.figure_canvas.get_tk_widget().pack()

    
