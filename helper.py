
import os
from datetime import datetime

#---------------------------------------------------------------------------------------------------------------------------#

def get_cur_datetime():
    now = datetime.now()
    cur_date_time = {
        'date_today': now.strftime("%d/%m/%Y"),
        'time_now': now.strftime("%H:%M"),
        "timestamp": int(now.timestamp())
    }

    # cur_date_time = {
    #     'date_today': now.strftime("%d/%m/%Y"),
    #     'time_now': now.strftime("%H:%M:%S"),
    #     "timestamp": int(now.timestamp())
    # }
    return cur_date_time

# print(get_cur_datetime())

#----------------------------------------------------------------------------------------------------------------------------#

def delete_files_older_than_x_days(folder_path, days):
    try:
        files = os.listdir(folder_path) 
        
        for file in files:
            file_path = os.path.join(folder_path,file)
            file_modified_ts = round(os.path.getmtime(file_path))
            
            timestamp_now = int(datetime.now().timestamp())
            ts = timestamp_now - (days * 86400)
            
            if(file_modified_ts < ts):
                os.remove(file_path)
                
    except Exception as ex:
        print(f'{ex} - def delete_files_older_than_x_days')
        

