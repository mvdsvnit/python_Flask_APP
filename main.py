from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer)

class QuizApp:
    def __init__(self):
        self.questions = [
            {
                'question': 'What is the capital of France?',
                'options': ['Berlin', 'Madrid', 'Paris', 'Rome'],
                'correct_answer': 'Paris'
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
                'correct_answer': 'Mars'
            },
            {
                'question': 'Who wrote "Romeo and Juliet"?',
                'options': ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'],
                'correct_answer': 'William Shakespeare'
            },
            # Add more questions as needed
        ]
        self.current_question = 0
        self.score = 0

quiz_app = QuizApp()

# This should be created within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    global enrollment_number
    enrollment_number = request.form['enrollment_number']
    name = request.form['name']
    semester = request.form['semester']

    user = User.query.filter_by(enrollment_number=enrollment_number).first()
    if not user:
        user = User(enrollment_number=enrollment_number, name=name, semester=semester, score=0)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global enrollment_number
    if request.method == 'POST':
        user_answer = request.form['answer']
        check_answer(user_answer)

    if quiz_app.current_question < len(quiz_app.questions):
        question = quiz_app.questions[quiz_app.current_question]
        return render_template('quiz.html', question=question)
    else:
        user = User.query.filter_by(enrollment_number=enrollment_number).first()
        user.score = quiz_app.score
        db.session.commit()

        result_message = f"Name: {user.name}\nEnrollment Number: {user.enrollment_number}\nSemester: {user.semester}\n\nYou scored {quiz_app.score} out of {len(quiz_app.questions)}"
        return render_template('result.html', result_message=result_message)

def check_answer(user_answer):
    global enrollment_number
    correct_answer = quiz_app.questions[quiz_app.current_question]['correct_answer']
    if user_answer == correct_answer:
        quiz_app.score += 1

    quiz_app.current_question += 1

@app.route('/view_database')
def view_database():
    users = User.query.all()
    return render_template('view_database.html', users=users)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
