from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")
    
@app.route("/gujarati", methods=["GET"])
def gujarati():
    return render_template("gujarati.html")
    
@app.route("/english", methods=["GET"])
def english():
    return render_template("english.html")

@app.route("/maths", methods=["GET"])
def maths():
    return render_template("maths.html") 
