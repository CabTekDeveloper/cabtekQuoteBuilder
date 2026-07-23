import inspect
from .core import create_db_connection

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
