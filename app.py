# from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify, Markup
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify

from datetime import datetime
from werkzeug.utils import secure_filename
import os
from waitress import serve

import quote_builder_db_manager as quote_builder_db
import company_info_manager
import eo_excel_manager
import helper
import inspect

app = Flask(__name__)
app.secret_key = 'super secret key'


#----------------------------------------------------------------------------------------------#
@app.route('/index')
@app.route('/index/<showSavedTemplate>')
def index(showSavedTemplate = 'no'):
    try:
        if 'user_info' in session:
            current_user_id = session['user_info']['user_id']

            # get all quotes for the current user
            quotes_by_user_id = quote_builder_db.get_quotes_by_user_id(current_user_id)
            for i in range(len(quotes_by_user_id)):
                # find full_name using the user_id of each quote and append it to the record
                user_id = quotes_by_user_id[i]['user_id']
                quotes_by_user_id[i]['quoted_by'] = quote_builder_db.get_user_info_by_id(user_id)['full_name']
                
                # find quote_status using the quote_status_id of each quote and append it to the record
                quote_status_id = quotes_by_user_id[i]['quote_status_id']
                quotes_by_user_id[i]['quote_status'] = quote_builder_db.get_quote_status_name(quote_status_id)
            
            # check if user has saved quotes (we are not looking for quotes saved as template)
            has_saved_quotes = True if any(row['is_template'] == 'no' for row in quotes_by_user_id) else False
            has_saved_template_quotes = True if any(row['is_template'] == 'yes' for row in quotes_by_user_id) else False
            # print("Loading Index Page")
            return render_template('index.html', quotes_by_user_id = quotes_by_user_id, has_saved_quotes = has_saved_quotes, has_saved_template_quotes = has_saved_template_quotes, showSavedTemplate = showSavedTemplate)
        
        else:
            return render_template('login_error.html')
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

