import pandas as pd

def readData(self, data_path):
    df=pd.read_csv('samples/Bldg90_load_6month.csv');
    
    #select datetime column by user
    
    #csv file preview 5lines with head(5)
    #and select column for plot
    
    data_df=df
    #data_df=df.column_name(A, B, C)
    #datetime_column.append(saved_column)
    
    return data_df 