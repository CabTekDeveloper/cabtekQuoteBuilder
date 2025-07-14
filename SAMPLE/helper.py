# Wangchuk, 20-03-2025
import os
import shutil
from datetime import datetime

import file_folder_paths

#---------------------------------------------------------------------------------------------------------------------------#
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

# Backup database-------------------------------------------------------------------------------###
def backup_db():
    try: 
        # Delete old backups
        delete_files_older_than_x_days(file_folder_paths.FOLDER_PATH_DB_BACKUP,30)
        
        db_name = file_folder_paths.DB_NAME
        db_to_copy = file_folder_paths.DB_PATH
        backup_folder_path = file_folder_paths.FOLDER_PATH_DB_BACKUP
        
        # Copy db into backup folder
        shutil.copy(db_to_copy, backup_folder_path)
  
        # Build backup db name
        dt = datetime.now().strftime("%Y%m%d%H%M")
        backup_db_name = f"{dt}_{db_name}"

        # Rename the backup db
        backup_db_path = f"{backup_folder_path}//{db_name}"
        new_path = f"{backup_folder_path}//{backup_db_name}"
        shutil.move(backup_db_path, new_path)
        
    except Exception as ex:
        print(f'{ex} - backup_db')
        
# Split string into a List -------------------------------------------------------------------------------###

def split_string_into_list(string, slit_char="|"):
    list = string.split(slit_char)
    list =[int(x.strip()) for x in list if x.strip()] 
    return list

# Join list into a string -------------------------------------------------------------------------------###
def join_list(lst, join_by="|"):
    return "|".join( f"{x}" for x in  lst).replace(" ","")