@app.route('/', methods=["POST", "GET"])
def login():
    try:
        if 'user_info' in session:
            session.pop('user_info')

        if request.method == "POST":
            user_name = request.form.get('user_name')
            user_password = request.form.get('user_password')
            user_info = quote_builder_db.get_user_info_by_user_name(user_name)

            if user_info and user_info['user_password'] == user_password:
                session['user_info'] = user_info
                
                # Wangchuk, 18-03-2025,
                quote_builder_db.backup_db(user_info['user_name'])
                
                return redirect(url_for('index'))
            else:
                flash("The username or password you entered is incorrect.")
                return render_template("login.html")
            
        if request.method == "GET": 
            return render_template('login.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    try:
        if 'user_info' in session:
            session.pop('user_info')

        flash("You are logged out.")
        return redirect(url_for('login'))

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

@app.route('/create_quote', methods=['POST', 'GET'])
def create_quote():
    try:
        if 'user_info' in session:
            date_today = f"{helper.get_cur_datetime()['date_today']}"
            all_company_info = company_info_manager.get_all_company_info()
            
            # POST method
            if request.method == "POST":
                new_quote_info = {
                    'quote_name'            : request.form['quote_name'].strip(),
                    'quoted_by'             : request.form['quoted_by'].strip().title(),
                    'date_quote_created'    : request.form['date_quote_created'].strip(),
                    'customer_name'         : request.form['customer_name'].strip(),
                    'customer_email'        : request.form['customer_email'].strip(),
                    'customer_phone_no'     : request.form['customer_phone_no'].strip(),
                    'delivery_info'         : request.form['delivery_info'].strip(),
                    'is_template'           : request.form['is_template'].strip() ,
                    'company_id'            : int(request.form['company_id'])
                }
                
                if "/" in new_quote_info['quote_name']:
                    flash(f'Quote name ( {new_quote_info["quote_name"]} ) cannot contain "/"')
                    return render_template('create_quote.html', date_today=date_today, new_quote_info = new_quote_info , all_company_info=all_company_info)
                
                if quote_builder_db.check_quote_name_exists(new_quote_info['quote_name']):
                    user_id = quote_builder_db.get_quote_info_by_quote_name(new_quote_info['quote_name'])['user_id']
                    full_name = quote_builder_db.get_user_info_by_id(user_id)['full_name']
                    flash(f'The quote name "{new_quote_info["quote_name"]}" is used by {full_name}.')
                    flash('Use a different quote name.')
                    return render_template('create_quote.html', date_today=date_today, new_quote_info = new_quote_info , all_company_info=all_company_info)
                else:
                    # store quote info in the db
                    user_id = quote_builder_db.get_user_info_by_full_name(new_quote_info['quoted_by'])['user_id']
                    quote_builder_db.insert_into_quotes_table(
                        new_quote_info['quote_name'], user_id, new_quote_info['date_quote_created'], new_quote_info['customer_name'], new_quote_info['customer_email'], 
                        new_quote_info['customer_phone_no'], new_quote_info['delivery_info'],new_quote_info['is_template'], new_quote_info['company_id'] )
                    return redirect(url_for('add_quote_details', quote_name=new_quote_info['quote_name']))
            
            # GET method
            if request.method == "GET":  
                return render_template('create_quote.html', date_today=date_today, all_company_info=all_company_info)
        
        else:
            return render_template('login_error.html')
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

@app.route('/edit_quote/<quote_id>', methods=['POST', 'GET'])
def edit_quote(quote_id):
    try:
        if 'user_info' in session:
            all_company_info = company_info_manager.get_all_company_info()
            # POST method
            if request.method == "POST":
                new_quote_info = {
                    'quote_id' :quote_id,
                    'quote_name' : request.form['quote_name'].strip(),
                    'quoted_by' : request.form['quoted_by'].strip().title(),
                    'date_quote_created' : request.form['date_quote_created'].strip(),
                    'customer_name' : request.form['customer_name'].strip(),
                    'customer_email' : request.form['customer_email'].strip(),
                    'customer_phone_no' : request.form['customer_phone_no'].strip(),
                    'delivery_info' : request.form['delivery_info'].strip(),
                    'is_template' : request.form['is_template'].strip(),
                    'company_id' : int(request.form['company_id'])
                }
                
                if "/" in new_quote_info['quote_name']:
                    flash(f'Quote name ( {new_quote_info["quote_name"]} ) cannot contain "/"')
                    return render_template('edit_quote.html', new_quote_info = new_quote_info , all_company_info=all_company_info)
                
                quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)
                quote_name = quote_info['quote_name']
                if quote_name.lower() == new_quote_info['quote_name'].lower() or (quote_builder_db.check_quote_name_exists(new_quote_info['quote_name']) == False):
                    quote_builder_db.update_quote_info_by_quote_id(new_quote_info)
                    return redirect(url_for('index', showSavedTemplate = new_quote_info['is_template']))
                else:
                    user_id = quote_builder_db.get_quote_info_by_quote_name(quote_name)['user_id']
                    full_name = quote_builder_db.get_user_info_by_id(user_id)['full_name']
                    flash(f'The quote name "{new_quote_info["quote_name"]}" is already used by {full_name}.')
                    flash('Use a different quote name.')
                    return render_template('edit_quote.html', new_quote_info = new_quote_info , all_company_info=all_company_info)
                
            # GET method
            if request.method == "GET":  
                quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)
                user_id = quote_info['user_id']
                quoted_by = quote_builder_db.get_user_info_by_id(user_id)['full_name']
                quote_info['quoted_by'] = quoted_by
                return render_template('edit_quote.html', quote_info = quote_info , all_company_info=all_company_info)
        
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#
@app.route('/add_quote_details/<quote_name>', methods=['GET'])
@app.route('/add_quote_details/<quote_name>/<add_new_section>/<section_name>', methods=['GET'])
def add_quote_details(quote_name, section_name = "none", add_new_section = "no"):
    try:
        if 'user_info' in session:
            selected_section_name = None
            user_id = session['user_info']['user_id']

            section_name = section_name.strip()
            add_new_section = add_new_section.strip()

            all_images = quote_builder_db.get_all_images()
            all_image_tags = quote_builder_db.get_all_image_tags()
            texts_by_user_id = quote_builder_db.get_texts_by_user_id(user_id)
            frequently_used_texts_by_user_id = quote_builder_db.get_frequently_used_texts_by_user_id(user_id)
            all_section_names = quote_builder_db.get_all_section_names()
            all_section_image_size = quote_builder_db.get_all_section_image_size()
            quote_data = quote_builder_db.get_quote_data(quote_name)
    
            quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
            quote_info['quoted_by'] = quote_builder_db.get_user_info_by_id(user_id)['full_name']
            
            eo_excel_text = []
            eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)

            if eo_excel_by_user_id :
                eo_excel_id = eo_excel_by_user_id[0]['id']
                eo_excel_text = quote_builder_db.get_eo_excel_text_by_eo_excel_id(eo_excel_id)
            
            # display the selected section name details
            if quote_name and section_name != 'none':
                selected_section_name = section_name
                return render_template('add_quote_details.html', all_images=all_images, quote_info=quote_info, texts_by_user_id=texts_by_user_id, all_section_names=all_section_names , quote_data =quote_data, selected_section_name = selected_section_name , page_name = 'add_quote_details' , eo_excel_text = eo_excel_text, all_image_tags = all_image_tags , all_section_image_size = all_section_image_size, frequently_used_texts_by_user_id = frequently_used_texts_by_user_id)
            
            # check if the user wants to add a new section and display add new section form accordingly
            if quote_name and add_new_section == 'yes':
                return render_template('add_quote_details.html', all_images=all_images, quote_info=quote_info, texts_by_user_id=texts_by_user_id, all_section_names=all_section_names , quote_data =quote_data, page_name = 'add_quote_details' , eo_excel_text = eo_excel_text , all_image_tags = all_image_tags, frequently_used_texts_by_user_id = frequently_used_texts_by_user_id)
            
            # if the user hasn't selected a section name nor intends to add a new section, we will display the first section of the quote if it has got one.
            if quote_name and section_name == 'none' and add_new_section == 'no':
                section_names = quote_data['section_names']
                if section_names:
                    selected_section_name = section_names[0]
                    return render_template('add_quote_details.html', all_images=all_images, quote_info=quote_info, texts_by_user_id=texts_by_user_id, all_section_names=all_section_names , quote_data =quote_data, selected_section_name = selected_section_name , page_name = 'add_quote_details' , eo_excel_text = eo_excel_text, all_image_tags = all_image_tags , all_section_image_size = all_section_image_size, frequently_used_texts_by_user_id = frequently_used_texts_by_user_id)
                else:
                    return render_template('add_quote_details.html', all_images=all_images, quote_info=quote_info, texts_by_user_id=texts_by_user_id, all_section_names=all_section_names , quote_data =quote_data, page_name = 'add_quote_details' , eo_excel_text = eo_excel_text , all_image_tags = all_image_tags, frequently_used_texts_by_user_id = frequently_used_texts_by_user_id)
            
            
        else:
            return render_template('login_error.html')

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

