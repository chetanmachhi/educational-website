from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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








if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
