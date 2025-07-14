from werkzeug.utils import secure_filename
import os
import sqlite3

import file_folder_paths
import helper

# Table names-----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
tbl_productType             = "tbl_productType"
tbl_products                = "tbl_products"
tbl_part                    = "tbl_part"
tbl_cncCode                 = "tbl_cncCode"
tbl_parameter               = "tbl_parameter"
tbl_product_info            = "tbl_product_info"
tbl_imageNames              = "tbl_imageNames"

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
 
def drop_column(table_name, column_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
    cursor.execute(sql)
    connection.commit()
    connection.close()

 
def alter_table_name(table_name, new_name):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} RENAME TO {new_name};"
    cursor.execute(sql)
    connection.commit()
    connection.close()

def add_column(table_name, column_name, data_type):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type} DEFAULT '';"
    cursor.execute(sql)
    connection.commit()
    connection.close()


# tbl_productType -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
# def create_tbl_productType():
    # sql = f''' CREATE TABLE IF NOT EXISTS {tbl_productType} (
    #         id Integer PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL UNIQUE,
    #         description TEXT
    #     )'''
    # connection = create_db_connection()
    # connection.execute(sql)
    # connection.close()


def insert_into_tbl_productType(name,description):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {'' } (name,description) VALUES (?,?) '''
        cursor.execute(sql, [name, description])
        connection.commit()
        connection.close()
    except:
        connection.close()

def get_product_type_info_by_id(product_type_id):
    db_data = {}
    try:
        id = int(product_type_id)
        sql = f' SELECT * FROM {tbl_productType} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: db_data = {key: row[key] for key in row.keys()}
        
        return db_data

    except:
        connection.close()
        return db_data 
    
# print(get_product_type_info_by_id(1))

def get_all_product_types():
    all_product_types = []
    try:
        sql = f''' SELECT * FROM {tbl_productType} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            all_product_types.append({key: row[key] for key in row.keys()})

        connection.close()

        return all_product_types

    except:
        connection.close()
        return all_product_types
    

# tbl_products -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
# def create_tbl_products():
    # sql = f''' CREATE TABLE IF NOT EXISTS {tbl_products} (
    #         id Integer NOT NULL UNIQUE,
    #         name TEXT NOT NULL,
    #         product_type_id Integer NOT NULL,
    #         part_ids TEXT,       
    #         cnccode_ids TEXT,       
    #     )'''
    # connection = create_db_connection()
    # connection.execute(sql)
    # connection.close()


def insert_into_tbl_products(id, name, product_type_id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_products} (id, name, product_type_id) VALUES (?,?,?) '''
        cursor.execute(sql, [id,name, product_type_id])
        connection.commit()
        connection.close()
        
        return True
    except:
        connection.close()
        return False

def get_all_products():
    all_products = []
    try:
        sql = f''' SELECT * FROM {tbl_products} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            all_products.append({key: row[key] for key in row.keys()})

        connection.close()
        return all_products

    except:
        connection.close()
        return all_products
    
def get_product_info_by_id(product_id):
    db_data = {}
    try:
        id = int(product_id)
        sql = f' SELECT * FROM {tbl_products} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: db_data = {key: row[key] for key in row.keys()}
        
        return db_data

    except:
        connection.close()
        return db_data



def get_products_by_product_type_id(product_type_id):
    filtered_products = []
    try:
        sql = f' SELECT * FROM {tbl_products} WHERE product_type_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_type_id])
        rows = cursor.fetchall()
  
        for row in rows:
            filtered_products.append({key: row[key] for key in row.keys()})
        connection.close()
        return filtered_products

    except:
        connection.close()
        return filtered_products
    
# tbl_part -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

# def create_tbl_partName():
#     sql = f''' CREATE TABLE IF NOT EXISTS {tbl_part} (
#                 id Integer PRIMARY KEY AUTOINCREMENT ,
#                 name TEXT NOT NULL UNIQUE 
#             )'''
#     connection = create_db_connection()
#     connection.execute(sql)
#     connection.close()


