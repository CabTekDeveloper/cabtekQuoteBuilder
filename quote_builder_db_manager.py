from datetime import datetime
import shutil
import sqlite3
import os
import helper
import inspect
import file_folder_paths
import company_info_manager

###-------------------------------------------------------------------------------###

def create_db_connection():
    QUOTING_DB_PATH = file_folder_paths.TEST_QUOTING_DB_PATH    # For Testing
    # QUOTING_DB_PATH = file_folder_paths.LIVE_QUOTING_DB_PATH    # For deployment
    connection = sqlite3.connect(QUOTING_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

# Backup database-------------------------------------------------------------------------------###
def backup_db(current_user):
    try: 
        # Delete old backups
        helper.delete_files_older_than_x_days(file_folder_paths.FOLDER_PATH_QUOTE_BUILDER_DB_BACKUP,30)
        
        db_name = file_folder_paths.QUOTING_DB_NAME
        db_to_copy = file_folder_paths.LIVE_QUOTING_DB_PATH
        backup_folder_path = file_folder_paths.FOLDER_PATH_QUOTE_BUILDER_DB_BACKUP
        
        # Copy db into backup folder
        shutil.copy(db_to_copy, backup_folder_path)
  
        # Build backup db name
        dt = datetime.now().strftime("%Y%m%d%H%M")
        backup_db_name = f"{dt}_{current_user}_{db_name}"

        # Rename the backup db
        backup_db_path = f"{backup_folder_path}//{db_name}"
        new_path = f"{backup_folder_path}//{backup_db_name}"
        shutil.move(backup_db_path, new_path)
        
    except Exception as ex:
        print(f'{ex} - backup_db')


# Alter table -------------------------------------------------------------------------------###

def drop_table(table_name):
    table_name = table_name.strip()
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"DROP TABLE {table_name} ;"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# drop_table("xx")

def alter_delete_column(table_name, column_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_delete_column("xx", "xxx")

def alter_add_column(table_name, new_column_name, dataType):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column_name} {dataType};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_add_column(table_name= "quotes_tableX", new_column_name= "company_id", dataType= "Integer")

def update_a_field(table_name, column_name, val):
    try:
        sql = f" UPDATE {table_name} SET {column_name} = ? "
        
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [val])
        connection.commit()
        cursor.close()
        connection.close()
    except:
        pass

def alter_rename_column(table_name, old_name, new_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} to {new_name};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_rename_column(table_name= "quotes_tableXX", old_name = "company_id", new_name= "company_id")

#---------------------------- Frequently used texts  db manager ------------------------------#

def create_frequently_used_text_table():
    sql = ''' CREATE TABLE IF NOT EXISTS frequently_used_text_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            count INTEGER,
            text_lower_case TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_frequently_used_text_table(user_id, text):
    try:
        user_id = int(user_id)
        text = text.strip()
        text_lower_case = text.lower().strip()
        count = 1

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO frequently_used_text_table (user_id, text, count, text_lower_case) 
                VALUES (?,?,?,?) '''
        cursor.execute(sql, [user_id, text, count, text_lower_case])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'{ex} - insert_into_frequently_used_text_table')
       

def get_frequently_used_text_count(user_id, text):
    count = 0
    try:
        user_id = int(user_id)
        text = text.strip()
        text_lower_case = text.lower().strip()

        sql = f' SELECT count FROM frequently_used_text_table WHERE user_id = ? AND text_lower_case = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_id, text_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            count = row['count']

        return count
    except:
        return count

def check_frequently_used_text_exists(user_id ,text):
    try:
        user_id = int(user_id)
        text = text.strip()
        text_lower_case = text.lower().strip()

        sql = f' SELECT * FROM frequently_used_text_table WHERE user_id = ? AND text_lower_case = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_id, text_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except:
        return False
    
    
