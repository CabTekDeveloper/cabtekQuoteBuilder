import inspect
from .core import create_db_connection

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