def insert_into_tbl_part(name):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_part} (name) 
                  VALUES (?) '''
        cursor.execute(sql, [name])
        connection.commit()
        connection.close()
        return True
    except:
        connection.close()
        return False


def get_all_parts():
    db_data = []
    try:
        sql = f''' SELECT * FROM {tbl_part} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            db_data.append({key: row[key] for key in row.keys()})

        connection.close()
        return db_data

    except:
        connection.close()
        return db_data

def get_part_info_by_id(id):
    part_info = {}
    try:
        id = int(id)
        sql = f' SELECT * FROM {tbl_part} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: part_info = {key: row[key] for key in row.keys()}
        
        return part_info

    except:
        connection.close()
        return part_info

# tbl_cncCode -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
# def create_tbl_cncCode():
#     sql = f''' CREATE TABLE IF NOT EXISTS {tbl_cncCode} (
#                 id Integer PRIMARY KEY AUTOINCREMENT ,
#                 name TEXT NOT NULL UNIQUE ,
#                 parameter_ids TEXT,
#                 image_ids TEXT,
#                 description TEXT
#             )'''
#     connection = create_db_connection()
#     connection.execute(sql)
#     connection.close()   

# create_tbl_cncCode() 

def insert_into_tbl_cncCode(name):
    try:
        name = name.upper()
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_cncCode} (name)  VALUES (?) '''
        cursor.execute(sql, [name])
        connection.commit()
        connection.close()
        return True
    except:
        connection.close()
        return False
    

def get_all_cnccodes():
    db_data = []
    try:
        sql = f''' SELECT * FROM {tbl_cncCode} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        connection.close()
        
        for row in rows:
            db_data.append({key: row[key] for key in row.keys()})

    
        for i in range (len(db_data)):
            db_data[i]['parameter_ids'] = helper.split_string_into_list(db_data[i]['parameter_ids']) 
            db_data[i]['image_ids'] = helper.split_string_into_list(db_data[i]['image_ids']) 
            
        
        return db_data

    except:
        connection.close()
        return db_data

  
def get_cnccode_info_by_id(cnccode_id):
    cnccode_info = {}
    try:
        id = int(cnccode_id)
        sql = f' SELECT * FROM {tbl_cncCode} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: 
            cnccode_info = {key: row[key] for key in row.keys()}
            # Convert parameter_ids and image_ids into lists
            cnccode_info['parameter_ids'] = helper.split_string_into_list(cnccode_info['parameter_ids'])  
            cnccode_info['image_ids'] = helper.split_string_into_list(cnccode_info['image_ids'])    
              
        return cnccode_info

    except:
        connection.close()
        return cnccode_info


def update_parameter_ids_in_tbl_cnccode(cnccode_id, parameter_ids):
    try:
        id = int(cnccode_id)
        parameter_ids = helper.join_list(parameter_ids)
        sql = f''' UPDATE {tbl_cncCode} 
                    SET parameter_ids = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [parameter_ids, id ])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False    

def update_image_ids_in_tbl_cnccode(cnccode_id, image_ids):
    try:
        id = int(cnccode_id)
        image_ids = helper.join_list(image_ids)
        sql = f''' UPDATE {tbl_cncCode} 
                    SET image_ids = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_ids, id ])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False   

def update_description_in_tbl_cnccode(cnccode_id, description):
    try:
        id = int(cnccode_id)
        sql = f''' UPDATE {tbl_cncCode} 
                    SET description = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [description, id])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False   
    
# tbl_parameter -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
# def create_tbl_parameter():
    # sql = f''' CREATE TABLE IF NOT EXISTS {tbl_parameter} (
    #         id Integer PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL UNIQUE,
    #         default_value REAL,
    #         min_value REAL,
    #         max_value REAL,
    #         image_ids TEXT,
    #         description TEXT
    #     )'''
    # connection = create_db_connection()
    # connection.execute(sql)
    # connection.close()

# create_tbl_parameter()



def insert_into_tbl_parameter(name):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_parameter} (name)  VALUES (?) '''
        cursor.execute(sql, [name])
        connection.commit()
        connection.close()
        return True
    except:
        return False

def get_all_parameters():
    db_data = []
    try:
        sql = f''' SELECT * FROM {tbl_parameter} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            db_data.append({key: row[key] for key in row.keys()})

        # Convert image_ids into a list
        for i in range (len(db_data)):
            db_data[i]['image_ids'] = helper.split_string_into_list(db_data[i]['image_ids']) 
            
        connection.close()
        return db_data

    except:
        connection.close()
        return db_data


