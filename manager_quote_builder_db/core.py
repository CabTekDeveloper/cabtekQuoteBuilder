from datetime import datetime
import shutil
import sqlite3
import helper
import file_folder_paths
###-------------------------------------------------------------------------------###

def create_db_connection():
    # QUOTING_DB_PATH = file_folder_paths.TEST_QUOTING_DB_PATH    # For Testing
    QUOTING_DB_PATH = file_folder_paths.LIVE_QUOTING_DB_PATH    # For deployment
    connection = sqlite3.connect(QUOTING_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

# Backup database-------------------------------------------------------------------------------###

def backup_db(current_user):
    try:
        # Delete old backups
        helper.delete_files_older_than_x_days(file_folder_paths.FOLDER_PATH_QUOTE_BUILDER_DB_BACKUP,30)

        db_name = file_folder_paths.QUOTING_DB_NAME
        db_to_copy = file_folder_paths.LIVE_QUOTING_DB_PATH
        backup_folder_path = file_folder_paths.FOLDER_PATH_QUOTE_BUILDER_DB_BACKUP

        # Copy db into backup folder
        shutil.copy(db_to_copy, backup_folder_path)

        # Build backup db name
        dt = datetime.now().strftime("%Y%m%d%H%M")
        backup_db_name = f"{dt}_{current_user}_{db_name}"

        # Rename the backup db
        backup_db_path = f"{backup_folder_path}//{db_name}"
        new_path = f"{backup_folder_path}//{backup_db_name}"
        shutil.move(backup_db_path, new_path)

    except Exception as ex:
        print(f'{ex} - backup_db')

# Alter table -------------------------------------------------------------------------------###

def drop_table(table_name):
    table_name = table_name.strip()
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"DROP TABLE {table_name} ;"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# drop_table("xx")

def alter_delete_column(table_name, column_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_delete_column(table_name = "quotes_tableX", column_name = "is_trade")

def alter_add_column(table_name, new_column_name, dataType):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column_name} {dataType};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_add_column(table_name= "section_names_table", new_column_name= "is_active", dataType= "TEXT")

def update_a_field(table_name, column_name, val):
    try:
        sql = f" UPDATE {table_name} SET {column_name} = ? "

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [val])
        connection.commit()
        cursor.close()
        connection.close()
    except:
        pass
# update_a_field(table_name= "section_names_table", column_name= "is_active", val= "yes")


def alter_rename_column(table_name, old_name, new_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} to {new_name};"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
# alter_rename_column(table_name= "quotes_table", old_name = "delivery_address", new_name= "delivery_type")

def alter_empty_column_values(table_name, column_name, default_value=""):
    connection = create_db_connection()
    cursor = connection.cursor()

    # Changed %s to ? for SQLite compatibility.
    # We target rows where the column is currently NULL.
    sql = f"""
        UPDATE {table_name}
        SET {column_name} = ?
        WHERE {column_name} IS NULL;
    """

    try:
        cursor.execute(sql, (default_value,))
        connection.commit()
        print(f"Successfully updated NULL fields in {table_name}.{column_name} to '{default_value}'")
    except Exception as e:
        connection.rollback()
        print(f"Error updating column: {e}")
    finally:
        cursor.close()
        connection.close()

# alter_empty_column_values(table_name="quotes_table",column_name="ship_via",default_value="")
