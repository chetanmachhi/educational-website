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

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        try:
            # Get data from form (with basic validation)
            topic_id = request.form['topic_id']
            question = request.form['question']
            correct_answer = request.form['correct_answer']

            # Ensure required fields are filled
            if not topic_id or not question or not correct_answer:
                return "Topic, Question, and Correct Answer are required!", 400

            hint = request.form.get('hint')  # Optional
            explanation = request.form.get('explanation')  # Optional
            difficulty = request.form.get('difficulty')  # Optional

            options = [
                request.form['option_1'],
                request.form['option_2'],
                request.form['option_3'],
                request.form['option_4']
            ]

            # Ensure there are 4 options
            if len(options) != 4 or any(option == '' for option in options):
                return "All 4 options are required!", 400

            # Database insertion
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO questions (topic_id, question, correct_answer, hint, explanation, difficulty, date_time, modified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (topic_id, question, correct_answer, hint, explanation, difficulty, datetime.now(), datetime.now()))

            question_id = cursor.lastrowid

            # Insert options into the options table
            for option in options:
                cursor.execute("""
                    INSERT INTO options (question_id, option_text)
                    VALUES (?, ?)
                """, (question_id, option))

            conn.commit()

        except sqlite3.DatabaseError as e:
            # Catch and log database errors
            print(f"Database error occurred: {e}")
            return "An error occurred while interacting with the database.", 500

        except Exception as e:
            # Catch any other exceptions
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred.", 500

        finally:
            if conn:
                conn.close()

        return redirect(url_for('add_question'))  # Redirect after successful submission

    # If GET request, render the form for adding a question
    return render_template('que.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