def get_parameter_info_by_id(parameter_id):
    db_data = {}
    try:
        id = int(parameter_id)
        sql = f' SELECT * FROM {tbl_parameter} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: 
            db_data = {key: row[key] for key in row.keys()}
            # Convert image_ids into lists
            db_data['image_ids'] = helper.split_string_into_list(db_data['image_ids'])    
              
        return db_data

    except:
        connection.close()
        return db_data

def update_image_ids_in_tbl_parameter(parameter_id, image_ids):
    try:
        id = int(parameter_id)
        image_ids = helper.join_list(image_ids)
        sql = f''' UPDATE {tbl_parameter} 
                    SET image_ids = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [image_ids, id ])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False   
    
def update_parameter_values_in_tbl_parameter(parameter_id, default_value, min_value, max_value):
    try:
        id = int(parameter_id)
        sql = f''' UPDATE {tbl_parameter} 
                    SET default_value = ?,
                    min_value = ?,
                    max_value = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [default_value, min_value, max_value, id ])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False  

def update_description_in_tbl_parameter(parameter_id, description):
    try:
        id = int(parameter_id)
        sql = f''' UPDATE {tbl_parameter} 
                    SET description = ?
                    WHERE id = ? '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [description, id])
        connection.commit()
        cursor.close()
        connection.close()
               
        return True
    except:
        connection.close()
        return False   

# tbl_product_info -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

# def create_tbl_product_info():
#     sql = f''' CREATE TABLE IF NOT EXISTS {tbl_product_info} (
#                 product_id Integer NOT NULL,
#                 part_id Integer NOT NULL,
#                 cnccode_ids TEXT,       
#                 UNIQUE (product_id, part_id)
#             )'''
#     connection = create_db_connection()
#     connection.execute(sql)
#     connection.close()

# drop_table(tbl_product_infoxxx)
# create_tbl_product_info()
        
    
def insert_into_tbl_product_info(product_id, part_id):
    try:
        cnccode_ids =""
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_product_info} (product_id, part_id, cnccode_ids)  VALUES (?,?,?) '''
        cursor.execute(sql, [product_id, part_id, cnccode_ids])
        connection.commit()
        connection.close()
        return True
    except Exception as ex:
        print(ex)
        connection.close()
        return False

def check_product_part_exists_in_tbl_product_info(product_id, part_id):
    try:
        product_id = int (product_id)
        part_id = int (part_id)
        
        sql = f' SELECT * FROM {tbl_product_info} WHERE product_id = ? AND part_id = ?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_id, part_id])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False
    
    except Exception as ex:
        print(ex)
        connection.close()
        return False


def get_product_parts_by_id_from_tbl_product_info(product_id):
    product_info = []
    try:
        product_id = int (product_id)
        sql = f' SELECT * FROM {tbl_product_info} WHERE product_id=? ORDER BY part_id ASC'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_id])
        rows = cursor.fetchall()
        connection.close()
        
        for row in rows:
            product_info.append({key: row[key] for key in row.keys()})

        # Convert cnccode_ids into a list
        for i in range (len(product_info)):
            product_info[i]['cnccode_ids'] = helper.split_string_into_list(product_info[i]['cnccode_ids'])      
                                  
        return product_info

    except Exception as ex:
        print(ex)
        connection.close()
        return []


def get_cnccode_ids_from_tbl_product_info(product_id, part_id):
    cnccode_ids = []
    try:
        product_id = int (product_id)
        part_id = int (part_id)
        
        sql = f' SELECT cnccode_ids FROM {tbl_product_info} WHERE product_id=? AND part_id=?'
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_id, part_id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None:  
            cnccode_ids = helper.split_string_into_list(row['cnccode_ids'])
            
        return cnccode_ids

    except Exception as ex:
        print(ex)
        connection.close()
        return cnccode_ids
    

def update_cnccode_ids_in_tbl_product_info(product_id, part_id, cnccode_ids=[]):
    try:
        product_id = int(product_id)
        part_id = int(part_id)
        cnccode_ids = helper.join_list(cnccode_ids)
        
        
        sql = f''' UPDATE {tbl_product_info} 
                    SET cnccode_ids = ?
                  WHERE product_id = ? AND part_id = ?'''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [cnccode_ids, product_id, part_id ])
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as ex:
        print(ex)
        connection.close()
        return False

# update_cnccodes_in_tbl_product_info(415,2,[3,4])

def delete_single_part_from_tbl_product_info(product_id, part_id):
    try:
        product_id  = int(product_id)
        part_id     = int(part_id)
        
        sql = f' DELETE FROM {tbl_product_info} WHERE product_id = ? AND part_id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_id, part_id])
        connection.commit()
        connection.close()
        
        return True
    except Exception as ex:
        print(ex)
        connection.close()
        return False


def delete_all_parts_by_id_from_tbl_product_info(product_id):
    try:
        product_id  = int(product_id)
        sql = f' DELETE FROM {tbl_product_info} WHERE product_id = ?  '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [product_id])
        connection.commit()
        connection.close()
        
        return True
    except Exception as ex:
        print(ex)
        connection.close()
        return False

 # tbl_imageNamesNames -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

# def create_tbl_imageNames():
#     sql = f''' CREATE TABLE IF NOT EXISTS {tbl_imageNames} (
#             id Integer PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL UNIQUE
#         )'''
#     connection = create_db_connection()
#     connection.execute(sql)
#     connection.close()

# drop_table(tbl_imageNamesxxx)
# create_tbl_imageNames()

def insert_into_tbl_imageNames(image_name):
    try:
        name = image_name.strip()
        connection = create_db_connection()
        cursor = connection.cursor()
        sql = f''' INSERT INTO {tbl_imageNames} (name)  VALUES (?) '''
        cursor.execute(sql, [name])
        connection.commit()
        connection.close()
        return True
    except Exception as ex:
        print(ex)
        return False


def check_imageName_exists_in_tbl_imageNames(name):
    try:
        name = name.strip()
        
        sql = f' SELECT * FROM {tbl_imageNames} WHERE name = ? COLLATE NOCASE '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [name])
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        return True if row != None else False

    except Exception as ex:
        connection.close()
        return False
    

