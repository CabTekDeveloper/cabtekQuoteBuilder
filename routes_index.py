from flask import render_template, session
import inspect

from extensions import app
import quote_builder_db_manager as quote_builder_db


@app.route("/index")
@app.route("/index/<showSavedTemplate>")
def index(showSavedTemplate="no"):
    try:
        if "user_info" in session:
            current_user_id = session["user_info"]["user_id"]

            # get all quotes for the current user
            quotes_by_user_id = quote_builder_db.get_quotes_by_user_id(current_user_id)
            for i in range(len(quotes_by_user_id)):
                # find full_name using the user_id of each quote and append it to the record
                user_id = quotes_by_user_id[i]["user_id"]
                quotes_by_user_id[i]["quoted_by"] = quote_builder_db.get_user_info_by_id(user_id)["full_name"]

                # find quote_status using the quote_status_id of each quote and append it to the record
                quote_status_id = quotes_by_user_id[i]["quote_status_id"]
                quotes_by_user_id[i]["quote_status"] = quote_builder_db.get_quote_status_name(quote_status_id)

            # check if user has saved quotes (we are not looking for quotes saved as template)
            has_saved_quotes = True if any(row["is_template"] == "no" for row in quotes_by_user_id) else False
            has_saved_template_quotes = True if any(row["is_template"] == "yes" for row in quotes_by_user_id) else False
            # print("Loading Index Page")
            return render_template(
                "index.html", quotes_by_user_id=quotes_by_user_id, has_saved_quotes=has_saved_quotes, has_saved_template_quotes=has_saved_template_quotes, showSavedTemplate=showSavedTemplate
            )

        else:
            return render_template("login_error.html")

    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
