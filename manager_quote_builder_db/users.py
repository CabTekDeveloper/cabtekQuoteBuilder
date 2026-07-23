import inspect
from .core import create_db_connection

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