def get_image_info_by_id(id):
    db_data = {}
    try:
        id = int(id)
        sql = f' SELECT * FROM {tbl_imageNames} WHERE id = ? '
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        row = cursor.fetchone()
        connection.close()
        
        if row != None: 
            db_data = {key: row[key] for key in row.keys()}
            # added image_path field
            db_data['image_path'] = f"{file_folder_paths.FOLDER_PATH_CP_IMAGES}/{db_data['name']}"
        
        return db_data

    except:
        connection.close()
        return db_data
 
 
def get_all_images():
    db_data = []
    try:
        sql = f''' SELECT * FROM {tbl_imageNames} '''
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            db_data.append({key: row[key] for key in row.keys()})

        # added image_path field
        for i in range(len(db_data)):  
                db_data[i]['image_path'] = f"{file_folder_paths.FOLDER_PATH_CP_IMAGES}/{db_data[i]['name']}"
                
        connection.close()
        return db_data

    except:
        connection.close()
        return db_data
 
# Build Product Info by product_id -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###

def build_product_info(product_id):
    product_info = {}
    try:
        product_id= int(product_id)
        product = get_product_info_by_id(product_id)
        product_type = get_product_type_info_by_id(product['product_type_id'])
        
        product_info = {
            "id"    : product_id,
            "name"  : product['name'],
            "product_type_id"   : product_type['id'],
            "product_type"      : product_type['name'],
            "parts" : []
        }

        product_parts = get_product_parts_by_id_from_tbl_product_info(product_id)

        for part in product_parts:
            part_info = get_part_info_by_id(part['part_id'])
            # Add a new list of cnccodes from cnccode_ids
            cnccode_ids = part["cnccode_ids"]
            part_info['cnccodes'] = [get_cnccode_info_by_id(id) for id in cnccode_ids ]
            # Add part_info to product_info parts
            product_info['parts'].append(part_info)
            
        return product_info
 
    except:
        
        return {}
 

