from flask import render_template, request, session, jsonify
from werkzeug.utils import secure_filename
import os
import inspect

from extensions import app
import quote_builder_db_manager as quote_builder_db
import eo_excel_manager


# eze oreder excel text routes
@app.route("/save_eo_excel_file_text_to_db", methods=["POST"])
def save_eo_excel_file_text_to_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                eo_excel_obj = request.files["uploadedFile"]
                user_id = request.form["user_id"]
                eo_excel_name = secure_filename(eo_excel_obj.filename)
                eo_excel_save_location = f"static/excel_files/{eo_excel_name}"

                # remove the file from saved folder if it already exists and save the new file
                if os.path.exists(eo_excel_save_location):
                    os.remove(eo_excel_save_location)
                eo_excel_obj.save(eo_excel_save_location)

                processed_data = eo_excel_manager.prepare_and_process_excel_data_using_pandas(eo_excel_save_location)

                if processed_data["data_processed"] == True:
                    if quote_builder_db.check_eo_excel_name_exists_by_user_id(eo_excel_name, user_id):
                        eo_excel_in_db_id = quote_builder_db.get_eo_excel_by_eo_excel_name_and_user_id(eo_excel_name, user_id)["id"]
                        quote_builder_db.delete_eo_excel_by_name_and_user_id(eo_excel_name, user_id)
                        quote_builder_db.delete_eo_excel_text_by_id(eo_excel_in_db_id)

                    quote_builder_db.insert_into_eo_excel_table(eo_excel_name, eo_excel_save_location, int(user_id))
                    quote_builder_db.delete_old_eo_excel(int(user_id))

                    # Enter data into eo_excel_text_table
                    last_added_eo_excel = quote_builder_db.get_eo_excel_by_eo_excel_name_and_user_id(eo_excel_name, int(user_id))
                    eo_excel_id = last_added_eo_excel["id"]
                    eo_excel_texts = processed_data["data"]

                    for text in eo_excel_texts:
                        quote_builder_db.insert_into_eo_excel_text_table(eo_excel_id, text)

                    return jsonify({"uploaded": True, "message": "File uploaded!"})
                else:
                    os.remove(eo_excel_save_location)
                    return jsonify({"uploaded": False, "message": processed_data["message"]})
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/get_searched_eo_excel_texts_db/<user_id>/<search_str>", methods=["GET"])
def get_searched_eo_excel_texts_db(user_id, search_str):
    searched_texts = []
    eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)
    if eo_excel_by_user_id:
        eo_excel_id = eo_excel_by_user_id[0]["id"]
        searched_texts = quote_builder_db.get_searched_eo_excel_text_by_eo_excel_id(eo_excel_id, search_str)

    return jsonify(searched_texts)


@app.route("/get_all_eo_texts_of_current_user_db/<user_id>", methods=["GET"])
def get_all_eo_texts_of_current_user_db(user_id):
    try:
        eo_texts = []
        eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)
        if eo_excel_by_user_id:
            eo_excel_id = eo_excel_by_user_id[0]["id"]
            eo_texts = quote_builder_db.get_eo_excel_text_by_eo_excel_id(eo_excel_id)

        return jsonify(eo_texts)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
