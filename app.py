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
        question = r["results"][x]["question"].replace("&quot;", '"').replace("&#039;","'")
        correct = r["results"][x]["correct_answer"].replace("&quot;", '"').replace("&#039;","'")
        incorrect = r["results"][x]["incorrect_answers"]
        incorrect = list(map(lambda x: x.replace("&quot;", '"').replace("&#039;","'"), incorrect))
        hits = solver.answer(question, [correct] + incorrect)
        rec = solver.rec(question, hits)

        question = {
            "category": r["results"][x]["category"],
            "question": question,
            "correct": correct,
            "incorrect_one": incorrect[0],
            "incorrect_two": incorrect[1],
            "incorrect_three": incorrect[2],
            "hits": hits,
            "recommended": rec,
            "isCorrect": rec == 1
        }
        question_bank.append(question)

    correct_recs = 0
    for question in question_bank:
        if question["isCorrect"]:
            correct_recs += 1

    return render_template("trivia.html", question_bank = question_bank, correct_recs = correct_recs)
