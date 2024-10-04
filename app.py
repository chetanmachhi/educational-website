from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)

# Your existing routes
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


# Hardcoded questions for the quiz (can replace this with SQL later)
questions = {
    1: {
        "question": "Which is the capital of India?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi"
    },
    # Add more questions if needed
}

# New quiz route
@app.route("/quiz", methods=["GET"])
def quiz():
    return render_template("quiz.html", questions=questions)

# Check answer route (POST)
@app.route("/check-answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data['question_id']
    selected_answer = data['answer']

    # Get the correct answer from the hardcoded questions
    correct_answer = questions[question_id]['answer']
    result = {
        "correct": selected_answer == correct_answer,
        "correct_answer": correct_answer
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
