import inspect
import helper
import manager_clickup_data as clickup_manager
from .core import create_db_connection

### --------------------------- Clients db manager -----------------------------------###

def create_clickup_clients_table():
    # Use ClickUp's task ID (e.g., '86ay8bx23') as primary key
    sql = ''' CREATE TABLE IF NOT EXISTS clickup_clients_table (
            id TEXT PRIMARY KEY,
            name TEXT ,
            company TEXT ,
            email TEXT ,
            phone TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


# Initialzied clickup clients table
def init_clickup_clients_table():
    connection = None

    # Named placeholders match dictionary keys: :id, :name, :company, :email, :phone
    sql = '''
            INSERT INTO clickup_clients_table (id, name, company, email, phone)
            VALUES (:id, :name, :company, :email, :phone);
        '''
    try:
        # If failed or there's no clickup contact data, skip init.
        clickup_client_data = clickup_manager.get_clickup_trade_contacts()
        if not clickup_client_data:
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        # Wipe the table clean
        cursor.execute("DELETE FROM clickup_clients_table;")

        # Pass the dictionary list directly
        cursor.executemany(sql, clickup_client_data)

        connection.commit()
        cursor.close()

        # update last init in the json file
        helper.update_clickup_client_table_last_init()

    except Exception as ex:
        if connection:
            connection.rollback()
        print(f'Error: "{ex}" [In function {inspect.stack()[0][3]}]')
    finally:
        if connection:
            connection.close()

def get_all_clickup_clients():
    connection = None
    all_clients = []
    sql = ''' SELECT * FROM clickup_clients_table ORDER BY company ASC'''

    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()

        for row in rows:
            all_clients.append({key: row[key] for key in row.keys()})

        return all_clients

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return all_clients
    finally:
        if connection:
            connection.close()
