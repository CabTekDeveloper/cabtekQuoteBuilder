import inspect
import os
import helper
from .core import create_db_connection
from .eo_excel_text import delete_eo_excel_text_by_id

### -------------------------- EO Excel db manager-----------------------------------------###

def create_eo_excel_table():
    sql = ''' CREATE TABLE IF NOT EXISTS eo_excel_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eo_excel_name TEXT NOT NULL,
            eo_excel_path TEXT NOT NULL,
            user_id INTEGER,
            eo_excel_name_lower_no_ext TEXT,
            timestamp INTEGER
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()



def insert_into_eo_excel_table(eo_excel_name, eo_excel_path, user_id):
    try:
        eo_excel_name = eo_excel_name.strip()
        user_id = int(user_id)
        eo_excel_name_lower_no_ext = eo_excel_name.strip().split('.')[0].lower()
        timestamp = helper.get_cur_datetime()['timestamp']

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO eo_excel_table (eo_excel_name, eo_excel_path, user_id, eo_excel_name_lower_no_ext, timestamp)
                VALUES (?,?,?,?,?) '''
        cursor.execute(sql, [eo_excel_name, eo_excel_path, user_id, eo_excel_name_lower_no_ext, timestamp])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def check_eo_excel_name_exists_by_user_id(eo_excel_name, user_id):
    try:
        eo_excel_name_lower_no_ext = eo_excel_name.strip().split('.')[0].lower()
        user_id = int(user_id)
        sql = f' SELECT * FROM eo_excel_table WHERE eo_excel_name_lower_no_ext = ? AND user_id = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [eo_excel_name_lower_no_ext,user_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def get_eo_excel_by_user_id(user_id):
    eo_excel_by_user_id = []
    try:
        user_id = int(user_id)

        sql = ''' SELECT * FROM eo_excel_table WHERE  user_id =? ORDER BY timestamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[user_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            eo_excel_by_user_id.append({key: row[key] for key in row.keys()})

        return eo_excel_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return eo_excel_by_user_id


def get_eo_excel_by_eo_excel_name_and_user_id(eo_excel_name, user_id):
    eo_excel = {}
    try:
        eo_excel_name_lower_no_ext = eo_excel_name.strip().split('.')[0].lower()
        user_id = int(user_id)

        sql = f' SELECT * FROM eo_excel_table WHERE eo_excel_name_lower_no_ext = ? AND user_id = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [eo_excel_name_lower_no_ext,user_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            eo_excel = {key: row[key] for key in row.keys()}

        return eo_excel
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return eo_excel


def delete_eo_excel_by_id(eo_excel_id):
    id = int(eo_excel_id)
    sql = ''' DELETE FROM eo_excel_table WHERE id = ? '''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [id])
    connection.commit()
    cursor.close()
    connection.close()


def delete_eo_excel_by_name_and_user_id(eo_excel_name, user_id):
    try:
        eo_excel_name_lower_no_ext = eo_excel_name.strip().split('.')[0].lower()
        user_id = int(user_id)

        sql = ''' DELETE FROM eo_excel_table WHERE eo_excel_name_lower_no_ext = ? and user_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [eo_excel_name_lower_no_ext, user_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')



#--------------------------------------------------------------------------------------------#
# This function will delete excel file from eo_excel_table, texts saved in eo_excel_text_table for the excel file being deleted, and finally remove the file itself from the folder
def delete_old_eo_excel(user_id):
    try:
        eo_excels = get_eo_excel_by_user_id(user_id)
        # keep only 3 files at indices 0,1,2
        files_to_delete = eo_excels[1:]

        for eo_excel in files_to_delete:
            delete_eo_excel_by_id(eo_excel['id'])
            delete_eo_excel_text_by_id(eo_excel['id'])
            if os.path.exists(eo_excel['eo_excel_path']):
                os.remove(eo_excel['eo_excel_path'])

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
