from flask import render_template, request, session, jsonify
import inspect

from extensions import app
import quote_builder_db_manager as quote_builder_db


@app.route("/add_quote_details/<quote_name>", methods=["GET"])
@app.route("/add_quote_details/<quote_name>/<add_new_section>/<section_name>", methods=["GET"])
def add_quote_details(quote_name, section_name="none", add_new_section="no"):
    try:
        if "user_info" in session:
            selected_section_name = None
            user_id = session["user_info"]["user_id"]

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
            quote_info["quoted_by"] = quote_builder_db.get_user_info_by_id(user_id)["full_name"]

            eo_excel_text = []
            eo_excel_by_user_id = quote_builder_db.get_eo_excel_by_user_id(user_id)

            if eo_excel_by_user_id:
                eo_excel_id = eo_excel_by_user_id[0]["id"]
                eo_excel_text = quote_builder_db.get_eo_excel_text_by_eo_excel_id(eo_excel_id)

            # display the selected section name details
            if quote_name and section_name != "none":
                selected_section_name = section_name
                return render_template(
                    "add_quote_details.html",
                    all_images=all_images,
                    quote_info=quote_info,
                    texts_by_user_id=texts_by_user_id,
                    all_section_names=all_section_names,
                    quote_data=quote_data,
                    selected_section_name=selected_section_name,
                    page_name="add_quote_details",
                    eo_excel_text=eo_excel_text,
                    all_image_tags=all_image_tags,
                    all_section_image_size=all_section_image_size,
                    frequently_used_texts_by_user_id=frequently_used_texts_by_user_id,
                )

            # check if the user wants to add a new section and display add new section form accordingly
            if quote_name and add_new_section == "yes":
                return render_template(
                    "add_quote_details.html",
                    all_images=all_images,
                    quote_info=quote_info,
                    texts_by_user_id=texts_by_user_id,
                    all_section_names=all_section_names,
                    quote_data=quote_data,
                    page_name="add_quote_details",
                    eo_excel_text=eo_excel_text,
                    all_image_tags=all_image_tags,
                    frequently_used_texts_by_user_id=frequently_used_texts_by_user_id,
                )

            # if the user hasn't selected a section name nor intends to add a new section, we will display the first section of the quote if it has got one.
            if quote_name and section_name == "none" and add_new_section == "no":
                section_names = quote_data["section_names"]
                if section_names:
                    selected_section_name = section_names[0]
                    return render_template(
                        "add_quote_details.html",
                        all_images=all_images,
                        quote_info=quote_info,
                        texts_by_user_id=texts_by_user_id,
                        all_section_names=all_section_names,
                        quote_data=quote_data,
                        selected_section_name=selected_section_name,
                        page_name="add_quote_details",
                        eo_excel_text=eo_excel_text,
                        all_image_tags=all_image_tags,
                        all_section_image_size=all_section_image_size,
                        frequently_used_texts_by_user_id=frequently_used_texts_by_user_id,
                    )
                else:
                    return render_template(
                        "add_quote_details.html",
                        all_images=all_images,
                        quote_info=quote_info,
                        texts_by_user_id=texts_by_user_id,
                        all_section_names=all_section_names,
                        quote_data=quote_data,
                        page_name="add_quote_details",
                        eo_excel_text=eo_excel_text,
                        all_image_tags=all_image_tags,
                        frequently_used_texts_by_user_id=frequently_used_texts_by_user_id,
                    )

        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


# Reorder section names routes
# 09-02-2024
@app.route("/reorder_section_names_db", methods=["POST"])
def reorder_section_names_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                quote_name = data["quote_name"]
                ordered_section_names = data["ordered_section_names"]
                quote_id = quote_builder_db.get_quote_id_by_quote_name(quote_name)

                section_order_no = 0
                for section_name in ordered_section_names:
                    section_order_no += 1
                    section_name_id = quote_builder_db.get_section_id_by_section_name(section_name)
                    quote_builder_db.update_quote_section_order_no(quote_id, section_name_id, section_order_no)

                return jsonify({"reordered": True})

        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


# section name routes
@app.route("/get_all_section_names_db", methods=["GET"])
def get_all_section_names_db():
    try:
        if request.method == "GET":
            return jsonify(quote_builder_db.get_all_section_names())

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/save_new_section_name_to_db", methods=["POST"])
def save_new_section_name_to_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                new_section_name = data["new_section_name"]

                if quote_builder_db.check_section_name_exists(new_section_name) == False:
                    quote_builder_db.insert_into_section_names_table(new_section_name)
                    # return the updated section name lists
                    return jsonify({"added": True, "all_section_names": quote_builder_db.get_all_section_names()})
                else:
                    # return empty section name lists
                    return jsonify({"added": False, "all_section_names": []})

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


# quote detials routes
@app.route("/save_quote_section_detials_db", methods=["POST"])
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
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


# quote section  routes
@app.route("/get_quote_data_db/<quote_name>", methods=["GET"])
def get_quote_data_db(quote_name):
    try:
        quote_data = quote_builder_db.get_quote_data(quote_name)
        return jsonify(quote_data)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


# delete_selected_section_db
@app.route("/delete_selected_section_db", methods=["POST"])
def delete_selected_section_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                quote_name = data["quote_name"]
                section_name = data["section_name"]
                quote_id = quote_builder_db.get_quote_info_by_quote_name(quote_name)["quote_id"]
                section_id = quote_builder_db.get_section_id_by_section_name(section_name)
                quote_builder_db.delete_seleceted_section_data(quote_id, section_id)

                return jsonify({"deleted": True})
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
