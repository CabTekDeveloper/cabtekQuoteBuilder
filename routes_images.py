from flask import render_template, request, session, jsonify
from werkzeug.utils import secure_filename
import os
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db


@app.route("/save_image_info_to_db", methods=["POST"])
def save_image_info_to_db():
    if "user_info" in session:
        if request.method == "POST":
            image_tag_name = request.form["image_tag_name"]
            image_tag_id = quote_builder_db.get_image_tag_id_by_tag_name(image_tag_name)
            img_obj = request.files["uploadedFile"]
            img_name = secure_filename(img_obj.filename)

            # If you look at the path below, you will see that static has been removed. This is done so that we can add this to img src in html files
            img_path = f"images/uploads/{img_name}"

            img_save_location = f"static/images/uploads/{img_name}"
            # Before saving the image file, make sure it does not exists already in the images/uploads folder or in the database
            # We have to make sure images stored in images/uploads folder have unique name.
            if (os.path.exists(img_save_location) == False) and (quote_builder_db.check_image_name_exists(img_name, image_tag_id) == False):
                img_obj.save(img_save_location)
                quote_builder_db.insert_into_images_table(img_name, img_path, image_tag_id)

                return jsonify({"uploaded": True})
            else:
                return jsonify({"uploaded": False})
    else:
        return render_template("login_error.html")


@app.route("/get_all_images_db/<image_tag_id>", methods=["GET"])
@app.route("/get_all_images_db", methods=["GET"])
def get_all_images_db(image_tag_id=None):
    try:
        if image_tag_id == None:
            all_images = quote_builder_db.get_all_images()
        else:
            all_images = quote_builder_db.get_all_images_by_tag_id(image_tag_id)

        return jsonify(all_images)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/get_searched_images_db/<search_str>", methods=["GET"])
def get_searched_images_db(search_str):
    try:
        searched_images = quote_builder_db.get_searched_images(search_str)
        return jsonify(searched_images)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/delete_image_by_id_db", methods=["POST"])
def delete_image_by_id_db():
    try:
        if "user_info" in session:

            if request.method == "POST":
                data = request.get_json()
                image_id = data["image_id"]

                image_info = quote_builder_db.get_image_info_by_image_id(image_id)
                img_save_location = f"static/{image_info['image_path']}" if image_info else ""
                if os.path.exists(img_save_location):
                    os.remove(img_save_location)

                if quote_builder_db.delete_image_by_image_id(image_id):
                    return jsonify({"deleted": True})
                else:
                    return jsonify({"deleted": False})
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/get_all_section_image_size_db", methods=["GET"])
def get_all_section_image_size_db():
    try:
        all_section_image_size = quote_builder_db.get_all_section_image_size()
        return jsonify(all_section_image_size)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
