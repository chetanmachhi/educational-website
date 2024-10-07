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
#@app.route("//", methods=["GET"])
#def main():
#    return render_template("index.html")

#@app.route("/gujarati", methods=["GET"])
#def gujarati():
 #   return render_template("gujarati/index_gujarati.html")

#@app.route("/gujarati/samas", methods=["GET"])
#def samas():
#    return render_template("gujarati/samas/samas_index.html")

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

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('test2.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/quiz", methods=["GET"])
def quiz():
    page = int(request.args.get('page', 1))
    limit = 5
    offset = (page - 1) * limit

    conn = get_db_connection()
    questions = conn.execute('SELECT id, question, option1, option2, option3, answer FROM questions LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    total_questions = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    conn.close()

    return render_template("quiz.html", questions=questions, current_page=page, total_questions=total_questions)

# Check answer route (POST)
@app.route("/check-answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_answer = data.get('answer')

    if not question_id or not selected_answer:
        return jsonify({"error": "Invalid request"}), 400

    conn = get_db_connection()
    question = conn.execute('SELECT answer FROM questions WHERE id = ?', (question_id,)).fetchone()
    conn.close()

    if question is None:
        return jsonify({"error": "Question not found"}), 404

    correct_answer = question['answer']
    result = {
        "correct": selected_answer == correct_answer,
        "correct_answer": correct_answer
    }

    return jsonify(result)

@app.route("/<subject>/<topic>/<subtopic>/quiz", methods=["GET"])
@app.route("/<subject>/<topic>/quiz", methods=["GET"])
@app.route("/<subject>/quiz", methods=["GET"])
@app.route("/quiz", methods=["GET"])
def get_quiz(subject=None, topic=None, subtopic=None):
    page = int(request.args.get('page', 1))
    limit = 5
    offset = (page - 1) * limit

    conn = get_db_connection()
    print('subject:',subject,'topic:', topic,'subtopic:', subtopic)
    if subject is None:
        # Scenario 4: No subject, topic, or subtopic (show all questions)
        questions = conn.execute('''
            SELECT id, question, option1, option2, option3, answer 
            FROM questions 
            LIMIT ? OFFSET ?
        ''', (limit, offset)).fetchall()
        
        total_questions = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]

    elif topic is None:
        # Scenario 1: Only subject (show all questions for the subject)
        questions = conn.execute('''
            SELECT id, question, option1, option2, option3, answer 
            FROM questions 
            WHERE subject_id = (SELECT id FROM subjects WHERE subject_name = ?)
            LIMIT ? OFFSET ?
        ''', (subject, limit, offset)).fetchall()
        
        total_questions = conn.execute('SELECT COUNT(*) FROM questions WHERE subject_id = (SELECT id FROM subjects WHERE subject_name = ?) ', (subject,)).fetchone()[0]

    elif subtopic is None:
        # Scenario 2: Subject and topic (show questions for the topic)
        questions = conn.execute('''
            SELECT id, question, option1, option2, option3, answer 
            FROM questions 
            WHERE subject_id = (SELECT id FROM subjects WHERE LOWER(subject_name) = ?)
            AND topic_id = (SELECT id FROM topics WHERE LOWER(topic_name) = ?)
            LIMIT ? OFFSET ?
        ''', (subject, topic, limit, offset)).fetchall()
        
        total_questions = conn.execute('SELECT COUNT(*) FROM questions WHERE subject_id = (SELECT id FROM subjects WHERE LOWER(subject_name) = ?) AND topic_id = (SELECT id FROM topics WHERE LOWER(topic_name) = ?)', (subject, topic)).fetchone()[0]

    else:
        # Scenario 3: Subject, topic, and subtopic (show questions for the subtopic)
        questions = conn.execute('''
            SELECT id, question, option1, option2, option3, answer 
            FROM questions 
            WHERE subject_id = (SELECT id FROM subjects WHERE subject_name = ?)
            AND topic_id = (SELECT id FROM topics WHERE topic_name = ?)
            AND subtopic_id = (SELECT id FROM subtopics WHERE subtopic_name = ?)
            LIMIT ? OFFSET ?
        ''', (subject, topic, subtopic, limit, offset)).fetchall()

        total_questions = conn.execute('SELECT COUNT(*) FROM questions WHERE subject_id = (SELECT id FROM subjects WHERE subject_name = ?) AND topic_id = (SELECT id FROM topics WHERE topic_name = ?) AND subtopic_id = (SELECT id FROM subtopics WHERE subtopic_name = ?)', (subject, topic, subtopic)).fetchone()[0]

    conn.close()
    print('questions:', questions, 'current_page:', page, 'total_questions:', total_questions)

    return render_template("quiz.html", questions=questions, current_page=page, total_questions=total_questions)


#if __name__ == "__main__":
 #   app.run(debug=True, host="0.0.0.0", port=5000)











@app.route('/')
def index():

    subjects = ["Gujarati", "English", "Maths"]
    return render_template('index.html', header_title="MCQs Hell", subjects=subjects)


@app.route('/<subject>')
def subject_page(subject):

    topics = {
        "gujarati": ["Samas", "Alankar", "Chhand"],
        "english": ["Grammar", "Literature", "Comprehension"],
        "maths": ["Algebra", "Geometry", "Calculus"]
                }
    
    topic_list = topics.get(subject.lower(), [])
    return render_template('subject.html', 
                           title=f"{subject.capitalize()} Topics", 
                           header_title=f"{subject.capitalize()} MCQs", 
                           topics=topic_list, 
                           subject=subject.lower())

# Route for a topic page
@app.route('/<subject>/<topic>')
def topic_page(subject, topic):
    subtopics = {
        "samas": ["Subtopic1", "Subtopic2"],
        "alankar": ["Subtopic3", "Subtopic4"],
        "chhand": ["Subtopic5", "Subtopic6"]
    }
    
    # Check if the topic has subtopics
    subtopic_list = subtopics.get(topic.lower(), [])
    
    if subtopic_list:
        return render_template('topic.html', 
                               title=f"{topic.capitalize()} - {subject.capitalize()}", 
                               header_title=f"{topic.capitalize()} Subtopics", 
                               subtopics=subtopic_list,
                               subject=subject.lower(), 
                               topic=topic)
    else:
        learning_material = f"Learning material for {topic} in {subject}."
        return render_template('learning.html', 
                               title=f"{topic.capitalize()} - {subject.capitalize()}", 
                               header_title=f"Learning {topic.capitalize()}", 
                               content=learning_material, 
                               subject=subject.lower(), 
                               topic=topic)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
