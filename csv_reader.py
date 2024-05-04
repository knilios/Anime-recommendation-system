import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

class Reader:
    def __init__(self, filename:str) -> None:
        self.__data = pd.read_csv(filename)

    @property
    def data(self):
        return self.__data
    

class Database:
    def __init__(self, filename:str) -> None:
        self.__filename = filename
        self.data = pd.read_csv(filename)

    def savefile(self):
        self.data.to_csv(self.__filename, index=False)