# Reorder section names routes
# 09-02-2024 
@app.route('/reorder_section_names_db', methods=['POST'])
def reorder_section_names_db():
    try:
        if 'user_info' in session:
            if request.method == "POST":
                data = request.get_json()
                quote_name = data['quote_name']
                ordered_section_names = data['ordered_section_names']
                quote_id = quote_builder_db.get_quote_id_by_quote_name(quote_name)
                
                section_order_no = 0
                for section_name in ordered_section_names:
                    section_order_no += 1
                    section_name_id = quote_builder_db.get_section_id_by_section_name(section_name)
                    quote_builder_db.update_quote_section_order_no(quote_id, section_name_id, section_order_no)

                return jsonify({"reordered": True})
                
        else:
            return render_template('login_error.html')
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

# image routes
@app.route('/save_image_info_to_db', methods=['POST'])
def save_image_info_to_db():
    if 'user_info' in session:
        if request.method == "POST":
            image_tag_name = request.form['image_tag_name']
            image_tag_id =quote_builder_db.get_image_tag_id_by_tag_name(image_tag_name)
            img_obj = request.files['uploadedFile']
            img_name = secure_filename(img_obj.filename)

            # If you look at the path below, you will see that static has been removed. This is done so that we can add this to img src in html files
            img_path = f"images/uploads/{img_name}"

            img_save_location = f"static/images/uploads/{img_name}"
            # Before saving the image file, make sure it does not exists already in the images/uploads folder or in the database
            # We have to make sure images stored in images/uploads folder have unique name.
            if ( os.path.exists(img_save_location) == False) and (quote_builder_db.check_image_name_exists(img_name, image_tag_id) == False):
                img_obj.save(img_save_location)
                quote_builder_db.insert_into_images_table(img_name, img_path, image_tag_id)

                return jsonify({"uploaded": True})
            else:
                return jsonify({"uploaded": False})
    else:
        return render_template('login_error.html')
    
