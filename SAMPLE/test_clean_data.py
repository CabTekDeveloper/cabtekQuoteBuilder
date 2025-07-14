
import db_manager_cabinet_parameters as cabinet_params_db

import pandas as pd



def clean_data():
    try:
        file = "parameters.csv"
        df = pd.read_csv(file, sep=",")
        
        # df["name"] = df["name"].apply(lambda x: str(x).split()[1])
        
        # df_sorted = df.sort_values(by=['name'])
        
        # df_sorted.to_csv("cleaned_parameter.csv" ,sep=",", index=False,header=True)
        # # df_dict = df_sorted.to_dict(orient='records')
        
        
        # # df_dict = df.to_dict(orient='records')
        
        # # print(df_dict)
        # # for row in df_dict:
        # #     print(row['name'])
        


        
        
        
    except Exception as ex:
        print(ex)

# clean_data()


def write_data_db():
    try:
        # file = "cleaned_parameter.csv"
        

        # df.to_csv(file ,sep=",", index=False,header=True)
        
        # df = pd.read_csv(file, sep=",")
        
        df_dict = df.to_dict(orient='records')
        
        for row in df_dict:
            cabinet_params_db.insert_into_tbl_parameter(row['name'],row['description'])
        
    except:
        pass

# write_data_db()