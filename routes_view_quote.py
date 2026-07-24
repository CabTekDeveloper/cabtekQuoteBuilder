from flask import render_template, request, session, jsonify, send_from_directory
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db
import manager_company_info as company_info_manager
import manager_myob_data as myob_data_manager
import helper


@app.route("/view_quote/<quote_name>", methods=["GET"])
def view_quote(quote_name):
    try:
        quote_info = quote_builder_db.get_quote_info_by_quote_name(quote_name)
        quote_info["quoted_by"] = quote_builder_db.get_user_info_by_id(quote_info['user_id'])["full_name"]

        quoted_by_info = quote_builder_db.get_user_info_by_id(quote_info["user_id"])
        quote_data = quote_builder_db.get_quote_data(quote_name)

        company_id = quote_info["company_id"]
        company_info = company_info_manager.get_company_info_by_id(company_id)

        # print("Loading View Quote Page")
        return render_template("view_quote.html", quote_info=quote_info, quote_data=quote_data, company_info=company_info, quoted_by_info=quoted_by_info, page_name="view_quote")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/add_new_rev_date_db", methods=["POST"])
def add_new_rev_date_db():
    try:
        if "user_info" in session:
            new_rev_date = helper.get_cur_datetime()["date_today"]

            if request.method == "POST":
                quote_id = request.form["quote_id"]
                revision_dates = quote_builder_db.get_quote_info_by_quote_id(quote_id)["revision_dates"]

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
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/update_joinery_supply_type_db", methods=["POST"])
def update_joinery_supply_type_db():
    try:
        if "user_info" in session:
            if request.method == "POST":
                joinery_supply_type = request.form["joinery_supply_type"]
                quote_id = request.form["quote_id"]
                quote_builder_db.update_joinery_supply_type(quote_id, joinery_supply_type)

                return jsonify({"updated": True})
        else:
            return render_template("login_error.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/download_myob_file/<quote_name>", methods=["GET"])
def download_myob_file(quote_name):
    try:
        file_info = myob_data_manager.generate_myob_data_file(quote_name)

        if not file_info:
            return jsonify({"success": False}), 500

        return send_from_directory(file_info["folder_path"], file_info["file_name"], as_attachment=True, mimetype="text/plain")

    except Exception as ex:
        print(ex)
        return jsonify({"success": False}), 500
