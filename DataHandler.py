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
    
    
    def data_city(self):#displays data for chosen city
        selected_city = self._gCombo_city.get()
        print(f"Selected city: {selected_city}")
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME']== selected_city].rename(columns={"TERM APRIL 2010":"THERM APRIL 2010"})
        return self.__subdf
    
    
    def kwh(self, from_month, to_month):#display kwh data for selected city
        start = self.__subdf.columns.get_loc("KWH " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("KWH " + to_month + " 2010")+1
        return self.__subdf.iloc[:,  range(start, end)]
    
    
    def therm(self, from_month, to_month):#display therm data for selected city
        start = self.__subdf.columns.get_loc("THERM " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("THERM " + to_month + " 2010")+1
        return self.__subdf.iloc[:,  range(start, end)]
    
    def range_plot(self, from_month, to_month):#arrange the range size for chosen months
        start = self.__subdf.columns.get_loc("THERM " + from_month + " 2010")
        end = self.__subdf.columns.get_loc("THERM " + to_month + " 2010")+2
        return range(1, end-start)