def update_frequently_used_text_count(user_id, text):
    try:
        user_id = int(user_id)
        text = text.strip()
        text_lower_case = text.lower().strip()
        count = get_frequently_used_text_count(user_id, text) + 1

        sql = ''' UPDATE frequently_used_text_table 
                SET count = ?
                WHERE user_id = ? AND text_lower_case = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [count, user_id, text_lower_case ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def get_frequently_used_texts_by_user_id(user_id):
    frequently_used_texts = []
    try:
        user_id = int(user_id)
        
        sql = ''' SELECT * FROM frequently_used_text_table WHERE user_id = ? ORDER BY count DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[user_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            frequently_used_texts.append({key: row[key] for key in row.keys()})
            # return top 15 used texts
            frequently_used_texts = frequently_used_texts[:21]
        return frequently_used_texts

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return frequently_used_texts

def delete_frequently_used_text(text_id):
    try:
        id = int(text_id)
        sql = ''' DELETE FROM frequently_used_text_table WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [ id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
###--------------------------- section image size db manager -----------------------------------###
def create_section_image_size_table():
    sql = ''' CREATE TABLE IF NOT EXISTS section_image_size_table (
            section_image_size_id Integer PRIMARY KEY AUTOINCREMENT,
            section_image_size_name TEXT NOT NULL UNIQUE,
            section_image_width TEXT,
            section_image_height TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_section_image_size_table(section_image_size_name, section_image_width, section_image_height):
    try:
        section_image_size_name = section_image_size_name.strip().title()
        section_image_width = section_image_width.strip().lower()
        section_image_height = section_image_height.strip().lower()

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO section_image_size_table (section_image_size_name, section_image_width, section_image_height) 
                VALUES (?,?,?) '''
        cursor.execute(sql, [section_image_size_name, section_image_width, section_image_height])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def get_all_section_image_size():
    all_section_image_size = []
    try:
        sql = ''' SELECT * FROM section_image_size_table ORDER BY section_image_size_id ASC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_section_image_size.append({key: row[key] for key in row.keys()})

        return all_section_image_size
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_section_image_size

def get_section_image_size_info(section_image_size_id):
    section_image_size_info = {}
    try:
        section_image_size_id = int(section_image_size_id)

        sql = f' SELECT * FROM section_image_size_table WHERE section_image_size_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_image_size_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            section_image_size_info = {key: row[key] for key in row.keys()}

        return section_image_size_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return section_image_size_info
    



### --------------------------- User type db manager -----------------------------------###
def create_user_type_table():
    sql = ''' CREATE TABLE IF NOT EXISTS user_type_table (
            user_type_id Integer PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL UNIQUE,
            user_type_lowerCase TEXT     
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_user_type_table(user_type):
    try:
        user_type_lowerCase = user_type.strip().lower()

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO user_type_table (user_type, user_type_lowerCase) VALUES (?,?) '''
        cursor.execute(sql, [user_type, user_type_lowerCase])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass

def get_all_user_types():
    all_user_types = []
    try:
        sql = ''' SELECT * FROM user_type_table ORDER BY user_type DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_user_types.append({key: row[key] for key in row.keys()})

        return all_user_types
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_user_types

def get_user_type_id(user_type):
    user_type_id = None
    try:
        user_type_lowerCase = user_type.strip().lower()

        sql = f' SELECT user_type_id FROM user_type_table WHERE user_type_lowerCase = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_type_lowerCase])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            user_type_id = row['user_type_id']

        return user_type_id

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return user_type_id


### --------------------------- User db manager -----------------------------------###

def create_user_table():
    sql = ''' CREATE TABLE IF NOT EXISTS user_table (
            user_id Integer PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            email_id TEXT NOT NULL,
            user_password TEXT NOT NULL,
            mobile_no TEXT,
            phone_no TEXT,
            user_type_id Integer
        )'''
    # phone/mobile no are stored as TEXT to allow spacings in between , ex:- "02 6284 4583"
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()



def insert_into_user_table(user_name, full_name, email_id, user_password, mobile_no, phone_no, user_type_id):
    try:
        user_name = user_name.strip().lower()
        email_id = email_id.strip().lower()
        mobile_no = mobile_no.strip().lower()
        phone_no = phone_no.strip()
        
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO user_table (user_name, full_name,email_id, user_password, mobile_no, phone_no, user_type_id) 
                  VALUES (?,?,?,?,?,?,?) '''
        cursor.execute(sql, [user_name, full_name, email_id, user_password, mobile_no, phone_no, user_type_id])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_user_info_by_user_name(user_name):
    user_info = {}
    try:
        user_name = user_name.strip().lower()
        sql = f' SELECT * FROM user_table WHERE user_name = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_name])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            user_info = {key: row[key] for key in row.keys()}

        return user_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return user_info


def get_user_info_by_full_name(full_name):
    user_info = {}
    try:
        full_name = full_name.strip().title()
        sql = f' SELECT * FROM user_table WHERE full_name = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [full_name])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            user_info = {key: row[key] for key in row.keys()}

        return user_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return user_info


def get_user_info_by_id(user_id):
    user_info = {}
    try:
        user_id = int(user_id)

        sql = f' SELECT * FROM user_table WHERE user_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            user_info = {key: row[key] for key in row.keys()}

        return user_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return user_info
    


def get_all_users():
    all_quotes = []
    try:
        sql = ''' SELECT * FROM user_table ORDER BY user_name ASC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_quotes.append({key: row[key] for key in row.keys()})

        return all_quotes
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_quotes

def check_user_name_exists(user_name):
    try:
        user_name = user_name.strip().lower()

        sql = f' SELECT * FROM user_table WHERE user_name = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [user_name])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False



def update_user_info_by_user_id(new_user_info):
    try:
        user_id = int(new_user_info['user_id'])
        user_name = new_user_info['user_name'].strip().lower()
        full_name = new_user_info['full_name'].strip().title()
        email_id = new_user_info['email_id']
        user_password = new_user_info['user_password']
        mobile_no = new_user_info['mobile_no']
        phone_no = new_user_info['phone_no']
        user_type_id = int(new_user_info['user_type_id']) if new_user_info['user_type_id'] != None else new_user_info['user_type_id']

        connection = create_db_connection()
        cursor = connection.cursor()

        if (user_type_id == None) or (user_type_id == ''):
            sql = ''' UPDATE user_table 
                SET user_name = ?,
                full_name = ?,
                email_id = ?,
                user_password = ?,
                mobile_no = ?,
                phone_no = ?
                
                WHERE user_id = ? '''
            cursor.execute(sql, [user_name, full_name, email_id, user_password, mobile_no, phone_no , user_id])
        else:
            sql = ''' UPDATE user_table 
                SET user_name = ?,
                full_name = ?,
                email_id = ?,
                user_password = ?,
                mobile_no = ?,
                phone_no = ?,
                user_type_id = ?
                
                WHERE user_id = ? '''
            cursor.execute(sql, [user_name, full_name, email_id, user_password, mobile_no, phone_no , user_type_id, user_id])

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


### -------------------------- Quote status db manager-----------------------------------------###

def create_quote_status_table():
    # create quote_name_lower_case to store the lowered case quote_name. We can use it later to check if the quote name already exists in the database.
    sql = ''' CREATE TABLE IF NOT EXISTS quote_status_table (
            quote_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_status TEXT NOT NULL UNIQUE,
            quote_status_lower_case TEXT 
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_quote_status_table(quote_status):
    try:

        quote_status_lower_case = quote_status.strip().lower()

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quote_status_table (quote_status, quote_status_lower_case) 
                VALUES (?,?) '''
        cursor.execute(sql, [quote_status, quote_status_lower_case])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass

def get_all_quote_status():
    all_quote_status = []
    try:
        sql = ''' SELECT * FROM quote_status_table ORDER BY quote_status ASC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_quote_status.append({key: row[key] for key in row.keys()})

        return all_quote_status
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_quote_status



def get_quote_status_name(quote_status_id):
    quote_status_name = ""
    try:
        quote_status_id = int(quote_status_id)

        sql = f' SELECT * FROM quote_status_table WHERE quote_status_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_status_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return row['quote_status']  if row  else quote_status_name
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_status_name

def get_quote_status_id(quote_status):
    quote_status_id = None
    try:
        quote_status_lower_case = quote_status.strip().lower()

        sql = f' SELECT * FROM quote_status_table WHERE quote_status_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_status_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return row['quote_status_id']  if row  else quote_status_id
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_status_id




### -------------------------- Quotes db manager-----------------------------------------###

def create_quotes_table():
    # create quote_name_lower_case to store the lowered case quote_name. We can use it later to check if the quote name already exists in the database.
    sql = ''' CREATE TABLE IF NOT EXISTS quotes_table (
            quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_name TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            date_quote_created TEXT,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone_no TEXT,
            delivery_info TEXT,
            quote_name_lower_case TEXT,
            time_stamp INTEGER,
            rev_date TEXT,
            is_template TEXT,
            quote_status_id INTEGER,
            revision_dates TEXT,
            joinery_supply_type TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()



def update_quote_info_by_quote_id(new_quote_info):
    try:
        quote_id = int(new_quote_info['quote_id'])
        quote_name = new_quote_info['quote_name']
        customer_name = new_quote_info['customer_name'].strip().title()
        customer_email = new_quote_info['customer_email']
        customer_phone_no = new_quote_info['customer_phone_no']
        delivery_info = new_quote_info['delivery_info']
        is_template = new_quote_info['is_template']
        quote_name_lower_case = quote_name.strip().lower()
        time_stamp = helper.get_cur_datetime()['timestamp']
        rev_date = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        company_id = int(new_quote_info['company_id'])
        
        sql = ''' UPDATE quotes_table 
                SET quote_name = ?,
                customer_name = ?,
                customer_email = ?,
                customer_phone_no = ?,
                delivery_info = ?,
                quote_name_lower_case = ?,
                is_template = ?,
                time_stamp = ?,
                rev_date = ?,
                company_id = ?
                
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name, customer_name, customer_email, customer_phone_no, delivery_info, quote_name_lower_case , is_template, time_stamp, rev_date, company_id, quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
    

def insert_into_quotes_table(quote_name, user_id, date_quote_created, customer_name="", customer_email="", customer_phone_no="", delivery_info="", is_template = "no" , company_id=0):
    try:

        quote_name_lower_case = quote_name.strip().lower()
        customer_name=customer_name.strip().title()
        time_stamp = helper.get_cur_datetime()['timestamp']
        is_template = is_template.strip().lower()
        quote_status_id = 0
        rev_date = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        quote_status_id = 0
        joinery_supply_type = 'Supply of customised joinery'
        company_id= int(company_id)
        
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quotes_table (quote_name,user_id,date_quote_created,customer_name,customer_email,customer_phone_no,delivery_info,quote_name_lower_case,time_stamp, rev_date, is_template, quote_status_id, joinery_supply_type, company_id) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, [quote_name, user_id, date_quote_created, customer_name, customer_email, customer_phone_no, delivery_info, quote_name_lower_case, time_stamp,rev_date, is_template, quote_status_id, joinery_supply_type, company_id])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_quote_info_by_quote_name(quote_name):
    quote_info = {}
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT * FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_info = {key: row[key] for key in row.keys()}
        return quote_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_info
    
# print(get_quote_info_by_quote_name("Testquote2"))

def get_quote_info_by_quote_id(quote_id):
    quote_info = {}
    try:
        quote_id = int(quote_id)

        sql = f' SELECT * FROM quotes_table WHERE quote_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_info = {key: row[key] for key in row.keys()}
        return quote_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_info

def check_quote_name_exists(quote_name):
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT * FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def get_all_quotes():
    all_quotes = []
    try:
        sql = ''' SELECT * FROM quotes_table ORDER BY time_stamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_quotes.append({key: row[key] for key in row.keys()})

        return all_quotes
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_quotes


def get_quotes_by_user_id(user_id):
    quotes_by_user_id = []
    try:
        user_id = int(user_id)
        sql = ''' SELECT * FROM quotes_table WHERE user_id=? ORDER BY time_stamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[user_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quotes_by_user_id.append({key: row[key] for key in row.keys()})

        return quotes_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quotes_by_user_id

def get_quote_id_by_quote_name(quote_name):
    quote_id = None
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT quote_id FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_id = row['quote_id']
        return quote_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_id


def get_quote_name_by_quote_id(quote_id):
    quote_name = ''
    try:
        sql = f' SELECT quote_name FROM quotes_table WHERE quote_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_name = row['quote_name']
        return quote_name
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_name

# print(get_quote_name_by_quote_id(56))

def delete_quote_by_quote_id(quote_id):
    try:
        sql = ''' DELETE FROM quotes_table WHERE quote_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def update_quote_rev_date_and_time_stamp(quote_id):
    try:
        quote_id = int(quote_id)
        rev_date = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        time_stamp = helper.get_cur_datetime()['timestamp']

        sql = ''' UPDATE quotes_table 
                SET rev_date = ?,
                time_stamp = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [rev_date, time_stamp,  quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_quote_status_by_quote_id(quote_id, quote_status_id):
    try:
        quote_id = int(quote_id)
        quote_status_id = int(quote_status_id)
        sql = ''' UPDATE quotes_table 
                SET quote_status_id = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_status_id, quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_quote_revision_dates(quote_id, new_revision_dates):
    try:
        quote_id = int(quote_id)
        new_revision_dates = new_revision_dates.strip()

        sql = ''' UPDATE quotes_table 
                SET revision_dates = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [new_revision_dates, quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_joinery_supply_type(quote_id, joinery_supply_type):
    try:
        quote_id = int(quote_id)
        joinery_supply_type = joinery_supply_type.strip()

        sql = ''' UPDATE quotes_table 
                SET joinery_supply_type = ?
                WHERE quote_id = ? '''
        
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [joinery_supply_type, quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')




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


    
### -------------------------- EO Excel Text db manager-----------------------------------------###

def create_eo_excel_text_table():
    sql = ''' CREATE TABLE IF NOT EXISTS eo_excel_text_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eo_excel_id INTEGER NOT NULL,
            text TEXT,
            text_lower_case TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_eo_excel_text_table(eo_excel_id, text):
    try:
        eo_excel_id = int(eo_excel_id)
        text = text.strip()
        text_lower_case = text.lower()
        
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO eo_excel_text_table (eo_excel_id, text, text_lower_case) 
                VALUES (?,?,?) '''
        cursor.execute(sql, [eo_excel_id, text, text_lower_case])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass

def get_eo_excel_text_by_eo_excel_id(eo_excel_id):
    eo_excel_texts = []
    try:
        eo_excel_id = int(eo_excel_id)

        sql = ''' SELECT * FROM eo_excel_text_table WHERE  eo_excel_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[eo_excel_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            eo_excel_texts.append({key: row[key] for key in row.keys()})

        return eo_excel_texts
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return eo_excel_texts
    

def delete_eo_excel_text_by_id(eo_excel_id):
    eo_excel_id = int(eo_excel_id)
    sql = ''' DELETE FROM eo_excel_text_table WHERE eo_excel_id = ? '''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [eo_excel_id])
    connection.commit()
    cursor.close()
    connection.close()    


def get_searched_eo_excel_text_by_eo_excel_id(eo_excel_id, search_str):
    searched_texts = []
    try:
        eo_excel_id = int(eo_excel_id)
        search_str = '%' + search_str.strip().lower() + '%'
        
        sql = ''' SELECT * FROM eo_excel_text_table WHERE eo_excel_id = ? AND text_lower_case LIKE  ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [eo_excel_id, search_str])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            searched_texts.append({key:row[key] for key in row.keys()})

        return searched_texts
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return searched_texts


### -------------------------- Image_tag db manager-----------------------------------------###
def create_image_tag_table():
    sql = ''' CREATE TABLE IF NOT EXISTS image_tag_table (
            image_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_tag_name TEXT NOT NULL UNIQUE,
            image_tag_name_lower_case TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_image_tag_table(image_tag_name):
    try:
        image_tag_name_lower_case = image_tag_name.strip().lower()
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO image_tag_table (image_tag_name, image_tag_name_lower_case) 
                VALUES (?,?) '''
        cursor.execute(
            sql, [image_tag_name, image_tag_name_lower_case])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_all_image_tags():
    all_image_tags = []
    try:
        sql = ''' SELECT * FROM image_tag_table '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_image_tags.append({key: row[key] for key in row.keys()})

        return all_image_tags
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_image_tags


def get_image_tag_name_by_tag_id(image_tag_id):
    image_tag_name = None
    try:

        sql = f' SELECT image_tag_name FROM image_tag_table WHERE image_tag_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_tag_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return row['image_tag_name'] if row != None else image_tag_name
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return image_tag_name


def get_image_tag_id_by_tag_name(image_tag_name):
    image_tag_id = None
    try:
        image_tag_name_lower_case = image_tag_name.strip().lower()

        sql = f' SELECT image_tag_id FROM image_tag_table WHERE image_tag_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_tag_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return row['image_tag_id'] if row != None else image_tag_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return image_tag_name
    

### -------------------------- Images db manager-----------------------------------------###

def create_images_table():
    sql = ''' CREATE TABLE IF NOT EXISTS images_table (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_full_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            image_name_lower_no_ext TEXT,
            image_tag_id INTEGER
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_images_table(image_full_name, image_path, image_tag_id = 0 ):
    try:
        image_name_lower_no_ext = image_full_name.split('.')[0].strip().lower()
        image_tag_id = int(image_tag_id)

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO images_table (image_full_name, image_path, image_name_lower_no_ext, image_tag_id) 
                VALUES (?,?,?,?) '''
        cursor.execute(
            sql, [image_full_name, image_path, image_name_lower_no_ext, image_tag_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_image_info_by_image_id(image_id):
    image_info = {}
    try:
        image_id= int(image_id)

        sql = f' SELECT * FROM images_table WHERE image_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return {key: row[key] for key in row.keys()} if row != None else image_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return image_info
    


def get_all_images():
    all_images = []
    try:
        sql = ''' SELECT * FROM images_table '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_images.append({key: row[key] for key in row.keys()})

        return all_images
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_images

def get_all_images_by_tag_id(image_tag_id):
    all_images_by_tag_id = []
    try:
        image_tag_id= int(image_tag_id)
        sql = ''' SELECT * FROM images_table WHERE image_tag_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_tag_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_images_by_tag_id.append({key: row[key] for key in row.keys()})

        return all_images_by_tag_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_images_by_tag_id


def get_searched_images(search_str):
    searched_images = []
    try:
        search_str = '%' + search_str.strip().lower() + '%'
        sql = ''' SELECT * FROM images_table WHERE image_name_lower_no_ext LIKE  ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [search_str])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            searched_images.append({key: row[key] for key in row.keys()})

        return searched_images
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return searched_images


# Note that image_full_name includes extention too.
def check_image_name_exists(image_full_name, image_tag_id):
    try:
        image_name_lower_no_ext = image_full_name.split('.')[0].strip().lower()
        image_tag_id = int(image_tag_id)
        
        sql = f' SELECT * FROM images_table WHERE image_name_lower_no_ext = ? AND image_tag_id=?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_name_lower_no_ext, image_tag_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False
    
def delete_image_by_image_id(image_id):
    try:
        image_id = int(image_id)

        sql = ''' DELETE FROM images_table WHERE image_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_id])
        connection.commit()
        cursor.close()
        connection.close()

        return True
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False
    


### --------------------------- Texts db manager -----------------------------------###

def create_texts_table():
    sql = ''' CREATE TABLE IF NOT EXISTS texts_table (
            text_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT NOT NULL,
            text_lower_case TEXT,
            time_stamp INTEGER
        )'''

    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_texts_table(text, user_id):
    try:
        text = text.strip()
        text_lower_case = text.strip().lower()
        user_id = int(user_id)
        time_stamp = helper.get_cur_datetime()['timestamp']
        
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO texts_table (user_id, text,text_lower_case,time_stamp) 
                VALUES (?,?,?,?) '''
        cursor.execute(sql, [user_id, text, text_lower_case, time_stamp])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_texts_by_user_id(user_id):
    texts_by_user_id = []
    try:
        user_id = int(user_id)
        
        sql = ''' SELECT * FROM texts_table WHERE user_id = ? ORDER BY time_stamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[user_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            texts_by_user_id.append({key: row[key] for key in row.keys()})

        return texts_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return texts_by_user_id

def check_text_exists(text):
    try:
        text_lower_case = text.strip().lower()

        sql = f' SELECT * FROM texts_table WHERE text_lower_case = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [text_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def get_searched_texts(search_str):
    texts_by_user_id = []
    try:
        search_str = '%' + search_str.strip().lower() + '%'
  
        sql = ''' SELECT * FROM texts_table WHERE text_lower_case LIKE  ? ORDER BY time_stamp DESC '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [search_str])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            texts_by_user_id.append({key: row[key] for key in row.keys()})

        return texts_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return texts_by_user_id

def delete_text_by_text_id(text_id, user_id):
    user_id =  int(user_id)
    text_id = int(text_id)
    sql = ''' DELETE FROM texts_table WHERE text_id = ? AND  user_id = ?'''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [ text_id, user_id])
    connection.commit()
    cursor.close()
    connection.close()


### --------------------------- section name db manager -----------------------------------###

def create_section_names_table():
    sql = ''' CREATE TABLE IF NOT EXISTS section_names_table (
            section_name_id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_name TEXT NOT NULL UNIQUE,
            section_name_lower_case TEXT  
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_section_names_table(section_name):
    try:
        section_name = section_name.strip()
        section_name_lower_case = section_name.strip().lower()

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO section_names_table (section_name,section_name_lower_case) 
                VALUES (?,?) '''
        cursor.execute(sql, [section_name, section_name_lower_case])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def check_section_name_exists(section_name):
    try:
        section_name_lower_case = section_name.strip().lower()

        sql = f' SELECT * FROM section_names_table WHERE section_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def get_all_section_names():
    all_section_names = []
    try:
        sql = ''' SELECT * FROM section_names_table ORDER BY section_name COLLATE NOCASE  ASC '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_section_names.append({key: row[key] for key in row.keys()})

        return all_section_names
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_section_names



def get_section_id_by_section_name(section_name):
    section_name_id = None
    try:
        section_name_lower_case = section_name.strip().lower()

        sql = f' SELECT section_name_id FROM section_names_table WHERE section_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            section_name_id = row['section_name_id']

        return section_name_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return section_name_id
    
def get_section_name_by_section_name_id(section_name_id):
    section_name = ''
    try:
        
        sql = f' SELECT section_name FROM section_names_table WHERE section_name_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_name_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            section_name = row['section_name']

        return section_name
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return section_name





### --------------------------- Quote Details db manager -----------------------------------###


def create_quote_details_table():
    sql = ''' CREATE TABLE IF NOT EXISTS quote_details_table (
            quote_id INTEGER NOT NULL,
            section_name_id INTEGER NOT NULL,
            section_sub_heading TEXT,
            section_image_row TEXT,
            section_text TEXT,
            section_qty_row INTEGER,
            section_unit_cost_row REAL,
            section_total_cost_row REAL
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_quote_details_table(quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quote_details_table (quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row) VALUES (?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, [quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_quote_details_by_quote_id(quote_id):
    quote_details_by_quote_id = []
    try:
        sql = ''' SELECT * FROM quote_details_table WHERE quote_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quote_details_by_quote_id.append(
                {key: row[key] for key in row.keys()})

        return quote_details_by_quote_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_details_by_quote_id




def get_quote_details_by_quoteId_and_sectionId(quote_id,section_name_id):
    quote_details_by_quoteId_and_sectionId = []
    try:
        sql = ''' SELECT * FROM quote_details_table WHERE quote_id = ? AND  section_name_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id,section_name_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quote_details_by_quoteId_and_sectionId.append(
                {key: row[key] for key in row.keys()})

        return quote_details_by_quoteId_and_sectionId
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_details_by_quoteId_and_sectionId
    


def check_quote_detials_exists_by_quoteId_and_sectionId(quote_id, section_name_id):
    try:
        sql = f' SELECT * FROM quote_details_table WHERE quote_id = ? AND section_name_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id, section_name_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def delete_quote_detials_by_quoteId_and_sectionId(quote_id, section_name_id):
    sql = ''' DELETE FROM quote_details_table WHERE quote_id = ? AND section_name_id = ? '''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quote_id, section_name_id])
    connection.commit()
    cursor.close()
    connection.close()


def delete_quote_details_by_quote_id(quote_id):
    sql = ''' DELETE FROM quote_details_table WHERE quote_id = ?'''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quote_id])
    connection.commit()
    cursor.close()
    connection.close()


### --------------------------- Quote section info db manager -----------------------------------###


def create_quote_section_info_table():
    sql = ''' CREATE TABLE IF NOT EXISTS quote_section_info_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id INTEGER NOT NULL,
            section_name_id INTEGER NOT NULL,
            section_image_full_names TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_quote_section_info_table(quote_id, section_name_id, section_image_full_names):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quote_section_info_table (quote_id,section_name_id,section_image_full_names) 
                VALUES (?,?,?) '''
        cursor.execute(sql, [quote_id, section_name_id, section_image_full_names])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass

def get_quote_section_info_by_quote_id(quote_id):
    quote_section_info_by_quote_id = []
    try:
        sql = ''' SELECT * FROM quote_section_info_table WHERE quote_id = ?  ORDER BY section_order_no ASC '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            temp_row = {key: row[key] for key in row.keys()}
            temp_row['quote_name'] = get_quote_name_by_quote_id(quote_id)
            temp_row['section_name'] = get_section_name_by_section_name_id(row['section_name_id'])
            quote_section_info_by_quote_id.append(temp_row)

        for index,value in enumerate(quote_section_info_by_quote_id):
            if value['section_order_no'] is not None:
                break
            else:
                quote_section_info_by_quote_id[index]['section_order_no'] = index+1
        return quote_section_info_by_quote_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_section_info_by_quote_id
   
# print(get_quote_section_info_by_quote_id(286))

def get_quote_section_info_by_quoteId_and_sectionNameId(quote_id, section_name_id):
    quote_section_info = []
    try:
        sql = ''' SELECT * FROM quote_section_info_table WHERE quote_id = ? AND section_name_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id, section_name_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quote_section_info.append({key: row[key] for key in row.keys()})

        return quote_section_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_section_info


def check_quote_section_info_exists(quote_id, section_name_id):
    try:
        sql = f' SELECT * FROM quote_section_info_table WHERE quote_id = ? AND section_name_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id, section_name_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def update_quote_section_info(quote_id, section_name_id, section_image_full_names):
    try:
        sql = ''' UPDATE quote_section_info_table 
              SET section_image_full_names = ?
              WHERE quote_id = ? AND section_name_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_image_full_names, quote_id, section_name_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        

def update_quote_section_order_no(quote_id, section_name_id, section_order_no):
    try:
        sql = ''' UPDATE quote_section_info_table 
                SET section_order_no = ?
                WHERE quote_id = ? AND section_name_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [section_order_no, quote_id, section_name_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
def delete_quote_section_info(quote_id, section_name_id):
    try:
        sql = ''' DELETE FROM quote_section_info_table WHERE quote_id = ? AND section_name_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id, section_name_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def delete_quote_section_info_by_quote_id(quote_id):
    try:
        sql = ''' DELETE FROM quote_section_info_table WHERE quote_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

### --------------------------------- Other Functions -----------------------------------###


# save section data to quote_details_table and quote_section_info_table
# section_data_to_save will come from the website when users click on save while creating a quote
def save_section_data(section_data_to_save):
    try:
        # get data into different variables
        quote_id = get_quote_id_by_quote_name(section_data_to_save.pop('quote_name'))
        section_name_id = get_section_id_by_section_name(section_data_to_save.pop('section_name'))
        section_image_full_names = section_data_to_save.pop('section_image_full_names').strip()
        section_detail_rows = section_data_to_save.pop('section_detail_rows')
        
        # add new section or update  section in quote_section_info table
        if (check_quote_section_info_exists(quote_id,section_name_id)):
            update_quote_section_info(quote_id, section_name_id, section_image_full_names)
        else:
            insert_into_quote_section_info_table(quote_id, section_name_id, section_image_full_names)
            quote_total_sections = len(get_quote_section_info_by_quote_id(quote_id))
            update_quote_section_order_no(quote_id, section_name_id,quote_total_sections)
            
        # delete section detail rows before adding new rows
        delete_quote_detials_by_quoteId_and_sectionId(quote_id, section_name_id)

        for row in section_detail_rows:
            insert_into_quote_details_table(quote_id, section_name_id, row['section_sub_heading'], row['section_image_row'], row['section_text'], row['section_qty_row'], row['section_unit_cost_row'],row['section_total_cost_row'])

        return True

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False




def get_quote_data(quote_name):
    quote_data = {}
    
    try:
        quote_info = get_quote_info_by_quote_name(quote_name)
        quote_id = quote_info['quote_id']

        section_names =[]
        all_sections_data = {}
        
        GST = company_info_manager.get_company_info_by_id(quote_info['company_id'])['gst']
        total_cost_ex_gst= 0
        total_cost_inc_gst =0

        # Get section names
        quote_section_info_by_quote_id =get_quote_section_info_by_quote_id(quote_id)
        for row in quote_section_info_by_quote_id:
            section_name = get_section_name_by_section_name_id(row['section_name_id'])
            section_names.append(section_name)
            # if section_name not in section_names:
            #     section_names.append(section_name)

        # Get section_row_details of each section name
        for section_name in section_names:
            section_name_id = get_section_id_by_section_name(section_name)
            temp_data = {}
            temp_data['section_name'] = section_name
            temp_data['section_name_id'] = section_name_id
            quote_section_info_by_quoteId_and_sectionNameId = get_quote_section_info_by_quoteId_and_sectionNameId(quote_id,section_name_id)
            
            if quote_section_info_by_quoteId_and_sectionNameId :
                section_image_full_names = quote_section_info_by_quoteId_and_sectionNameId[0]['section_image_full_names'].strip()
                if len(section_image_full_names) > 0:
                    temp_data['section_image_full_names'] = [{ "image_full_name" : item.split(';')[0], "image_size_info": get_section_image_size_info(item.split(';')[1].split('_')[1]) } for item in  section_image_full_names.split("|")] 
                else:
                    temp_data['section_image_full_names']  = []
            else:
                temp_data['section_image_full_names']  = []

            quote_details_by_quoteId_and_sectionId = get_quote_details_by_quoteId_and_sectionId(quote_id,section_name_id)

            section_detail_rows = []
            for section_detial_row in quote_details_by_quoteId_and_sectionId:
                temp_row ={}
                temp_row['section_sub_heading'] = section_detial_row['section_sub_heading']
                temp_row['section_image_row'] = section_detial_row['section_image_row']
                temp_row['section_text'] = section_detial_row['section_text']
                temp_row['section_qty_row'] = section_detial_row['section_qty_row']
                temp_row['section_unit_cost_row'] = section_detial_row['section_unit_cost_row']
                temp_row['section_total_cost_row'] = section_detial_row['section_total_cost_row']
                section_detail_rows.append(temp_row)

                # add all the total_costs of each row
                total_cost_ex_gst += section_detial_row['section_total_cost_row']

            temp_data['section_detail_rows'] = section_detail_rows

            all_sections_data[section_name] = temp_data

        total_gst = round((GST/100)*total_cost_ex_gst ,2)
        total_cost_inc_gst = total_cost_ex_gst + total_gst


        # Append data
        quote_data['quote_id'] = quote_id
        quote_data['quote_name'] = quote_name
        quote_data['total_cost_ex_gst'] = round(total_cost_ex_gst,2)
        quote_data['total_gst'] = round(total_gst, 2)
        quote_data['total_cost_inc_gst'] = round(total_cost_inc_gst, 2)
        quote_data['section_names'] = section_names
        quote_data['total_sections'] = len(section_names)
        quote_data['all_sections_data'] = all_sections_data

        return quote_data

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_data
    


# print(get_quote_section_info_by_quote_id(56))

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


# this will delete quote and all its data from different tables
def delete_quote_and_its_data(quote_id):
    try:
        delete_quote_by_quote_id(quote_id)
        delete_quote_details_by_quote_id(quote_id)
        delete_quote_section_info_by_quote_id(quote_id)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

# To delete the selected saved section in quote_section_info_table and its details saved in quote_details_table
def delete_seleceted_section_data(quote_id, section_id):
    try:
        delete_quote_detials_by_quoteId_and_sectionId(quote_id,section_id)
        delete_quote_section_info(quote_id,section_id)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#--------------------------------------------------------------------------------------------#

def copy_quote_details_to_new_quote(original_quote_data, copied_quote_id):
    try:
        copied_quote_id = int(copied_quote_id)
        all_sections_data = original_quote_data['all_sections_data']
        for key, value in all_sections_data.items():
            section_name_id = value['section_name_id']
            # section_image_full_names = "|".join(value['section_image_full_names'])
            section_image_data = value['section_image_full_names']
            if section_image_data:
                section_image_full_names = "|".join([ item['image_full_name']+';imageSizeId_'+ str(item['image_size_info']['section_image_size_id']) for item in section_image_data])
            else:
                section_image_full_names = ''
            section_detail_rows = value['section_detail_rows']
            #  insert info into quote_section_info table
            insert_into_quote_section_info_table(copied_quote_id, section_name_id, section_image_full_names)

            # isert into quote_details table
            for row in section_detail_rows:
                insert_into_quote_details_table(copied_quote_id, 
                                                section_name_id, 
                                                row['section_sub_heading'], 
                                                row['section_image_row'], 
                                                row['section_text'], 
                                                row['section_qty_row'], 
                                                row['section_unit_cost_row'],
                                                row['section_total_cost_row']
                                            )
        
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#--------------------------------------------------------------------------------------------#








#--------------------------------------------------------------------------------------------#

# def copy_data():
#     old_data=[]
#     sql = ''' SELECT * FROM quote_details_table_xx '''
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     cursor.close()
        # connection.close()

#     for row in rows:
#         old_data.append({key: row[key] for key in row.keys() if key != 'id' })


#     for row in old_data:
#         col_name = ",".join(row.keys())

#         connection = create_db_connection()
#         cursor = connection.cursor()
#         sql = ''' INSERT INTO quote_details_table (quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row) VALUES (?,?,?,?,?,?,?,?) '''
#         cursor.execute(sql, [value for key,value in row.items()])
#         connection.commit()
#         cursor.close()
        # connection.close()

#         # whenever there's a successful insetion, we will make a backup of the backend pt_database
#         # backup_db()

# copy_data()

###--------------------------- Company (CabTek) info db manager -----------------------------------###

# def create_company_info_table():
#     sql = ''' CREATE TABLE IF NOT EXISTS company_info_table (
#             id Integer PRIMARY KEY AUTOINCREMENT,
#             company_name TEXT,
#             phone_no TEXT ,
#             fax TEXT,
#             email_id TEXT,
#             abn TEXT,
#             logo_path TEXT,
#             company_name_lower_case TEXT,
#             gst REAL
#         )'''
#     connection = create_db_connection()
#     connection.execute(sql)
#     cursor.close()
        # connection.close()


# def insert_into_company_info_table(company_name, phone_no, fax, email_id, abn ,logo_path, gst=10):
#     try:
#         company_name_lower_case = company_name.strip().lower()

#         connection = create_db_connection()
#         cursor = connection.cursor()
#         sql = ''' INSERT INTO company_info_table (company_name, phone_no, fax, email_id ,abn, logo_path, company_name_lower_case,gst) 
#                 VALUES (?,?,?,?,?,?,?,?) '''
#         cursor.execute(sql, [company_name, phone_no, fax, email_id, abn, logo_path, company_name_lower_case,gst])
#         connection.commit()
#         cursor.close()
        # connection.close()

#     except:
#         pass

# def get_company_info_by_id(id):
#     company_info = {}
#     try:
#         sql = f' SELECT * FROM company_info_table WHERE id = ? '
#         connection = create_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(sql, [id])
#         row = cursor.fetchone()
#         cursor.close()
        # connection.close()

#         if row != None:
#             company_info = {key: row[key] for key in row.keys()}

#         return company_info
#     except:
#         return company_info



# def get_all_company_info():
#     companies = []
#     try:
#         sql = ''' SELECT * FROM company_info_table ORDER BY company_name ASC'''
#         connection = create_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(sql)
#         rows = cursor.fetchall()
#         cursor.close()
        # connection.close()

#         for row in rows:
#             companies.append({key: row[key] for key in row.keys()})

#         return companies
#     except:
#         return companies