import pandas as pd


class DataHandler:
    def __init__(self):
        pass
        
    
    def load_file(self, filePath):
        '''
        Parameters
        ----------
        filePath : file path of selected file.

        Returns
        -------
        None.

        '''
        self.__df = pd.read_csv(filePath)
        self.__df = self.__df.dropna()
        
        
    def list_cities(self):
        '''
        function for list for gCombo_city combobox  
        Returns
        -------
        vals : get community area names.

        '''
        vals = list(self.__df['COMMUNITY AREA NAME'].unique())
        vals.sort()
        return vals
    
    #displays data for chosen city
    def data_city(self, selected_city):
        '''
        function for data for selected city
        Parameters
        ----------
        selected_city : selected city.

        Returns
        -------
        returns data for selected city.

        '''
              
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME']== selected_city]
        return self.__subdf
    
    
    #display kwh data for selected city
    def kwh(self,from_month, to_month, selected_city):
        '''
        function for kwh data
        Parameters
        ----------
        from_month : start month of data visualisation.
        to_month : end month of data visualisation.
        selected_city : get data for specific city.

        Returns
        -------
        returns data  for selected city in specified month range

        '''
        __dc = self.data_city(selected_city)
        #GET INDEX OF JANUARY COLUMN
        janind = __dc.columns.get_loc("KWH JANUARY 2010")    
        #GET INDEX OF NTH-MONTH COLUMN
        start = janind+from_month-1
        end = janind+to_month
        #RETURN 
        return __dc.iloc[:,  range(start,end)]
    
    #display therm data for selected city
    def therm(self, from_month, to_month, selected_city):
        '''
        function for therms data
        Parameters
        ----------
        from_month : start month of data visualisation.
        to_month : end month of data visualisation.
        selected_city : get data for specific city.

        Returns
        -------
        returns data  for selected city in specified month range.

        '''
        __dc = self.data_city(selected_city)      
        janind = __dc.columns.get_loc("THERM JANUARY 2010")
        start = janind+from_month-1
        end = janind+to_month
        return __dc.iloc[:,  range(start,end)]
    
   