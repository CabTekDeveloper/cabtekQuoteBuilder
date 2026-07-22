# Wangchuk added
# Wangchuk modified 01-08-2025
# Wangchuk modifed 10-07-2026
# Wangchuk modifed 21-07-2026

import inspect
from waitress import serve

from extensions import app, socketio

# ----------------------------------------------------------------------------------------------#
# Route modules (each registers its routes on `app`/`socketio` as a side effect of import)

import routes_auth
import routes_index
import routes_users
import routes_clickup
import routes_quotes
import routes_quote_sections
import routes_view_quote
import routes_images
import routes_texts
import routes_frequently_used_texts
import routes_eo_excel
import routes_websocket

# ----------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5001, debug=True)  # For Testing
        # serve(app,host='0.0.0.0', port=5001, threads=10)          # For Deployment
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
# ----------------------------------------------------------------------------------------------#

# IMPORTANT
# Before deploying
#   1. Change server to deployment server
#   2. In db_manager.py, make sure QUOTING_DB_PATH is file_folder_paths.LIVE_QUOTING_DB_PATH.
#   3. Make sure to copy over the uploads folder in static/images/ from the live copy into static/images/ of this new copy.
