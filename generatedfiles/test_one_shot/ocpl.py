from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

questions = []

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct1 = request.form['correct1'] == 'True'
        correct2 = request.form['correct2'] == 'True'
        correct3 = request.form['correct3'] == 'True'
        correct4 = request.form['correct4'] == 'True'
        question = {
            'title': title,
            'description': description,
            'options': [option1, option2, option3, option4],
            'correct': [correct1, correct2, correct3, correct4]
        }
        questions.append(question)
        save_data()
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        questions.pop(id)
        save_data()
        return redirect(url_for('index'))
    else:
        return render_template('delete.html', id=id)

@app.route('/question/<int:id>')
def question(id):
    return render_template('question.html', question=questions[id])

@app.route('/answer', methods=['POST'])
def answer():
    id = request.form['id']
    correct = questions[int(id)]['correct']
    selected = [request.form[f'option{i}'] for i in range(1, 5)]
    result = []
    for i, option in enumerate(selected):
        if option == 'True':
            result.append(correct[i])
    return jsonify({'result': result})

def save_data():
    with open('questions.json', 'w') as file:
        json.dump(questions, file)

if __name__ == '__main__':
    load_data()
    app.run(debug=True)