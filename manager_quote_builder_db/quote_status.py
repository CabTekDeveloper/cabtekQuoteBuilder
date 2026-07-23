import inspect
from .core import create_db_connection

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
