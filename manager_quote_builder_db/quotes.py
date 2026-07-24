import inspect
import helper
from .core import create_db_connection

### -------------------------- Quotes db manager-----------------------------------------###

def create_quotes_table():
    # create quote_name_lower_case to store the lowered case quote_name. We can use it later to check if the quote name already exists in the database.
    sql = ''' CREATE TABLE IF NOT EXISTS quotes_table (
            quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_name TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            date_quote_created TEXT,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone_no TEXT,
            delivery_info TEXT,
            quote_name_lower_case TEXT,
            time_stamp INTEGER,
            rev_date TEXT,
            is_template TEXT,
            quote_status_id INTEGER,
            revision_dates TEXT,
            joinery_supply_type TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def update_quote_info_by_quote_id(new_quote_info):
    try:
        quote_id                = int(new_quote_info['quote_id'])
        quote_name              = new_quote_info['quote_name']
        customer_name           = new_quote_info['customer_name'].strip().title()
        customer_email          = new_quote_info['customer_email']
        customer_phone_no       = new_quote_info['customer_phone_no']
        delivery_info           = new_quote_info['delivery_info']
        is_template             = new_quote_info['is_template']
        quote_name_lower_case   = quote_name.strip().lower()
        time_stamp              = helper.get_cur_datetime()['timestamp']
        rev_date                = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        company_id              = int(new_quote_info['company_id'])
        is_trade_client         = new_quote_info['is_trade_client']
        customer_company        = new_quote_info['customer_company']
        delivery_type           = new_quote_info['delivery_type']
        ship_via                = new_quote_info['ship_via']

        sql = ''' UPDATE quotes_table
                SET quote_name = ?,
                customer_name = ?,
                customer_email = ?,
                customer_phone_no = ?,
                delivery_info = ?,
                quote_name_lower_case = ?,
                is_template = ?,
                time_stamp = ?,
                rev_date = ?,
                company_id = ?,
                is_trade_client = ?,
                customer_company =?,
                delivery_type=?,
                ship_via=?

                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name, customer_name, customer_email, customer_phone_no, delivery_info, quote_name_lower_case , is_template, time_stamp, rev_date, company_id,is_trade_client,customer_company,delivery_type, ship_via, quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def insert_into_quotes_table(quote_name, user_id, date_quote_created, customer_name="", customer_email="", customer_phone_no="", delivery_info="", is_template = "no" , company_id=0, is_trade_client="no", customer_company="",delivery_type="", ship_via=""):
    try:

        quote_name_lower_case = quote_name.strip().lower()
        customer_name=customer_name.strip().title()
        time_stamp = helper.get_cur_datetime()['timestamp']
        is_template = is_template.strip().lower()
        quote_status_id = 0
        rev_date = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        quote_status_id = 0
        joinery_supply_type = 'Supply of customised joinery'
        company_id= int(company_id)
        is_locked = "no"
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = ''' INSERT INTO quotes_table (quote_name,user_id,date_quote_created,customer_name,customer_email,customer_phone_no,delivery_info,quote_name_lower_case,time_stamp, rev_date, is_template, quote_status_id, joinery_supply_type, company_id,is_trade_client,customer_company,delivery_type,ship_via, is_locked)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, [quote_name, user_id, date_quote_created, customer_name, customer_email, customer_phone_no, delivery_info, quote_name_lower_case, time_stamp,rev_date, is_template, quote_status_id, joinery_supply_type, company_id,is_trade_client,customer_company,delivery_type,ship_via, is_locked])
        connection.commit()
        cursor.close()
        connection.close()

        # whenever there's a successful insetion, we will make a backup of the backend pt_database
        # backup_db()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        pass


def get_quote_info_by_quote_name(quote_name):
    quote_info = {}
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT * FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_info = {key: row[key] for key in row.keys()}
        return quote_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_info

# print(get_quote_info_by_quote_name("Testquote2"))

def get_quote_info_by_quote_id(quote_id):
    quote_info = {}
    try:
        quote_id = int(quote_id)

        sql = f' SELECT * FROM quotes_table WHERE quote_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_info = {key: row[key] for key in row.keys()}
        return quote_info
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_info

def check_quote_name_exists(quote_name):
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT * FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return False


def get_all_quotes():
    all_quotes = []
    try:
        sql = ''' SELECT * FROM quotes_table ORDER BY time_stamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            all_quotes.append({key: row[key] for key in row.keys()})

        return all_quotes
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_quotes


def get_quotes_by_user_id(user_id):
    quotes_by_user_id = []
    try:
        user_id = int(user_id)
        sql = ''' SELECT * FROM quotes_table WHERE user_id=? ORDER BY time_stamp DESC'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql,[user_id])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            quotes_by_user_id.append({key: row[key] for key in row.keys()})

        return quotes_by_user_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quotes_by_user_id

def get_quote_id_by_quote_name(quote_name):
    quote_id = None
    try:
        quote_name_lower_case = quote_name.strip().lower()

        sql = f' SELECT quote_id FROM quotes_table WHERE quote_name_lower_case = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_name_lower_case])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_id = row['quote_id']
        return quote_id
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_id


def get_quote_name_by_quote_id(quote_id):
    quote_name = ''
    try:
        sql = f' SELECT quote_name FROM quotes_table WHERE quote_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row != None:
            quote_name = row['quote_name']
        return quote_name
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return quote_name

# print(get_quote_name_by_quote_id(56))

def delete_quote_by_quote_id(quote_id):
    try:
        sql = ''' DELETE FROM quotes_table WHERE quote_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def update_quote_rev_date_and_time_stamp(quote_id):
    try:
        quote_id = int(quote_id)
        rev_date = f"{helper.get_cur_datetime()['date_today']} {helper.get_cur_datetime()['time_now']}"
        time_stamp = helper.get_cur_datetime()['timestamp']

        sql = ''' UPDATE quotes_table
                SET rev_date = ?,
                time_stamp = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [rev_date, time_stamp,  quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_quote_status_by_quote_id(quote_id, quote_status_id):
    try:
        quote_id = int(quote_id)
        quote_status_id = int(quote_status_id)
        sql = ''' UPDATE quotes_table
                SET quote_status_id = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [quote_status_id, quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_quote_revision_dates(quote_id, new_revision_dates):
    try:
        quote_id = int(quote_id)
        new_revision_dates = new_revision_dates.strip()

        sql = ''' UPDATE quotes_table
                SET revision_dates = ?
                WHERE quote_id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [new_revision_dates, quote_id ])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


def update_joinery_supply_type(quote_id, joinery_supply_type):
    try:
        quote_id = int(quote_id)
        joinery_supply_type = joinery_supply_type.strip()

        sql = ''' UPDATE quotes_table
                SET joinery_supply_type = ?
                WHERE quote_id = ? '''

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [joinery_supply_type, quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

def update_is_locked(quote_id, is_locked):
    try:
        quote_id = int(quote_id)
        is_locked = is_locked.strip()

        sql = ''' UPDATE quotes_table
                SET is_locked = ?
                WHERE quote_id = ? '''

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [is_locked, quote_id])
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')