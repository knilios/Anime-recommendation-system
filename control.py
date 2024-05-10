from csv_reader import *
import pandas as pd
import re


class Control:
    def __init__(self) -> None:
        self.__file = Reader("newer_anime.csv")
        self.preference_list = ListDatabase("prefered_list")

    @property
    def data(self):
        return self.__file.data

    def unique(self, attr: str) -> list:
        return list(self.__file.data[attr].unique())

    def get_show_by_name(self, show_name) -> pd.DataFrame:
        return self.data[self.data["Name"] == show_name]

    def get_show_by_id(self, show_id:float) -> pd.DataFrame:
        return self.data[self.data["MAL_ID"] == show_id]

    def get_scatter_plot(self, genre: str | None = None) -> tuple:
        if genre == None:
            return self.__file.data["Score"], self.__file.data['drop_percent']
        only_genre = self.get_show_with_genre(genre)
        return only_genre["Score"], only_genre['drop_percent']

    def get_unique_genre(self) -> list:
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

    def get_unique_type(self):
        return ["TV", "OVA", "Movie", "Special", "ONA"]
    
    def get_show_with_genre(self, genre: str) -> pd.DataFrame:
        return self.__file.data[self.__file.data['Genres'].str.contains(genre)]
    
    def get_data_for_histogram_page(self, filters:list=[]) -> pd.DataFrame:
        """
        Get the data for the histogram
        :param filters: The list of lists of filters that will be applied on the search
                    Example : [ ["attribute name", "filtered value"], ["attribute name 2", "filtered value 2"],]
        :return: A dataframe of result of the search
        """
        _list = self.__get_filters_from_prefered_list()
        if filters == []:
            return _list
        return self.get_show_with_filters(filters, _list)
        
    def __get_filters_from_prefered_list(self) -> pd.DataFrame:
        genre = []
        episodes = []
        _type = []

        data = self.data.copy()

        for i in self.preference_list.data:
            anime = self.get_show_by_id(float(i))
            episodes.append(int(anime["Episodes"].to_list()[0]))
            genre += [i.strip() for i in anime["Genres"].to_list()[0].split(",")]
            _type.append(anime["Type"].to_list()[0])

        genre = list(set(genre))
        _type = list(set(_type))
        
        _query_genre = "(" + genre[0] + ")"
        for i in genre[1::]:
            _query_genre += "|(" + i + ")"

        _query_type = "(" + _type[0] + ")"
        for i in _type[1::]:
            _query_genre += "|(" + i + ")"

        # Filter genre
        data = data[data["Genres"].str.match(_query_genre)]

        # Filter type
        data = data[data["Type"].str.match(_query_type)]

        # Filter number of episodes
        data = data[(data["Episodes"] >= min(episodes)) & (data["Episodes"] <= max(episodes))]

        return data

    
    def get_show_with_filters(self, filters:list=[], data:pd.DataFrame=None) -> pd.DataFrame:
        """
        Get the data for the search bar
        :param filters: The list of lists of filters that will be applied on the search
                    Example : [ ["Inclusive or Exclusive","attribute name", 
                                "filtered value", "filter value2 (for range)"], 
                                ["Inclusive or Exclusive","attribute name 2", "filtered value 2"],
                                ]
        :return: A dataframe of result of the search
        """
        if filters == []:
            return self.__file.data
        
        df = data
        if data is None:
            df = self.__file.data.copy()
        
        for i in filters:
            if i[0] == "Inclusive":
                if i[1] == "Episodes":
                    df = df[(df[i[1]] >= float(i[2])) & (df[i[1]] <= float(i[3]))]
                    continue
                df = df[df[i[1]].str.contains(i[2])]
            else:
                df = df[df[i[1]].str.contains(i[2]) == False]
        
        return df
        # extract id and name from the dataframe
        _id = df["MAL_ID"].to_list()
        _name = df["Name"].to_list()
        return _id, _name

    def get_the_show_from_each_histogram(self, bar_index:int, data:pd.DataFrame, bins_num:int) -> pd.DataFrame:
        """
        Get the shows from each histogram's index.
        :param bar_index: an index of a histogram clicked
        :param data: the data provided to the histogram
        :param bins_num: the number of histograms 
        :return: A dataframe of the shows in each histogram bar
        """
        score_list = data["Score"].to_list()
        lower_bound = (max(score_list) - min(score_list)) * (bar_index / bins_num) + min(score_list)
        upper_bound = (max(score_list) - min(score_list)) * ((bar_index+1) / bins_num) + min(score_list)
        return data[(data["Score"] >= lower_bound) & (data["Score"] <= upper_bound)]

    def get_show_from_part_of_name(self, text:str="") -> list:
        """
        Get show from the search bar's text.
        :param text: A string of the search bar's text.
        :return: A list of a lists, each containing the id and the name of each show.
        """
        _text = text.strip()
        df = self.data[self.data["Name"].str.contains(_text, flags=re.IGNORECASE)]
        _id = df["MAL_ID"].to_list()
        _name = df["Name"].to_list()
        return [[_id[i], _name[i]] for i in range(len(_id))]
    
    
    


if __name__ == "__main__":
    co = Control()
    print(co.get_show_with_genre('Mecha')['Genres'])
