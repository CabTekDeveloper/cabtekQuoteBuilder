import inspect
import helper
from .core import create_db_connection

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


def get_searched_texts(search_str,user_id=None):
    texts_by_user_id = []
    try:
        search_str = '%' + search_str.strip().lower() + '%'
        sql_parameters = []

        if user_id is None:
            sql = ''' SELECT * FROM texts_table WHERE text_lower_case LIKE  ? ORDER BY time_stamp DESC '''
            sql_parameters = [search_str]
        else:
            sql = ''' SELECT * FROM texts_table WHERE text_lower_case LIKE  ? AND  user_id = ? ORDER BY time_stamp DESC '''
            sql_parameters = [search_str, user_id]

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, sql_parameters)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            texts_by_user_id.append({key: row[key] for key in row.keys()})

        return texts_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return texts_by_user_id

# print(get_searched_texts("i"))

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
