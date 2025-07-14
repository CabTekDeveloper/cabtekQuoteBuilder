import sqlite3
import file_folder_paths


# Create DB Connection-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def create_db_connection():
    db_path = file_folder_paths.DB_PATH
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

# Drop Table-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def drop_table(table_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"DROP TABLE {table_name} ;"
    cursor.execute(sql)
    connection.commit()
    connection.close()

# Create Tables-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def create_programs_table():
    sql = ''' CREATE TABLE IF NOT EXISTS programs_table (
            program_id Integer PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL UNIQUE
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def create_issues_table():
    sql = ''' CREATE TABLE IF NOT EXISTS issues_table (
            issue_id Integer PRIMARY KEY AUTOINCREMENT,
            program_id Integer NOT NULL,
            issue_name TEXT NOT NULL,
            cause TEXT NOT NULL,
            solution TEXT NOT NULL,
            example TEXT
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()


def create_files_table():
    sql = ''' CREATE TABLE IF NOT EXISTS files_table (
            file_id Integer PRIMARY KEY AUTOINCREMENT,
            issue_id Integer NOT NULL,
            file_type TEXT NOT NULL,
            file_path TEXT NOT NULL
        )'''
    connection = create_db_connection()
    connection.execute(sql)
    connection.close()

# Insert data into DB-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def insert_into_files_table(issue_id,file_type,file_path):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = ''' INSERT INTO files_table (issue_id,file_type,file_path) 
            VALUES (?,?,?) '''
    cursor.execute(sql, [issue_id, file_type, file_path])
    connection.commit()
    connection.close()

def insert_into_programs_table(program_name):
    program_name = program_name.strip().title()
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = ''' INSERT INTO programs_table (program_name) VALUES (?) '''
    cursor.execute(sql, [program_name])
    connection.commit()
    connection.close()

def insert_into_issues_table(program_id, issue_name, cause, solution, example, added_by):
    current_issue_id = None
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = ''' INSERT INTO issues_table (program_id,issue_name,cause,solution,example,added_by) 
            VALUES (?,?,?,?,?,?) '''
    cursor.execute(sql, [program_id, issue_name, cause, solution, example,added_by])
    connection.commit()
    current_issue_id = cursor.lastrowid
    connection.close()
    return current_issue_id

# Read DB Data-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def get_all_programs():
    all_programs = []
    try:
        sql = ''' SELECT * FROM programs_table '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        for row in rows:
            all_programs.append({key: row[key] for key in row.keys()})

        connection.close()

        return all_programs

    except:
        return all_programs


def get_prog_id_by_prog_name(program_name):
    program_id = None

    try:
        program_name = program_name.strip()
        sql = f' SELECT program_id FROM programs_table WHERE program_name Like ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_name])

        row = cursor.fetchone()
        if row != None:
            program_id = row['program_id']

        connection.close()

        return program_id
    except:
        return program_id


def get_prog_name_by_prog_id(program_id):
    program_name = None

    try:
        sql = f' SELECT program_name FROM programs_table WHERE program_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_id])

        row = cursor.fetchone()
        if row != None:
            program_name = row['program_name']

        connection.close()

        return program_name
    except:
        return program_name


def get_issues_by_prog_id(program_id):
    issues_by_prog_id = []

    try:
        sql = f' SELECT * FROM issues_table WHERE program_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_id])

        rows = cursor.fetchall()
        if rows != None:
            for row in rows:
                issues_by_prog_id.append({key: row[key] for key in row.keys()})

        connection.close()

        return issues_by_prog_id
    except:
        return issues_by_prog_id


def get_single_issue(issue_id):
    single_issue = {}
    try:
        sql = f' SELECT * FROM issues_table WHERE issue_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [issue_id])

        row = cursor.fetchone()
        if row != None:
            single_issue = {key: row[key] for key in row.keys()}

        connection.close()

        return single_issue
    except:
        return single_issue


def get_files_by_issue_id(issue_id):
    files_by_issue_id = []

    try:
        sql = f' SELECT * FROM files_table WHERE issue_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [issue_id])

        rows = cursor.fetchall()
        if rows != None:
            for row in rows:
                files_by_issue_id.append({key: row[key] for key in row.keys()})

        connection.close()

        return files_by_issue_id
    except:
        return files_by_issue_id


def get_single_file(file_id):
    single_file = {}
    try:
        sql = f' SELECT * FROM files_table WHERE file_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [file_id])

        row = cursor.fetchone()
        if row != None:
            single_file = {key: row[key] for key in row.keys()}

        connection.close()

        return single_file
    except:
        return single_file


# Update DB Data -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def update_issue(issue_id, program_id, issue_name, cause, solution, example,added_by):
    try:
        # sql = " UPDATE issues_table SET (program_id=?,issue_name=?,cause=?,solution=?,example=?) WHERE issue_id = ? "
        sql = '''   UPDATE issues_table 
                    SET program_id=?,
                        issue_name=?,
                        cause=?,
                        solution=?,
                        example=?,
                        added_by=? 
                    WHERE issue_id = ? ; '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_id, issue_name, cause, solution, example,added_by, issue_id])

        connection.commit()
        connection.close()
    except:
        pass

def update_program_name(program_id,new_program_name):
    try:
        sql = '''   UPDATE programs_table 
                    SET program_name=?
                    WHERE program_id = ? ; '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [new_program_name,program_id])
        connection.commit()
        connection.close()
    except:
        pass

# Delete DB data-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def delete_single_issue(issue_id):
    try:
        sql = f' DELETE FROM issues_table WHERE issue_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [issue_id])
        connection.commit()
        connection.close()
    except:
        pass

def delete_single_file(file_id):
    try:
        sql = f' DELETE FROM files_table WHERE file_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [file_id])
        connection.commit()
        connection.close()
    except:
        pass

def delete_files_using_issue_id(issue_id):
    try:
        sql = f' DELETE FROM files_table WHERE issue_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [issue_id])
        connection.commit()
        connection.close()
    except:
        pass

def delete_issues_by_prog_id(program_id):
    try:
        sql = f' DELETE FROM issues_table WHERE program_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_id])
        connection.commit()
        connection.close()
    except:
        pass

def delete_program_by_prog_id(program_id):
    try:
        sql = f' DELETE FROM programs_table WHERE program_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [program_id])
        connection.commit()
        connection.close()
    except:
        pass
# delete_program_by_prog_id(8)
###-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

# # *Very Important
# #  Run this function only if you know what you are doing and  want to reset the database.
# #  Check if the database is not empty and contains important data because the function below will erase them.

# def drop_and_recreate_tables():
#     drop_table('programs_table')
#     create_programs_table()
#     drop_table('issues_table')
#     create_issues_table()
#     drop_table('files_table')
#     create_files_table()


# Alter DB table -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def alter_table_name(table_name, new_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} RENAME TO {new_name};"
    cursor.execute(sql)
    connection.commit()
    connection.close()

## Add new column with default value, modify the sql as per the requirement.
def add_column():
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE issues_table ADD COLUMN added_by TEXT NOT NULL DEFAULT 'add_name';"
    cursor.execute(sql)
    connection.commit()
    connection.close()

###-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
