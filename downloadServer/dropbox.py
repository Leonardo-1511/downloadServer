from . import app
import os
import json
import time
import requests as rq
from flask import request, send_file, redirect

@app.route("/")
def root():
    return json.dumps({'status': "development"}) + "<a href=/auth>auth</a>"


@app.route("/files/<file>")
def files(file):
    try:
        return send_file(f"downloadables/{file}", as_attachment=True)
    except FileNotFoundError:
        return json.dumps({"errorMsg": "File was not Found"})


@app.route("/dropbox/<path:path>")
def dropbox_download(path):
    file = None
    path = "/"+path
    with open("history.json", "r") as history:
        file = json.loads(history.read())
    try:
        print("pass try")
        if file[path] and file[path][1] >= int(time.time()):
            return redirect(file[path][0])
        else:
            raise ValueError
    except (KeyError, ValueError):
        dict = {"path": path}
        headers = {"Authorization": f"Bearer {os.environ['dropbox_api']}", "Content-Type": "application/json"}
        request = rq.request("post", "https://api.dropboxapi.com/2/files/get_temporary_link/", headers=headers, data=json.dumps(dict))
        
        file = None
        try:
            with open("history.json", "r") as historyR:
                file = json.loads(historyR.read())
                file.update({request.json()["metadata"]["path_display"]: [request.json()["link"], int(time.time())+14400]})
        except KeyError:
            return json.dumps({"error": "File does not Exist or token is Invalid"})
            
        with open("history.json", "w") as historyW:
            historyW.write(json.dumps(file))
        link = request.json()["link"]

        return redirect(link)


@app.route("/auth")
def authorize_url():
    html = '''
    <script src="https://replit.com/public/js/repl-auth-v2.js"></script>
    
<button onclick="LoginWithReplit()"> Login </button>
    '''
    return html


@app.route("/test")
def webhook_dropbox():
    replitUserId = request.headers.get("X-Replit-User-Id")
    return replitUserId