@app.route('/get_all_images_db/<image_tag_id>', methods=["GET"])
@app.route('/get_all_images_db', methods=["GET"])
def get_all_images_db(image_tag_id = None):
    try:
        if image_tag_id == None:
            all_images = quote_builder_db.get_all_images()
        else:
            all_images = quote_builder_db.get_all_images_by_tag_id(image_tag_id)

        return jsonify(all_images)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

@app.route('/get_searched_images_db/<search_str>', methods=["GET"])
def get_searched_images_db(search_str):
    try:
        searched_images = quote_builder_db.get_searched_images(search_str)
        return jsonify(searched_images)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

@app.route('/delete_image_by_id_db', methods=["POST"])
def delete_image_by_id_db():
    try:
        if "user_info" in session:

            if request.method == "POST":
                data = request.get_json()
                image_id = data['image_id']

                image_info = quote_builder_db.get_image_info_by_image_id(image_id)
                img_save_location = f"static/{image_info['image_path']}" if image_info else ""
                if os.path.exists(img_save_location):
                    os.remove(img_save_location)

                if quote_builder_db.delete_image_by_image_id(image_id):
                    return jsonify({'deleted': True})
                else:
                    return jsonify({'deleted': False})
        else:
            return render_template('login_error.html')

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

@app.route('/get_all_section_image_size_db', methods=["GET"])
def get_all_section_image_size_db():
    try:
        all_section_image_size = quote_builder_db.get_all_section_image_size()
        return jsonify(all_section_image_size)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
# frequently used texts routes
@app.route('/get_frequently_used_texts_by_user_id_db', methods=["GET"])
def get_frequently_used_texts_by_user_id_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']
            frequently_used_texts_by_user_id = quote_builder_db.get_frequently_used_texts_by_user_id(user_id)
            return jsonify(frequently_used_texts_by_user_id)
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
@app.route('/add_text_to_frequently_used_table_db', methods=["POST"])
def add_text_to_frequently_used_table_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']
            if request.method == "POST":
                data = request.get_json()
                text = data['text']

                if quote_builder_db.check_frequently_used_text_exists(user_id, text):
                    quote_builder_db.update_frequently_used_text_count(user_id, text)
                else:
                    quote_builder_db.insert_into_frequently_used_text_table(user_id, text)
                
                return jsonify({"saved": True})
        else:
            return render_template('login_error.html')
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
@app.route('/delete_frequently_used_text_db', methods=["POST"])
def delete_frequently_used_text_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']

            if request.method == "POST":
                data = request.get_json()
                text_id = data['text_id']
                quote_builder_db.delete_frequently_used_text(text_id)
                return jsonify({"deleted" : True})

        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#
