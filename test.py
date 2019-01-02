from flask import Flask

app=Flask(__name__)
@app.route("/",methods=["GET"])
def test():
    return "hello"
from werkzeug.serving import run_simple
run_simple("localhost",5000,app)