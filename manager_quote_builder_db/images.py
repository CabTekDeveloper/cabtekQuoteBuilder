import inspect
from .core import create_db_connection

### -------------------------- Images db manager-----------------------------------------###

def create_images_table():
    sql = ''' CREATE TABLE IF NOT EXISTS images_table (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_full_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            image_name_lower_no_ext TEXT,
            image_tag_id INTEGER
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_images_table(image_full_name, image_path, image_tag_id = 0 ):
    try:
        image_name_lower_no_ext = image_full_name.split('.')[0].strip().lower()
        image_tag_id = int(image_tag_id)

        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO images_table (image_full_name, image_path, image_name_lower_no_ext, image_tag_id)
                VALUES (?,?,?,?) '''
        cursor.execute(
            sql, [image_full_name, image_path, image_name_lower_no_ext, image_tag_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_image_info_by_image_id(image_id):
    image_info = {}
    try:
        image_id= int(image_id)

        sql = f' SELECT * FROM images_table WHERE image_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return {key: row[key] for key in row.keys()} if row != None else image_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return image_info



def get_all_images():
    all_images = []
    try:
        sql = ''' SELECT * FROM images_table '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_images.append({key: row[key] for key in row.keys()})

        return all_images
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_images

# print(get_all_images()[0])

def get_all_images_by_tag_id(image_tag_id):
    all_images_by_tag_id = []
    try:
        image_tag_id= int(image_tag_id)
        sql = ''' SELECT * FROM images_table WHERE image_tag_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_tag_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_images_by_tag_id.append({key: row[key] for key in row.keys()})

        return all_images_by_tag_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_images_by_tag_id


def get_searched_images(search_str):
    searched_images = []
    try:
        search_str = '%' + search_str.strip().lower() + '%'
        sql = ''' SELECT * FROM images_table WHERE image_name_lower_no_ext LIKE  ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [search_str])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            searched_images.append({key: row[key] for key in row.keys()})

        return searched_images
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return searched_images


# Note that image_full_name includes extention too.
def check_image_name_exists(image_full_name, image_tag_id):
    try:
        image_name_lower_no_ext = image_full_name.split('.')[0].strip().lower()
        image_tag_id = int(image_tag_id)

        sql = f' SELECT * FROM images_table WHERE image_name_lower_no_ext = ? AND image_tag_id=?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_name_lower_no_ext, image_tag_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False

def delete_image_by_image_id(image_id):
    try:
        image_id = int(image_id)

        sql = ''' DELETE FROM images_table WHERE image_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_id])
        connection.commit()
        cursor.close()
        connection.close()

        return True
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False
