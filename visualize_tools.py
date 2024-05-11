from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import ceil
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')


class Visualize(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


class Histogram(Visualize):
    """Create a histogram"""

    def __init__(self, parent) -> None:
        """
        Initiate a histogram.
        :param parent: A parent that will hold this histogram frame.
        """
        super().__init__(parent)
        self.parent = parent

    def show(self, data: list, bin_num: int, title: str, bar_clicked, ylabel: str = None) -> None:
        """
        Create a histogram for the first time.
        :param data: A list of data to put in the histogram.
        :param bin_num: Number of bins in the histogram.
        :param title: Title of the histogram.
        :param bar_clicked: A function that it will called after the bar is clicked.
        :param ylabel: A lebel in the y axis's label.
        """
        self.bar_clicked = bar_clicked
        self.title = title
        self.ylabel = ylabel
        self.bin_num = bin_num

        # create a histogram
        self.__create_hist(data, bin_num)

    def update(self, bin_num: int, data: list = None):
        """
        Update the already existed histogram.
        :param bin_num: The number of the bins in the histogram.
        :param data: A list of data that will be shown in the histogram. Left it blank 
        to use the old one.
        """
        data_in_use = data
        if data_in_use == None:
            data_in_use = self.data

        # delete everything in the frame
        for i in self.winfo_children():
            i.destroy()

        # create a new histogram
        self.__create_hist(data_in_use, bin_num)

    def __create_hist(self, data: list, bin_num: int):
        """
        Create a histogram.
        :param data: A list containing all data to be displayed in the histogram.
        :param bin_num: The number of bins in the histogram.
        """
        self.bin_num = bin_num
        self.data = data

        # create a figure
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)

        # NavigationToolbar2Tk(self.figure_canvas, self)
        axes = self.figure.add_subplot()

        # create the barchart
        axes.hist(data, bins=bin_num)
        axes.set_title(self.title)
        if self.ylabel != None:
            axes.set_ylabel(self.ylabel)

        # show the histogram
        self.figure_canvas.mpl_connect('button_press_event', self.bar_clicked)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def onClick(self, callback_function):
        """
        This function returns another function which you can use it as a binding function
        of the histogram on-click.
        :param callback_function: a function that the binding function will call. It
        will call something like this:
        ```py
        callback_function(bar_index, self:tk.Tk)
        ```
        bar_index is the integer of the histogram clicked.

        :return: a callback function
        """
        def realOnclick(event, *args):
            # Get the index of the clicked bar
            if not isinstance(event.xdata, (int, float)):
                return
            bar_index = (event.xdata - min(self.data)
                         ) // ((max(self.data)-min(self.data)) / self.bin_num)
            if (bar_index < 0) or (bar_index > (self.bin_num - 1)):
                return
            callback_function(bar_index, self)
        return realOnclick


class BarGraph(Visualize):
    """Generate a frame containing a BarGraph"""

    def __init__(self, parent, data_x: list, data_y: list, title: str, bar_clicked, ylabel: str = None) -> None:
        """
        Intiate the box plot and the frame.
        :param parent: The parent of this box plot frame.
        :param data_x: The data in the x-axis.
        :param data_y: The data in the y-axis.
        :param title: The title of the box plot.
        :param bar_clicked: The function that will be calling when a bar is clicked.
        :param ylabel: The name of the y-axis/
        """
        super().__init__(parent)
        self.bar_clicked = bar_clicked
        self.parent = parent

        # create a figure
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

    def update(self, data_x: list, data_y: list) -> None:
        """
        Update the data in the box plot.
        :param data_x:  a list of data in the x-axis.
        :param data_y: A list of data in the y-axis.
        """
        self.axes.bar(data_x, data_y)
        for i in self.winfo_children():
            i.destroy()


