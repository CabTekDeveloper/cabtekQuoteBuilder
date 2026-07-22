from flask import render_template, request, session
from flask_socketio import emit
from datetime import datetime
import inspect

from extensions import app, socketio

# Web Socket
# To track the clients connected to the this web app

clients = {}  # We might have to store this in a json file. For now leave it here


@socketio.on("connect")
def on_connect():
    # # Store client info when they connect
    clients[request.sid] = {"ip_address": request.remote_addr}

    # # Store client info when they connect
    clients[request.sid] = {
        "client_name": session.get("user_info", {}).get("full_name", "Missing user name"),  # Flask sessions
        "ip_address": request.remote_addr,
        "page_url": request.referrer,
        "connected_at": datetime.now().strftime("%H:%M:%S"),
        "user_agent": request.headers.get("User-Agent"),
    }

    emit("update_client_list", clients, broadcast=True)


@socketio.on("disconnect")
def on_disconnect():
    # Remove client info when they disconnect
    if request.sid in clients:
        del clients[request.sid]

    emit("update_client_list", clients, broadcast=True)


# Display details of the connected clients.
@app.route("/active_connections", methods=["GET"])
def active_connections():
    try:
        return render_template("active_connections.html")
    except Exception as ex:
        print(f'Error:"{ex}" [In function {inspect.stack()[0][3]}]')
