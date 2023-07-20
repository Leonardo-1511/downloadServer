import downloadServer

if __name__ == "__main__":
    downloadServer.app.run("0.0.0.0", 8080, debug=True)