import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import os


class Reader:
    def __init__(self, filename: str) -> None:
        self.__data = pd.read_csv(filename)

    @property
    def data(self):
        return self.__data


class ListDatabase:
    def __init__(self, database_name: str) -> None:
        """Initialize

        Args:
            database_name (str): The name of the database
        """
        self.database_name = database_name
        try:
            self.__reload()
        except FileNotFoundError:
            file = open(self.database_name + ".txt", "x")
            file.write("")
            self.__data = []
            file.close()

    def __reload(self) -> None:
        """(private) reload the database
        """
        file = open(self.database_name + ".txt", "r")
        self.__data = [i.replace("\n", "") for i in file.readlines()]
        file.close()

    @property
    def data(self):
        return self.__data

    def save_data(self) -> None:
        """Make the database actually save the database on to the file.
        """
        file = open(self.database_name + ".txt", "w")
        for i in self.__data:
            file.write(i + "\n")
        file.close()
        self.__reload()

    def delete_database(self) -> None:
        """Delete the database
        """
        os.remove(self.database_name + ".txt")

    def delete(self, data: any) -> None:
        """Delete on of the data in the database

        Args:
            data (any): The data that is intended to be delete.
        """
        self.data.remove(str(data))
        self.save_data()


if __name__ == "__main__":
    db = ListDatabase("TEST")
    db.data.append("Hello world")
    db.data.append("Bonjour Sekai")
    db.save_data()
    print(db.data)
    db.delete_database()
