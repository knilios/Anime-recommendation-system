from visualize_tools import *
import numpy as np 
import random


if __name__ == "__main__":
    _input = input("Enter : ")
    test_window = tk.Tk()
    if _input == "1":
        test_window.title("Testing")
        data = {
                'Python': 11.27,
                'C': 11.16,
                'Java': 10.46,
                'C++': 7.5,
                'C#': 5.26
            }
        languages = data.keys()
        popularity = data.values()
        def bar_clicked(event):
            # Get the index of the clicked bar
            if not isinstance(event.xdata, (int, float)):
                return
            bar_index = round(event.xdata)
            print(f"Bar {bar_index} clicked!")

        histogram = Histogram(test_window, languages, popularity, "Test", bar_clicked)
        histogram.start()
        histogram.pack()
    elif _input == "2":
        test_window.title("Testing 2")
        def handler(*args):
            pie_test.update(['a', 'b', 'c'], [10, 10, 80])
        pie_test = PieChart(test_window)
        pie_test.display(['a', 'b', 'c'], [40, 30, 30])
        pie_test.start()
        pie_test.pack()
        tk.Button(test_window, text="click me", command=handler).pack()
    elif _input == "3":
        # Test treeview
        test_window.title("Testing 3")
        test_window.geometry("300x300")
        test_treeview = TreeView(test_window, ("ID", "Name"))
        test_treeview.start()
        test_treeview.pack(fill="both",side="left", expand=True)
        test_treeview.display([['123', 'JOJO'], ['124', "ドラえもん"]])
        def click_event(event, **args):
            print(event.widget.selection()[0])
            item = test_treeview.tree.item(event.widget.selection()[0])
            print("item: ", item["values"][0])
        test_treeview.bind(click_event)
    elif _input == "4":
        # test scatter plot
        def onClick(*args):
            test_scatter.update(list(np.random.randint(200,size=10)), list(np.random.randint(200,size=10)))
        test_window.title("Test Scatter plot")
        test_scatter = ScatterChart(test_window)
        test_button = tk.Button(test_window, text="click me", command=onClick)
        test_scatter.pack(fill="both",side="top", expand=True)
        test_scatter.display([0,1,2,3,4,5,6], [6,5,4,3,2,1,0])
        test_button.pack(side="top")

    elif _input == "5":
        #test histogram
        def bar_clicked(bar_index, *args):
            # Get the index of the clicked bar
            print(bar_index)
        def onClick(*args):
            # Stuffs
            test_histogram.update(random.randint(1,3))
        test_window.title("Test histogram")
        _data = [1,2,5,4,1,1,2,3,5,4,1,2,3,5,5,2,2,6,6,2,5,8,5,2,3,8]
        test_histogram = Histogram(test_window)
        test_histogram.show(_data, 3, "sample", test_histogram.onClick(bar_clicked), "stuffs")
        test_button = tk.Button(test_window, text="click me", command=onClick)
        test_button.pack(side="top")

        test_histogram.pack(fill="both",side="top", expand=True)


    test_window.mainloop()
