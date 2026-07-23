import inspect
from .core import create_db_connection
from .quotes import get_quote_name_by_quote_id
from .section_names import get_section_name_by_section_name_id

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
