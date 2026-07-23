from flask import render_template, request, flash, session
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db


# add new user, modify user
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    try:
        if "user_info" in session:
            all_user_types = quote_builder_db.get_all_user_types()

            if request.method == "POST":
                new_user_info = {
                    "user_name": request.form["user_name"].strip().lower(),
                    "full_name": request.form["full_name"].strip().title(),
                    "email_id": request.form["email_id"].strip(),
                    "mobile_no": request.form["mobile_no"].strip(),
                    "phone_no": request.form["phone_no"].strip(),
                    "user_type": request.form["user_type"],
                    "user_password": request.form["user_password"].strip(),
                    "retyped_password": request.form["retyped_password"].strip(),
                }

                if quote_builder_db.get_user_info_by_user_name(new_user_info["user_name"]):
                    flash((f"The username '{new_user_info['user_name']}' is already taken.' "))
                    flash("Please type in a new user name.")
                    new_user_info["user_name"] = ""
                    return render_template("add_user.html", page_name="add_user", all_user_types=all_user_types, new_user_info=new_user_info)
                else:
                    if new_user_info["user_password"] == new_user_info["retyped_password"]:
                        user_type_id = quote_builder_db.get_user_type_id(new_user_info["user_type"])
                        quote_builder_db.insert_into_user_table(
                            new_user_info["user_name"],
                            new_user_info["full_name"],
                            new_user_info["email_id"],
                            new_user_info["user_password"],
                            new_user_info["mobile_no"],
                            new_user_info["phone_no"],
                            user_type_id,
                        )
                        flash(f"Successfully added new user {new_user_info['user_name']}")
                        return render_template("add_user.html", page_name="add_user", user_added=True)
                    else:
                        flash("Passwords don't match!")
                        flash("Please fill the password fields again.")
                        return render_template("add_user.html", page_name="add_user", all_user_types=all_user_types, new_user_info=new_user_info)

            if request.method == "GET":
                return render_template("add_user.html", page_name="add_user", all_user_types=all_user_types)

        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    try:
        if "user_info" in session:

            all_user_types = quote_builder_db.get_all_user_types()

            if request.method == "POST":
                new_user_info = {
                    "user_id": user_id,
                    "user_name": request.form["user_name"].strip().lower(),
                    "full_name": request.form["full_name"].strip().title(),
                    "email_id": request.form["email_id"].strip(),
                    "mobile_no": request.form["mobile_no"].strip(),
                    "phone_no": request.form["phone_no"].strip(),
                    "user_type": request.form["user_type"] if "user_type" in request.form else "",
                    "user_type_id": quote_builder_db.get_user_type_id(request.form["user_type"]) if "user_type" in request.form else None,
                    "user_password": request.form["user_password"].strip(),
                    "retyped_password": request.form["retyped_password"].strip(),
                }

                user_info = quote_builder_db.get_user_info_by_id(user_id)

                if (user_info["user_name"] == new_user_info["user_name"]) or (quote_builder_db.check_user_name_exists(new_user_info["user_name"]) == False):
                    if new_user_info["user_password"] == new_user_info["retyped_password"]:
                        quote_builder_db.update_user_info_by_user_id(new_user_info)
                        # now update the session['user_info']
                        if "user_info" in session:
                            session.pop("user_info")
                        session["user_info"] = quote_builder_db.get_user_info_by_id(user_id)
                        flash(f"Successfully updated user profile!")
                        return render_template("edit_user.html", user_updated=True)
                    else:
                        flash("Passwords don't match!")
                        flash("Please fill in the password fields again.")
                        return render_template("edit_user.html", new_user_info=new_user_info, all_user_types=all_user_types)

                else:
                    flash((f"The username '{new_user_info['user_name']}' is already taken.' "))
                    flash("Please type in a new user name.")
                    # new_user_info['user_name'] = ''
                    return render_template("edit_user.html", new_user_info=new_user_info, all_user_types=all_user_types)

            if request.method == "GET":
                user_info = quote_builder_db.get_user_info_by_id(user_id)
                return render_template("edit_user.html", user_info=user_info, all_user_types=all_user_types)

        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