# text routes
@app.route('/save_texts_to_db', methods=['POST'])
def save_texts_to_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']
            
            if request.method == "POST":
                data = request.get_json()
                text = data['text'].strip()
                if quote_builder_db.check_text_exists(text) == False:
                    quote_builder_db.insert_into_texts_table(text, user_id)
                    return jsonify({"saved": True})
                else:
                    return jsonify({"saved": False})
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
@app.route('/get_texts_by_user_id_db', methods=["GET"])
def get_texts_by_user_id_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']
            texts_by_user_id = quote_builder_db.get_texts_by_user_id(user_id)
            return jsonify(texts_by_user_id)
        
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
@app.route('/get_searched_texts_db/<search_str>', methods=["GET"])
def get_searched_texts_db(search_str):
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']
            searched_texts = quote_builder_db.get_searched_texts(search_str)
            return jsonify(searched_texts)

        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route('/delete_text_by_text_id_db', methods=["POST"])
def delete_text_by_text_id_db():
    try:
        if "user_info" in session:
            user_id = session['user_info']['user_id']

            if request.method == "POST":
                data = request.get_json()
                text_id = data['text_id']
                quote_builder_db.delete_text_by_text_id(text_id, user_id)
                return jsonify({"deleted" : True})

        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#
# section name routes
@app.route('/get_all_section_names_db', methods=['GET'])
def get_all_section_names_db():
    try:
        if request.method == "GET":
            return jsonify(quote_builder_db.get_all_section_names())
        
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
@app.route('/save_new_section_name_to_db', methods=['POST'])
def save_new_section_name_to_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                new_section_name = data['new_section_name']
                
                if quote_builder_db.check_section_name_exists(new_section_name) == False:
                    quote_builder_db.insert_into_section_names_table(new_section_name)
                    # return the updated section name lists
                    return jsonify({"added": True, "all_section_names": quote_builder_db.get_all_section_names()})
                else:
                    # return empty section name lists
                    return jsonify({"added": False, "all_section_names": []})

        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#
# quote detials routes
@app.route('/save_quote_section_detials_db', methods=['POST'])
def save_quote_section_detials_db():
    try:
        if "user_info" in session: 
            if request.method == "POST":
                data_to_save = request.get_json()
                quote_name = data_to_save["quote_name"]
                res = quote_builder_db.save_section_data(data_to_save)
                quote_id = quote_builder_db.get_quote_id_by_quote_name(quote_name)
                quote_builder_db.update_quote_rev_date_and_time_stamp(quote_id)
                
                return jsonify({"saved": res})
        else:
            return render_template('login_error.html')

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
#----------------------------------------------------------------------------------------------#
# quote section  routes
@app.route('/get_quote_data_db/<quote_name>', methods=["GET"])
def get_quote_data_db(quote_name):
    try:
        quote_data = quote_builder_db.get_quote_data(quote_name)
        return jsonify(quote_data)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
# delete_selected_section_db
@app.route('/delete_selected_section_db', methods=['POST'])
def delete_selected_section_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                quote_name = data['quote_name']
                section_name = data['section_name']
                quote_id = quote_builder_db.get_quote_info_by_quote_name(quote_name)['quote_id']
                section_id = quote_builder_db.get_section_id_by_section_name(section_name)
                quote_builder_db.delete_seleceted_section_data(quote_id, section_id)

                return jsonify({"deleted": True})
        else:
            return render_template('login_error.html')
    
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
# Copy quote and its details,  delete quote

