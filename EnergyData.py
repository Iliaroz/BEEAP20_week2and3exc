# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 11:30:05 2021

EnergyData class

@author: ilia
"""

import pandas as pd


class EnergyData:
    """
        Some description of class here
    """    
    
    def __init__(self):
        self.__df = pd.DataFrame()
        self.__subdf = pd.DataFrame()
        self.__values = ("KWH", "THERM")
        self.__months = range(1, 13)
    
    
    def loadData(self, data):
        """
        Improt data from file (or some acceptable data source) 
        to DataFrame
        
        Parameters
        ----------
        data : string
            path to file to load data from.

        Returns
        -------
        None.

        """
        try:
            self.__df = pd.read_csv(data)
        except TypeError :
            self.__df = pd.DataFrame(data)
            
        self.__df = self.__df.dropna()
            
    
    def getValuesList(self):
        return list(self.__values)

    
    def getMonthsRange(self):
        return range(1, 13)
        
    
    def __getData(self, aggregator, value, startmonth , endmonth):
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME'] == aggregator]
        janind = self.__subdf.columns.get_loc(value + " JANUARY 2010")
        if startmonth in self.__months and endmonth in self.__months:
            return self.__subdf.iloc[:, janind + startmonth - 1 : janind + endmonth  ]
    
    
    def getData_mean(self, aggregator, value, startmonth , endmonth):
        """
        

        Parameters
        ----------
        aggregator : string
            The value of field for data aggregation.
            (The name of city district)
        value : string
            Group of data to collect. One of element in list given by getValuesList().
        startmonth : int
            number of starting month (1..12).
        endmonth : int
            number of ending month (1..12).

        Returns
        -------
        # TODO: numpy or whatever else to return ???
        DataFrame
            DataFrame contains mean values.

        """
        if startmonth in self.__months and endmonth in self.__months:
            return self.__getData(aggregator, value, startmonth , endmonth).mean()

    

    def getData_max(self, aggregator, value, startmonth , endmonth):
        if startmonth in self.__months and endmonth in self.__months:
            return self.__getData(aggregator, value, startmonth , endmonth).max()
    

    def getData_min(self, aggregator, value, startmonth , endmonth):
        if startmonth in self.__months and endmonth in self.__months:
            return self.__getData(aggregator, value, startmonth , endmonth).min()
    

    def getAreasList (self):   ## ugly name
        return list(self.__df['COMMUNITY AREA NAME'].unique())

