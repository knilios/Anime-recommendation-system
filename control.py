from csv_reader import Reader
import pandas as pd


class Control:
    def __init__(self) -> None:
        self.__file = Reader("newer_anime.csv")

    @property
    def data(self):
        return self.__file.data

    def unique(self, attr: str):
        return list(self.__file.data[attr].unique())

    def get_show_by_name(show_name):
        pass  # TODO

    def get_show_by_id(show_id):
        pass  # TODO

    def get_scatter_plot(self, genre: str | None = None):
        if genre == None:
            return self.__file.data["Score"], self.__file.data['drop_percent']
        only_genre = self.get_show_with_genre(genre)
        return only_genre["Score"], only_genre['drop_percent']

    def get_unique_genre(self):
        return ['Action',     'Adventure',        'Comedy',         'Drama',
                'Sci-Fi',         'Space',       'Mystery',       'Shounen',
                'Police',  'Supernatural',         'Magic',       'Fantasy',
                'Sports',         'Josei',       'Romance', 'Slice of Life',
                'Cars',        'Seinen',        'Horror', 'Psychological',
                'Thriller',   'Super Power',  'Martial Arts',        'School',
                'Ecchi',       'Vampire',      'Military',    'Historical',
                'Dementia',         'Mecha',        'Demons',       'Samurai',
                'Game',        'Shoujo',         'Harem',         'Music',
                'Shoujo Ai',    'Shounen Ai',          'Kids',        'Hentai',
                'Parody',          'Yaoi',          'Yuri']

    def get_show_with_genre(self, genre: str):
        return self.__file.data[self.__file.data['Genres'].str.contains(genre)]
    
    def get_data_for_histogram_page(self, filters:list):
        """
        Get the data for the histogram
        """
        #TODO
        pass

    def get_the_show_for_each_histogram(self, bar_index:int, data:list, bins_num:int):
        #TODO get the shows by sort(data)[num(data)*bar_index/bins_num: num(data)*bar_index+1/bins_num]
        pass


if __name__ == "__main__":
    co = Control()
    print(co.get_show_with_genre('Mecha')['Genres'])
