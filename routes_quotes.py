from flask import render_template, request, session, jsonify
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db
import manager_company_info as company_info_manager
import delivery_types as delivery_types
import helper


@app.route("/get_quote_info_db/<quote_name>", methods=["GET"])
def get_quote_info_db(quote_name):
    try:
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quote_info["quoted_by"] = quote_builder_db.get_user_info_by_id(quote_info["user_id"])["full_name"]
        return jsonify(quote_info)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/check_quote_name_exists_db/<quote_name>")
def check_quote_name_exists_db(quote_name):
    exists = quote_builder_db.check_quote_name_exists(quote_name)
    return jsonify({"exists": exists})


@app.route("/get_quotes_by_user_id_db/<user_id>", methods=["GET"])
def get_quotes_by_user_id_db(user_id):
    try:
        quotes_by_user_id = quote_builder_db.get_quotes_by_user_id(user_id)
        return jsonify(quotes_by_user_id)

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/create_quote", methods=["GET"])
def create_quote():
    try:
        if "user_info" in session:

            # Sync clickup clients table with local db if 2 hour has elapsed since last sync
            if helper.get_clickup_clients_table_sync_elapsed_seconds() > 7200:
                quote_builder_db.init_clickup_clients_table()

            all_company_info = company_info_manager.get_all_company_info()
            all_clients = quote_builder_db.get_all_clickup_clients()
            all_delivery_types = delivery_types.get_all_delivery_types()
            return render_template("quote_form.html", all_company_info=all_company_info, all_clients=all_clients, all_delivery_types=all_delivery_types)
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/create_quote/create_new_quote", methods=["POST"])
def create_new_quote():
    try:
        date_today = f"{helper.get_cur_datetime()['date_today']}"
        data = request.get_json()
        user_id = quote_builder_db.get_user_info_by_full_name(data["quoted_by"])["user_id"]

        quote_builder_db.insert_into_quotes_table(
            data["quote_name"],
            user_id,
            date_today,
            data["customer_name"],
            data["customer_email"],
            data["customer_phone_no"],
            data["delivery_info"],
            data["is_template"],
            data["company_id"],
            data["is_trade_client"],
            data["customer_company"],
            data["delivery_type"],
            data["ship_via"],
        )

        return jsonify({"success": True})
    except Exception as e:
        print(f"Database error during quote edit save: {e}")
        return jsonify({"success": False, "message": "Internal database error occurred while saving."}), 500


@app.route("/edit_quote/<quote_id>")
def edit_quote(quote_id):
    try:
        if "user_info" in session:

            # Sync clickup clients table with local db if 2 hour has elapsed since last sync
            if helper.get_clickup_clients_table_sync_elapsed_seconds() > 7200:
                quote_builder_db.init_clickup_clients_table()

            all_company_info = company_info_manager.get_all_company_info()
            all_clients = quote_builder_db.get_all_clickup_clients()
            all_delivery_types = delivery_types.get_all_delivery_types()

            quote_info = quote_builder_db.get_quote_info_by_quote_id(quote_id)
            quote_info["quoted_by"] = quote_builder_db.get_user_info_by_id(quote_info["user_id"])["full_name"]

            return render_template("quote_form.html", quote_info=quote_info, all_company_info=all_company_info, all_clients=all_clients, all_delivery_types=all_delivery_types)
        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/edit_quote/save_edited_quote", methods=["POST"])
def save_edited_quote():
    try:
        data = request.get_json()
        quote_builder_db.update_quote_info_by_quote_id(data)
        return jsonify({"success": True})
    except Exception as e:
        print(f"Database error during quote edit save: {e}")

        return jsonify({"success": False, "message": "Internal database error occurred while saving."}), 500


@app.route("/copy_quote_and_details", methods=["POST"])
def copy_quote():
    try:
        if "user_info" in session:
            user_id = session["user_info"]["user_id"]

            if request.method == "POST":
                data = request.get_json()
                quote_id = data["quote_id"]

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
                is_template = original_quote_info["is_template"]
                customer_name = original_quote_info["customer_name"]
                customer_email = original_quote_info["customer_email"]
                customer_phone_no = original_quote_info["customer_phone_no"]
                delivery_info = original_quote_info["delivery_info"]
                company_id = original_quote_info["company_id"]
                customer_company = original_quote_info["customer_company"]
                is_trade_client = original_quote_info["is_trade_client"]
                delivery_type = original_quote_info["delivery_type"]
                ship_via = original_quote_info["ship_via"]

                quote_builder_db.insert_into_quotes_table(
                    new_quote_name,
                    user_id,
                    date_quote_created,
                    customer_name,
                    customer_email,
                    customer_phone_no,
                    delivery_info,
                    is_template=is_template,
                    company_id=company_id,
                    customer_company=customer_company,
                    is_trade_client=is_trade_client,
                    delivery_type=delivery_type,
                    ship_via=ship_via,
                )

                # # get info of copied quote and add quoted_by and quote_status
                # copied_quote_info = quote_builder_db.get_quote_info_by_quote_name(new_quote_name)
                # copied_quote_info["quoted_by"] = quote_builder_db.get_user_info_by_id(user_id)["full_name"]
                # copied_quote_info["quote_status"] = quote_builder_db.get_quote_status_name(copied_quote_info["quote_status_id"])

                # # copy the quote details and section details of the original quote
                # original_quote_data = quote_builder_db.get_quote_data(original_quote_info["quote_name"])
                # quote_builder_db.copy_quote_details_to_new_quote(original_quote_data, copied_quote_info["quote_id"])
                return jsonify({"success": True})
        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return jsonify({"success": True})



@app.route("/delete_quote", methods=["POST"])
def delete_quote():
    try:
        if "user_info" in session:
            if request.method == "POST":
                data = request.get_json()
                quote_id = int(data["quote_id"])

                quote_builder_db.delete_quote_and_its_data(quote_id)
                return jsonify({"success": True})
        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
        return jsonify({"success": False})



@app.route("/set_quote_is_locked_db", methods=["POST"])
def set_quote_is_locked_db():
    try:
        if "user_info" not in session:
            return render_template("login_error.html")
        
        data = request.get_json()
        quote_name = data.get("quote_name")
        is_locked = data.get("is_locked")

        # Get the quote_id based on the quote_name
        quote_id = quote_builder_db.get_quote_id_by_quote_name(quote_name)

        # Update the quote's locked status in the database
        quote_builder_db.update_is_locked(quote_id, is_locked)

        # Return a success response
        return jsonify({"success": True})
    except Exception as e:
        print(f"Database error during quote edit save: {e}")
        return jsonify({"success": False}), 500