@app.route('/copy_quote_and_details', methods=['POST'])
def copy_quote():
    try:
        if 'user_info' in session:
            user_id = session['user_info']['user_id']
            
            if request.method == "POST":
                data = request.get_json()
                quote_id = data['quote_id']

                original_quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)

                # create a new quote info
                # first, create a new unique quote_name
                new_quote_name = f"{original_quote_info['quote_name']} _Copy"
                copy_count = 1
                while quote_builder_db.check_quote_name_exists(new_quote_name):
                    new_quote_name = f"{original_quote_info['quote_name']} _Copy({copy_count})"
                    copy_count += 1
                
                # insert new record
                date_quote_created = f"{helper.get_cur_datetime()['date_today']}"
                is_template = original_quote_info['is_template']
                customer_name = original_quote_info['customer_name']
                customer_email = original_quote_info['customer_email']
                customer_phone_no = original_quote_info['customer_phone_no']
                delivery_info = original_quote_info['delivery_info']
                company_id = original_quote_info['company_id']
                
                quote_builder_db.insert_into_quotes_table(new_quote_name, user_id, date_quote_created, customer_name, customer_email, customer_phone_no, delivery_info, is_template=is_template, 
                                                        company_id=company_id)
                # get info of copied quote and add quoted_by and quote_status
                copied_quote_info = quote_builder_db.get_quote_info_by_quote_name(new_quote_name)
                copied_quote_info['quoted_by'] = quote_builder_db.get_user_info_by_id(user_id)['full_name']
                copied_quote_info['quote_status'] = quote_builder_db.get_quote_status_name(copied_quote_info['quote_status_id'])

                # copy the quote details and section details of the original quote
                original_quote_data = quote_builder_db.get_quote_data(original_quote_info['quote_name'])
                quote_builder_db.copy_quote_details_to_new_quote(original_quote_data, copied_quote_info['quote_id'] )
                return jsonify({"data": copied_quote_info})
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
@app.route('/delete_quote', methods=["POST"])
def delete_quote():
    try:   
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                quote_id= int(data['quote_id'])
                print(data)
                quote_builder_db.delete_quote_and_its_data(quote_id)
                return jsonify({"deleted": True})
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#

# eze oreder excel text routes
@app.route('/save_eo_excel_file_text_to_db', methods=['POST'])
def save_eo_excel_file_text_to_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                eo_excel_obj = request.files['uploadedFile']
                user_id = request.form['user_id']
                eo_excel_name = secure_filename(eo_excel_obj.filename)
                eo_excel_save_location = f"static/excel_files/{eo_excel_name}"

                # remove the file from saved folder if it already exists and save the new file
                if os.path.exists(eo_excel_save_location):
                    os.remove(eo_excel_save_location)
                eo_excel_obj.save(eo_excel_save_location)

                processed_data = eo_excel_manager.prepare_and_process_excel_data_using_pandas(eo_excel_save_location)

                if processed_data['data_processed'] == True :
                    if quote_builder_db.check_eo_excel_name_exists_by_user_id(eo_excel_name,user_id):
                        eo_excel_in_db_id = quote_builder_db.get_eo_excel_by_eo_excel_name_and_user_id(eo_excel_name, user_id)['id']
                        quote_builder_db.delete_eo_excel_by_name_and_user_id(eo_excel_name, user_id)
                        quote_builder_db.delete_eo_excel_text_by_id(eo_excel_in_db_id)
                        
                    quote_builder_db.insert_into_eo_excel_table(eo_excel_name, eo_excel_save_location,int(user_id))
                    quote_builder_db.delete_old_eo_excel(int(user_id))

                    # Enter data into eo_excel_text_table
                    last_added_eo_excel = quote_builder_db.get_eo_excel_by_eo_excel_name_and_user_id(eo_excel_name, int(user_id))
                    eo_excel_id = last_added_eo_excel['id']
                    eo_excel_texts = processed_data['data']

                    for text in eo_excel_texts:
                        quote_builder_db.insert_into_eo_excel_text_table(eo_excel_id, text)

                    return jsonify({"uploaded": True , "message": 'File uploaded!'})   
                else:
                    os.remove(eo_excel_save_location)
                    return jsonify({"uploaded": False, "message": processed_data['message'] })
        else:
            return render_template('login_error.html')
        
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
@app.route('/get_searched_eo_excel_texts_db/<user_id>/<search_str>', methods=["GET"])
def get_searched_eo_excel_texts_db(user_id, search_str):
    searched_texts = []
    eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)
    if eo_excel_by_user_id :
        eo_excel_id = eo_excel_by_user_id[0]['id']
        searched_texts = quote_builder_db.get_searched_eo_excel_text_by_eo_excel_id(eo_excel_id, search_str)
    
    return jsonify(searched_texts)


