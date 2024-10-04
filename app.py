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

@app.route("/alankar", methods=["GET"])
def alankar():
    return render_template("alankar.html")
    
@app.route("/learn-alankar", methods=["GET"])
def learn_alankar():
    return render_template("learn-alankar.html")

@app.route("/practice-alankar", methods=["GET"])
def practice_alankar():
    return render_template("practice-alankar.html") 








if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
