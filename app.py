from flask import Flask, render_template
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    url = "https://opentdb.com/api.php?amount=12&type=multiple"
    r = requests.get(url).json()

    question_bank = []

    for x in range(0,12):
        question = {
            "category": r["results"][x]["category"],
            "question": r["results"][x]["question"],
            "correct": r["results"][x]["correct_answer"],
            "incorrect_one": r["results"][x]["incorrect_answers"][0],
            "incorrect_two": r["results"][x]["incorrect_answers"][1],
            "incorrect_three": r["results"][x]["incorrect_answers"][2]
        }
        question_bank.append(question)

    return render_template("trivia.html", question_bank = question_bank)