@app.route('/get_all_eo_texts_of_current_user_db/<user_id>', methods=["GET"])
def get_all_eo_texts_of_current_user_db(user_id):
    try:
        eo_texts = []
        eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)
        if eo_excel_by_user_id :
            eo_excel_id = eo_excel_by_user_id[0]['id']
            eo_texts = quote_builder_db.get_eo_excel_text_by_eo_excel_id(eo_excel_id)
        
        return jsonify(eo_texts)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
# view quote
@app.route('/view_quote/<quote_name>', methods=["GET"])
def view_quote(quote_name):
    try:
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quoted_by_info = quote_builder_db.get_user_info_by_id(quote_info['user_id'])
        quote_data = quote_builder_db.get_quote_data(quote_name)
        
        company_id = quote_info['company_id']
        company_info = company_info_manager.get_company_info_by_id(company_id)
        
        # print("Loading View Quote Page")

        return render_template('view_quote.html',quote_info=quote_info, quote_data=quote_data, company_info=company_info, quoted_by_info=quoted_by_info, page_name='view_quote' )
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
        
@app.route('/add_new_rev_date_db', methods=["POST"])
def add_new_rev_date_db():
    try:
        if 'user_info' in session:
            new_rev_date = helper.get_cur_datetime()['date_today']

            if request.method == "POST":
                quote_id = request.form['quote_id']
                revision_dates = quote_builder_db.get_quote_info_by_quote_id(quote_id)['revision_dates']

                if revision_dates:
                    new_revision_dates = f"{revision_dates}|{new_rev_date}"
                else:
                    new_revision_dates = new_rev_date
                quote_builder_db.update_quote_revision_dates(quote_id, new_revision_dates)
                updated_quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)
                # rev_count = len(new_revision_dates.split('|'))

                # return jsonify({"new_rev_date": new_rev_date, "rev_count" : rev_count})
                return jsonify(updated_quote_info)
        
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        
@app.route('/update_joinery_supply_type_db', methods=["POST"])
def update_joinery_supply_type_db():
    try:
        if 'user_info' in session:
            if request.method == "POST":
                joinery_supply_type = request.form['joinery_supply_type']
                quote_id = request.form['quote_id']
                quote_builder_db.update_joinery_supply_type(quote_id,joinery_supply_type)

                return jsonify({'updated':True})
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
# update quote status
@app.route('/update_quote_status/<quote_id>', methods=["GET", "POST"])
def update_quote_status(quote_id):
    try:
        if 'user_info' in session:
            quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)
            quote_info['quote_status'] = quote_builder_db.get_quote_status_name(quote_info['quote_status_id'])
            all_quote_status = quote_builder_db.get_all_quote_status()

            if request.method == "POST":
                quote_id = request.form['quote_id']
                quote_status = request.form['quote_status']
                quote_status_id = quote_builder_db.get_quote_status_id(quote_status) if quote_builder_db.get_quote_status_id(quote_status) else 0 
                quote_builder_db.update_quote_status_by_quote_id(quote_id, quote_status_id) 
                return jsonify({'updated':True})

            if request.method == "GET":
                return render_template('update_quote_status.html', all_quote_status=all_quote_status , quote_info = quote_info)
            
            
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
# add new user, modify user
@app.route('/add_user', methods=["GET", 'POST'])
def add_user():
    try:
        if 'user_info' in session:
            all_user_types = quote_builder_db.get_all_user_types()

            if request.method == 'POST' :
                new_user_info = {
                    'user_name' : request.form['user_name'].strip().lower(),
                    'full_name' : request.form['full_name'].strip().title(),
                    'email_id' : request.form['email_id'].strip(),
                    'mobile_no' : request.form['mobile_no'].strip(),
                    'phone_no' : request.form['phone_no'].strip(),
                    'user_type' : request.form['user_type'],
                    'user_password' : request.form['user_password'].strip(),
                    'retyped_password' : request.form['retyped_password'].strip()
                }

                if quote_builder_db.get_user_info_by_user_name(new_user_info['user_name']):
                    flash((f"The username '{new_user_info['user_name']}' is already taken.' "))
                    flash("Please type in a new user name.")
                    new_user_info['user_name'] = ''
                    return render_template('add_user.html', page_name = "add_user" , all_user_types = all_user_types, new_user_info = new_user_info)
                else:
                    if new_user_info['user_password'] == new_user_info['retyped_password']:
                        user_type_id = quote_builder_db.get_user_type_id(new_user_info['user_type'])
                        quote_builder_db.insert_into_user_table(new_user_info['user_name'], new_user_info['full_name'], new_user_info['email_id'], new_user_info['user_password'], new_user_info['mobile_no'], new_user_info['phone_no'], user_type_id)
                        flash(f"Successfully added new user {new_user_info['user_name']}")
                        return render_template('add_user.html', page_name = "add_user" , user_added = True)
                    else:
                        flash("Passwords don't match!")
                        flash("Please fill the password fields again.")
                        return render_template('add_user.html', page_name = "add_user" , all_user_types = all_user_types, new_user_info = new_user_info)
                    
            if request.method == 'GET' :
                return render_template('add_user.html', page_name = "add_user" , all_user_types = all_user_types)

        else:
            return render_template('login_error.html')

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')

