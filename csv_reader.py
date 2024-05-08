import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import os

class Reader:
    def __init__(self, filename:str) -> None:
        self.__data = pd.read_csv(filename)

    @property
    def data(self):
        return self.__data
    

class ListDatabase:
    def __init__(self, database_name:str) -> None:
        self.database_name = database_name
        try:
            self.__reload()
        except FileNotFoundError:
            file = open(self.database_name + ".txt", "x")
            file.write("")
            self.__data = []
            file.close()

    def __reload(self):
        file = open(self.database_name + ".txt", "r")
        self.__data = [i.replace("\n", "") for i in file.readlines()]
        file.close()

    @property
    def data(self):
        return self.__data

    def save_data(self):
        file = open(self.database_name + ".txt", "w")
        for i in self.__data:
            file.write(i + "\n")
        file.close()
        self.__reload()

    def delete_database(self):
        os.remove(self.database_name + ".txt")

if __name__ == "__main__":
    db = ListDatabase("TEST")
    db.data.append("Hello world")
    db.data.append("Bonjour Sekai")
    db.save_data()
    print(db.data)
    db.delete_database()

