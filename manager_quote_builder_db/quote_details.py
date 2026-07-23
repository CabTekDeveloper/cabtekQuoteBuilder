import inspect
from .core import create_db_connection

### --------------------------- Quote Details db manager -----------------------------------###


def create_quote_details_table():
    sql = ''' CREATE TABLE IF NOT EXISTS quote_details_table (
            quote_id INTEGER NOT NULL,
            section_name_id INTEGER NOT NULL,
            section_sub_heading TEXT,
            section_image_row TEXT,
            section_text TEXT,
            section_qty_row INTEGER,
            section_unit_cost_row REAL,
            section_total_cost_row REAL
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def insert_into_quote_details_table(quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quote_details_table (quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row) VALUES (?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, [quote_id, section_name_id, section_sub_heading, section_image_row, section_text, section_qty_row, section_unit_cost_row, section_total_cost_row])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_quote_details_by_quote_id(quote_id):
    quote_details_by_quote_id = []
    try:
        sql = ''' SELECT * FROM quote_details_table WHERE quote_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quote_details_by_quote_id.append(
                {key: row[key] for key in row.keys()})

        return quote_details_by_quote_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_details_by_quote_id




def get_quote_details_by_quoteId_and_sectionId(quote_id,section_name_id):
    quote_details_by_quoteId_and_sectionId = []
    try:
        sql = ''' SELECT * FROM quote_details_table WHERE quote_id = ? AND  section_name_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id,section_name_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quote_details_by_quoteId_and_sectionId.append(
                {key: row[key] for key in row.keys()})

        return quote_details_by_quoteId_and_sectionId
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_details_by_quoteId_and_sectionId



def check_quote_detials_exists_by_quoteId_and_sectionId(quote_id, section_name_id):
    try:
        sql = f' SELECT * FROM quote_details_table WHERE quote_id = ? AND section_name_id = ? '
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


def delete_quote_detials_by_quoteId_and_sectionId(quote_id, section_name_id):
    sql = ''' DELETE FROM quote_details_table WHERE quote_id = ? AND section_name_id = ? '''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quote_id, section_name_id])
    connection.commit()
    cursor.close()
    connection.close()


def delete_quote_details_by_quote_id(quote_id):
    sql = ''' DELETE FROM quote_details_table WHERE quote_id = ?'''
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quote_id])
    connection.commit()
    cursor.close()
    connection.close()
