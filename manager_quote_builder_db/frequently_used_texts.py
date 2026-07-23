import inspect
from .core import create_db_connection

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
