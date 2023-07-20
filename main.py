from flask import Flask, send_file, request, redirect
import json
import time
import logic
import requests as rq
import os

app = Flask("app")


@app.before_request()
def before_request():
    return

@app.route("/")
def root():
    return json.dumps({'status': "development"}) + "<a href=/auth>auth</a>"


@app.route("/files/<file>")
def files(file):
    auth = request.args.get("auth")
    if auth != os.environ["auth"]:
        return json.dumps({"errorMsg": "user not auhtorized"})
    try:
        return send_file(f"downloadables/{file}", as_attachment=True)
    except FileNotFoundError:
        return json.dumps({"errorMsg": "File was not Found"})


@app.route("/dropbox/<path:path>")
def drp(path):
    return logic.dropbox_download(path)


@app.route("/auth")
def authorize_url():
    html = '''
    <script src="https://replit.com/public/js/repl-auth-v2.js"></script>
    
<button onclick="LoginWithReplit()"> Login </button>
    '''
    return html


@app.route("/webhook/dropbox")
def webhook_dropbox():
    return

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)