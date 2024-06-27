from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# JSON file to store questions and answers
QUESTIONS_FILE = 'questions.json'

# Question class to store question details
class Question:
    def __init__(self, title, description, option1, option2, option3, option4, answer1, answer2, answer3, answer4):
        self.title = title
        self.description = description
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4

# Load questions from JSON file
def load_questions():
    with open(QUESTIONS_FILE, 'r') as f:
        data = json.load(f)
        questions = []
        for question in data['questions']:
            title = question['title']
            description = question['description']
            option1 = question['option1']
            option2 = question['option2']
            option3 = question['option3']
            option4 = question['option4']
            answer1 = question['answer1']
            answer2 = question['answer2']
            answer3 = question['answer3']
            answer4 = question['answer4']
            questions.append(Question(title, description, option1, option2, option3, option4, answer1, answer2, answer3, answer4))
        return questions

# Save questions to JSON file
def save_questions(questions):
    data = {}
    data['questions'] = []
    for question in questions:
        title = question.title
        description = question.description
        option1 = question.option1
        option2 = question.option2
        option3 = question.option3
        option4 = question.option4
        answer1 = question.answer1
        answer2 = question.answer2
        answer3 = question.answer3
        answer4 = question.answer4
        data['questions'].append({'title': title, 'description': description, 'option1': option1, 'option2': option2, 'option3': option3, 'option4': option4, 'answer1': answer1, 'answer2': answer2, 'answer3': answer3, 'answer4': answer4})
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(data, f)

# Add a new question
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer1 = request.form['answer1']
    answer2 = request.form['answer2']
    answer3 = request.form['answer3']
    answer4 = request.form['answer4']
    question = Question(title, description, option1, option2, option3, option4, answer1, answer2, answer3, answer4)
    questions = load_questions()
    questions.append(question)
    save_questions(questions)
    return render_template('index.html', questions=questions)

# Delete a question
@app.route('/delete/<int:question_id>', methods=['POST'])
def delete(question_id):
    questions = load_questions()
    for i, question in enumerate(questions):
        if question.title == question_id:
            del questions[i]
            break
    save_questions(questions)
    return render_template('index.html', questions=questions)

# Display a question
@app.route('/question/<int:question_id>')
def question(question_id):
    questions = load_questions()
    for question in questions:
        if question.title == question_id:
            return render_template('question.html', question=question)
    return 'Question not found'

# Display the main page
@app.route('/')
def index():
    questions = load_questions()
    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)