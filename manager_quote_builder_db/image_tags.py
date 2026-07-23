import inspect
from .core import create_db_connection

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
