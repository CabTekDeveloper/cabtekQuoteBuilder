import inspect
from .core import create_db_connection

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