# print(build_product_info(415))
# print(get_part_info_by_id(1))
# build_product_info(415)

def build_cnccode_info(cnccode_id):
    try:
        cnccode_info = {}
        cnccode_info = get_cnccode_info_by_id(cnccode_id)
        
        if cnccode_info:
            # Add a new list of parameters info from parameter_ids
            parameter_ids = cnccode_info['parameter_ids']
            cnccode_info['parameters'] = [get_parameter_info_by_id(id) for id in parameter_ids ]

            # Add a new list of images info from image_ids
            image_ids = cnccode_info['image_ids']
            images = [get_image_info_by_id(id) for id in image_ids ]
            
            # for i in range(len(images)):    images[i]['image_path'] = f"{file_folder_paths.FOLDER_PATH_CP_IMAGES}/{images[i]['name']}"
            
            cnccode_info['images'] = images
            
            #Remove redundant info
            cnccode_info.pop("parameter_ids")
            cnccode_info.pop("image_ids")
            
        return cnccode_info
    except:
        return {}
 


def build_parameter_info(parameter_id):
    try:
        parameter_info = {}
        parameter_info = get_parameter_info_by_id(parameter_id)
        
        if parameter_info:
            # Add a new list of images info from image_ids
            image_ids = parameter_info['image_ids']
            images = [get_image_info_by_id(id) for id in image_ids ]
            
            # for i in range(len(images)):  images[i]['image_path'] = f"{file_folder_paths.FOLDER_PATH_CP_IMAGES}/{images[i]['name']}"
            
            parameter_info['images'] = images

            #Remove redundant info
            parameter_info.pop("image_ids")
            
        return parameter_info
    except:
        return {}
    
    
def update_product_parts_in_tbl_product_info(product_info):
    try:
        product_id = product_info['id']
        new_parts = product_info['parts']

        if new_parts:
            # Remove old parts from tbl_product_info if does not exists in the new parts list
            old_parts = get_product_parts_by_id_from_tbl_product_info(product_id)
            for old_part in old_parts:
                old_part_id = old_part['part_id']
                if not any(part['id'] == old_part_id for part in new_parts):
                    delete_single_part_from_tbl_product_info(product_id, old_part_id)
            
            # Now insert the new parts in tbl_product_info
            for part in new_parts:
                part_id = part['id']
                if not check_product_part_exists_in_tbl_product_info(product_id, part_id):
                    insert_into_tbl_product_info(product_id, part_id)
                
        else:
            # Remove all parts by product _id from tbl_product_info
            delete_all_parts_by_id_from_tbl_product_info(product_id)
        return True
    except:
        return False
    
    
def save_image_in_folder_and_tbl_images(img_obj):
    try:
        img_name = secure_filename(img_obj.filename)
        img_save_location = f"{file_folder_paths.FOLDER_PATH_CP_IMAGES}/{img_name}"
        
        # Before saving the image file, make sure it does not exists already in the folder or in the database
        if ( os.path.exists(img_save_location) == False):
            if(check_imageName_exists_in_tbl_imageNames(img_name) == False):
                insert_into_tbl_imageNames(img_name)
                img_obj.save(img_save_location)
                return True
            else:
                return False
        else:
            return False

    except:
        return False



