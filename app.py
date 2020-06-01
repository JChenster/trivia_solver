from flask import Flask, render_template
import requests
import solver

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    url = "https://opentdb.com/api.php?amount=12&type=multiple"
    r = requests.get(url).json()

    question_bank = []

    for x in range(0,12):
        question = r["results"][x]["question"]
        correct = r["results"][x]["correct_answer"]
        incorrect = r["results"][x]["incorrect_answers"]
        hits = solver.main(question, [correct] + incorrect)
        
        question = {
            "category": r["results"][x]["category"],
            "question": question,
            "correct": correct,
            "incorrect_one": incorrect[0],
            "incorrect_two": incorrect[1],
            "incorrect_three": incorrect[2],
            "hits": hits,
            "isCorrect": hits[0] > hits[1] and hits[0] > hits[2] and hits[0] > hits[3]
        }
        question_bank.append(question)

    return render_template("trivia.html", question_bank = question_bank)
