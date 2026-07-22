from flask import render_template, redirect, request, flash, session, url_for
import inspect

from extensions import app
import quote_builder_db_manager as quote_builder_db


@app.route("/", methods=["POST", "GET"])
def login():
    try:
        if "user_info" in session:
            session.pop("user_info")

        if request.method == "POST":
            user_name = request.form.get("user_name")
            user_password = request.form.get("user_password")
            user_info = quote_builder_db.get_user_info_by_user_name(user_name)

            if user_info and user_info["user_password"] == user_password:
                session["user_info"] = user_info

                # Wangchuk, 18-03-2025,
                quote_builder_db.backup_db(user_info["user_name"])

                return redirect(url_for("index"))
            else:
                flash("The username or password you entered is incorrect.")
                return render_template("login.html")

        if request.method == "GET":
            return render_template("login.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/logout")
def logout():
    try:
        if "user_info" in session:
            session.pop("user_info")

        flash("You are logged out.")
        return redirect(url_for("login"))

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
