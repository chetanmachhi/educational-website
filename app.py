from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('data.db')  # Connect to your SQLite database
    conn.row_factory = sqlite3.Row  # Allows for accessing columns by name
    return conn

# Your existing routes
@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/gujarati", methods=["GET"])
def gujarati():
    return render_template("gujarati.html")

@app.route("/samas", methods=["GET"])
def samas():
    return render_template("samas.html")

@app.route("/dvand-samas", methods=["GET"])
def dvand_samas():
    return render_template("dvand-samas.html")

@app.route("/learn-dvand-samas", methods=["GET"])
def learn_dvand_samas():
    return render_template("learn-dvand-samas.html")

@app.route("/practice-dvand-samas", methods=["GET"])
def practice_dvand_samas():
    return render_template("practice-dvand-samas.html")

# New quiz route
@app.route("/quiz", methods=["GET"])
def quiz():
    return render_template("quiz.html")  # Ensure you have a 'quiz.html' file

# Check answer route (POST)
@app.route("/check-answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data['question_id']
    selected_answer = data['answer']

    # Assume you have some hardcoded questions for the quiz
    correct_answer = "some_correct_answer"  # Update this with your logic
    result = {
        "correct": selected_answer == correct_answer,
        "correct_answer": correct_answer
    }

    return jsonify(result)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    # Connect to the database and retrieve subjects, topics, and subtopics first
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Retrieve subjects
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    # Retrieve topics
    cursor.execute("SELECT id, topic_name FROM topics GROUP BY id")
    topics = cursor.fetchall()

    # Retrieve subtopics
    cursor.execute("SELECT id, MAX(subtopic_name) AS subtopic_name FROM subtopics GROUP BY id")
    subtopics = cursor.fetchall()

    conn.close()
    
    # Handle POST request for adding a question
    if request.method == 'POST':
        # Now you get the subject ID, topic ID, and subtopic ID directly from the form
        subject_id = request.form['subject']
        topic_id = request.form['topic']
        subtopic_id = request.form['subtopic']
        question = request.form['question']
        answer = request.form['correct_answer']
        option1 = request.form['option_a']
        option2 = request.form['option_b']
        option3 = request.form['option_c']
        hints = request.form.get('hint')  
        explanation = request.form.get('solution')  

        # Insert the question into the database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO questions (subject_id, topic_id, subtopic_id, question, answer, option1, option2, option3, hints, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (subject_id, topic_id, subtopic_id, question, answer, option1, option2, option3, hints, explanation))
        
        conn.commit()
        conn.close()

        return redirect(url_for('add_question'))  # Redirect to the same route after adding the question

    # For GET request, render the form with subjects, topics, and subtopics
    return render_template('que.html', subjects=subjects, topics=topics, subtopics=subtopics)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
