import datetime
import numpy as np
import pandas as pd

# http://jsideas.net/python/2015/08/30/daily_to_weekly.html
class Set_Date:
    #def __init__(self, parent=None):
        
    
    def df_to_day(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
       
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        
        for i in range(len(df.columns)):
            daily_df.append(df.resample('D', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_week(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
        
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('W', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_month(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
        
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
        
        df = df.drop(df.columns[0], 1)
        
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('M', how={df.columns[i]:np.sum}))
        
        return pd.concat(daily_df, axis=1)
    
    def df_to_min10(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('10T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min15(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('15T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min30(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('30T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)
     
    def df_to_min60(self):
        df = pd.read_csv('samples/Bldg90_load_6month.csv')
         
        df[df.columns[0]] = df[df.columns[0]].apply(lambda x: pd.to_datetime(str(x), format='%m/%d/%Y %H:%M'))   
        df.set_index(df[df.columns[0]], inplace=True)
         
        df = df.drop(df.columns[0], 1)
         
        daily_df = []
        for i in range(len(df.columns)):
            daily_df.append(df.resample('60T', how={df.columns[i]:np.sum}))
         
        return pd.concat(daily_df, axis=1)