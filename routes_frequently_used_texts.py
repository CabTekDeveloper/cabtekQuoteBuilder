from flask import render_template, request, session, jsonify
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db


@app.route("/get_frequently_used_texts_by_user_id_db", methods=["GET"])
def get_frequently_used_texts_by_user_id_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]
            frequently_used_texts_by_user_id = quote_builder_db.get_frequently_used_texts_by_user_id(user_id)
            return jsonify(frequently_used_texts_by_user_id)
        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/add_text_to_frequently_used_table_db", methods=["POST"])
def add_text_to_frequently_used_table_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]
            if request.method == "POST":
                data = request.get_json()
                text = data["text"]

                if quote_builder_db.check_frequently_used_text_exists(user_id, text):
                    quote_builder_db.update_frequently_used_text_count(user_id, text)
                else:
                    quote_builder_db.insert_into_frequently_used_text_table(user_id, text)

                return jsonify({"saved": True})
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/delete_frequently_used_text_db", methods=["POST"])
def delete_frequently_used_text_db():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]

            if request.method == "POST":
                data = request.get_json()
                text_id = data["text_id"]
                quote_builder_db.delete_frequently_used_text(text_id)
                return jsonify({"deleted": True})

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