class TreeView(Visualize):
    """
    Create a clickable and scrollable treeview.
    """

    def __init__(self, parent: tk.Tk | tk.Frame, columns: tuple):
        """
        :param parent: The parent of this element.
        :param columns: The tuple of each column name.
        """
        super().__init__(parent)
        self.parent = parent
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for i in columns:
            self.tree.heading(i, text=str(i))
        # Create a scrollbar for the tree
        self.scrollbar = tk.Scrollbar(
            self.tree, orient="vertical", command=self.tree.yview)

    def start(self) -> None:
        """Make the tree visible (but not the frame that's containing it)"""
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def display(self, content: list) -> None:
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
        """
        Bind each lines of the tree with a function
        :param func: The function that will be called after a row is clicked.
        """
        self.tree.bind('<<TreeviewSelect>>', func)


class EntryTextView(Visualize):
    """A textview that can only display texts"""

    def __init__(self, parent: tk.Tk | tk.Frame):
        """
        :param parent: The parent of this element.
        """
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
    def __init__(self, parent: tk.Tk | tk.Frame):
        """
        :param parent: The parent of this element.
        """
        super().__init__(parent)

    def display(self, keys: list, values: list) -> None:
        """
        Display the pie graph from the parameters.
        :param keys: - a list containing the keys of each values.
        :param values: - a list containing the numerical values.
        """
        fig = Figure()
        ax = fig.add_subplot()
        ax.pie(values, radius=1, labels=keys, autopct="%0.2f%%")
        self.pie = FigureCanvasTkAgg(fig, self)

    def update(self, keys: list, values: list) -> None:

        # Delete everything in the frame
        for i in self.winfo_children():
            i.destroy()

        self.display(keys, values)
        self.start()

    def start(self) -> None:
        """Make the pie chart appear on the frame."""
        self.pie.get_tk_widget().pack(expand=True, fill="both")


class ScatterChart(Visualize):
    """Create a frame containing a scatter plot"""

    def __init__(self, parent: tk.Tk | tk.Frame) -> None:
        """
        :param parent: The parent of this element.
        """
        super().__init__(parent)

    def __create_scatter(self, x_data: list, y_data: list) -> tuple:
        """
        Create a scatter plot.
        :param x_data:
        :param y_data:
        :return: Figure, ax, scatter plot
        """
        minmax_x_data = (min(x_data), max(x_data))
        minmax_y_data = (min(y_data), max(y_data))
        figure = Figure(figsize=(4, 6))
        figure_canvas = FigureCanvasTkAgg(figure, master=self)
        __ax = figure.add_subplot()
        _step_x = round((minmax_x_data[1] - minmax_x_data[0]) / 10)
        _step_y = round((minmax_y_data[1] - minmax_y_data[0]) / 10)
        if _step_x <= 0:
            _step_x = 1
        __ax.set_xticks(range(int(minmax_x_data[0]), ceil(
            minmax_x_data[1]) + _step_x, _step_x))
        __ax.set_yticks(range(int(minmax_y_data[0]), ceil(
            minmax_y_data[1]) + _step_y, _step_y))
        s = [0.5 for i in range(len(x_data))]
        scatter = __ax.scatter(x_data, y_data, s=s)
        return figure, figure_canvas, __ax, scatter

    def display(self, x_data: list, y_data: list) -> None:
        """
        Display the heatmap from the spicified array.
        :param x: - a list of data in the x axis.
        :param y: - a list of data in the y axis.
        """
        self.figure, self.figure_canvas, self.__ax, self.scatter = self.__create_scatter(
            x_data, y_data)
        self.start()

    def update(self, x_data: list, y_data: list):
        """
        Update the heatmap from the spicified array.
        :param x: - a list of data in the x axis.
        :param y: - a list of data in the y axis.
        """
        # Delete all items in the frame
        for i in self.winfo_children():
            i.destroy()
        # Create new scatter plot
        self.figure, self.figure_canvas, self.__ax, self.scatter = self.__create_scatter(
            x_data, y_data)
        self.start()

    def start(self):
        self.figure_canvas.get_tk_widget().pack()
