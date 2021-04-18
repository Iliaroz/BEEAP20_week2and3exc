import pandas as pd


class DataHandler:
    def __init__(self):
        pass
        
    
    def load_file(self, filePath):
        self.__df = pd.read_csv(filePath)
        self.__df = self.__df.dropna()
        
        
    def list_cities(self):
        vals = list(self.__df['COMMUNITY AREA NAME'].unique())
        vals.sort()
        return vals
    
    
    def data_city(self, selected_city):#displays data for chosen city
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME']== selected_city].rename(columns={"TERM APRIL 2010":"THERM APRIL 2010"})
        return self.__subdf
    
    
    def kwh(self, from_month, to_month, selected_city):#display kwh data for selected city
        start = self.data_city(selected_city).columns.get_loc("KWH " + from_month + " 2010")
        end = self.data_city(selected_city).columns.get_loc("KWH " + to_month + " 2010")+1
        return self.data_city(selected_city).iloc[:,  range(start, end)]
    
    
    def therm(self, from_month, to_month, selected_city):#display therm data for selected city
        start = self.data_city(selected_city).columns.get_loc("THERM " + from_month + " 2010")
        end = self.data_city(selected_city).columns.get_loc("THERM " + to_month + " 2010")+1
        return self.data_city(selected_city).iloc[:,  range(start, end)]
    
   