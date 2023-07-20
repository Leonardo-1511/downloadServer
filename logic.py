import json
from flask import redirect
import requests as rq
import time
import os

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