@app.route('/edit_user/<user_id>', methods=["GET", 'POST'])
def edit_user(user_id):
    try:
        if 'user_info' in session:

            all_user_types = quote_builder_db.get_all_user_types()

            if request.method == 'POST' :
                new_user_info = {
                    'user_id' : user_id,
                    'user_name' : request.form['user_name'].strip().lower(),
                    'full_name' : request.form['full_name'].strip().title(),
                    'email_id' : request.form['email_id'].strip(),
                    'mobile_no' : request.form['mobile_no'].strip(),
                    'phone_no' : request.form['phone_no'].strip(),
                    'user_type' : request.form['user_type'] if "user_type" in request.form else '',
                    'user_type_id' : quote_builder_db.get_user_type_id(request.form['user_type']) if "user_type" in request.form else None,
                    'user_password' : request.form['user_password'].strip(),
                    'retyped_password' : request.form['retyped_password'].strip()
                }

                user_info = quote_builder_db.get_user_info_by_id(user_id)

                if (user_info['user_name'] == new_user_info['user_name']) or (quote_builder_db.check_user_name_exists(new_user_info['user_name']) == False ) :
                    if new_user_info['user_password'] == new_user_info['retyped_password']:
                        quote_builder_db.update_user_info_by_user_id(new_user_info)
                        # now update the session['user_info']
                        if 'user_info' in session:
                            session.pop('user_info')
                        session['user_info'] = quote_builder_db.get_user_info_by_id(user_id)
                        flash(f"Successfully updated user profile!")
                        return render_template("edit_user.html",user_updated = True)
                    else:
                        flash("Passwords don't match!")
                        flash("Please fill in the password fields again.")
                        return render_template("edit_user.html", new_user_info = new_user_info, all_user_types = all_user_types)
                
                else:
                    flash((f"The username '{new_user_info['user_name']}' is already taken.' "))
                    flash("Please type in a new user name.")
                    # new_user_info['user_name'] = ''
                    return render_template("edit_user.html", new_user_info = new_user_info, all_user_types = all_user_types)
            
            if request.method == 'GET' :
                user_info = quote_builder_db.get_user_info_by_id(user_id)
                return render_template("edit_user.html", user_info = user_info, all_user_types = all_user_types)
            
        else:
            return render_template('login_error.html')
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)            # For Testing
        # serve(app,host='0.0.0.0', port=5001, threads=10)          # For Deployment
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
#----------------------------------------------------------------------------------------------#

# IMPORTANT
# Before deploying
#   1. Change server to deployment server  
#   2. In db_manager.py, make sure QUOTING_DB_PATH is file_folder_paths.LIVE_QUOTING_DB_PATH.
#   3. Make sure to copy over the uploads folder in static/images/ from the live copy into static/images/ of this new copy.  