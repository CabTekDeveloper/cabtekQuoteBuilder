
import os
from datetime import datetime
import json
import time

# Constants ----------------------------------------------------------------------------------------------------------------#
DB_TABLE_METADATA_FILE = "db_table_meta_data.json"
KEY_CLIENTS_TABLE_INIT_TS = "clickup_clients_table_last_init_ts_seconds"

#---------------------------------------------------------------------------------------------------------------------------#

def get_cur_datetime():
    now = datetime.now()
    cur_date_time = {
        'date_today': now.strftime("%d/%m/%Y"),
        'time_now': now.strftime("%H:%M"),
        "timestamp": int(now.timestamp())
    }
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
        
#----------------------------------------------------------------------------------------------------------------------------#

# If the last init was over 60 seconds, return True
def check_require_init_clickup_client_table():
    try:
        ts_now = int(time.time())

        with open(DB_TABLE_METADATA_FILE,"r") as file:
            metadata = json.load(file)

        # Fallback to 0 if the key doesn't exist yet
        last_init = metadata.get(KEY_CLIENTS_TABLE_INIT_TS,0)

        return (ts_now - last_init) > 600
    
    except Exception as ex:
        # If errors, return True, so we will initialize the clients table regardless
        print(ex)
        return True
    
#----------------------------------------------------------------------------------------------------------------------------#    
def update_clickup_client_table_last_init():
    metadata={}
    try:
        # Open file to get metadata
        if os.path.exists(DB_TABLE_METADATA_FILE):
            with open(DB_TABLE_METADATA_FILE,"r") as file:
                metadata = json.load(file)

        # update last init ts
        metadata[KEY_CLIENTS_TABLE_INIT_TS] = int(time.time())

        # Write the updated file back
        with open(DB_TABLE_METADATA_FILE, "w") as file:
            json.dump(metadata, file, indent=4)

        return True
    except Exception as ex:
        print(f"Warning: Failed to log timestamp to {DB_TABLE_METADATA_FILE} file ({ex})")
        return False



#----------------------------------------------------------------------------------------------------------------------------#