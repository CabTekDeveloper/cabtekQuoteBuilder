import inspect
from .core import create_db_connection

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
        is_active= "yes"

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO section_names_table (section_name,section_name_lower_case,is_active)
                VALUES (?,?,?) '''
        cursor.execute(sql, [section_name, section_name_lower_case,is_active])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass

# insert_into_section_names_table("test")

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
        sql = ''' SELECT * FROM section_names_table WHERE is_active = 'yes' ORDER BY section_name COLLATE NOCASE  ASC '''
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
