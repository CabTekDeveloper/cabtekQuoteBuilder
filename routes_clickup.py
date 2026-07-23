from flask import jsonify
import inspect

from extensions import app
import manager_quote_builder_db as quote_builder_db
import helper


@app.route("/get_all_clickup_clients_db", methods=["GET"])
def get_all_clickup_clients_db():
    try:
        data = quote_builder_db.get_all_clickup_clients()
        return jsonify(data)
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')


@app.route("/sync_clickup_clients_table", methods=["POST"])
def sync_clickup_clients_table():
    try:

        init_elapsed_sec = helper.get_clickup_clients_table_sync_elapsed_seconds()
        cooldown_limit = 120

        # Stop user from smashing the sync process
        if init_elapsed_sec < cooldown_limit:
            wait_time = cooldown_limit - init_elapsed_sec
            return jsonify({"success": False, "message": f"Please wait for {wait_time} seconds before manually syncing again."})

        # Perform sync process if time elapsed is more than cool down period
        quote_builder_db.init_clickup_clients_table()

        return jsonify({"success": True, "message": "Local client data successfully synchronized with ClickUp!"})

    except Exception as ex:
        print(f"Manual sync endpoint encountered an error: {ex}")
        return jsonify({"success": False, "message": "An internal error occurred during synchronization."})
