from flask import render_template, request, session, jsonify
import inspect

from extensions import app
import quote_builder_db_manager as quote_builder_db


@app.route("/save_texts_to_db", methods=["POST"])
def save_texts_to_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]

            if request.method == "POST":
                data = request.get_json()
                text = data["text"].strip()
                if quote_builder_db.check_text_exists(text) == False:
                    quote_builder_db.insert_into_texts_table(text, user_id)
                    return jsonify({"saved": True})
                else:
                    return jsonify({"saved": False})
        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/get_texts_by_user_id_db", methods=["GET"])
def get_texts_by_user_id_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]
            texts_by_user_id = quote_builder_db.get_texts_by_user_id(user_id)
            return jsonify(texts_by_user_id)

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/get_searched_texts_db/<search_str>/<filter_searched_texts_by_current_user>", methods=["GET"])
def get_searched_texts_db(search_str, filter_searched_texts_by_current_user):
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]
            searched_texts = quote_builder_db.get_searched_texts(search_str, user_id) if filter_searched_texts_by_current_user == "true" else quote_builder_db.get_searched_texts(search_str)
            return jsonify(searched_texts)

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/delete_text_by_text_id_db", methods=["POST"])
def delete_text_by_text_id_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]

            if request.method == "POST":
                data = request.get_json()
                text_id = data["text_id"]
                quote_builder_db.delete_text_by_text_id(text_id, user_id)
                return jsonify({"deleted": True})

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
