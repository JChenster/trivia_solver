import requests
from bs4 import BeautifulSoup
import random
import time

punc = '"?!.:;/'
fileIn = open('ignore.txt', 'r')
ignoreList = fileIn.read().lower().split()
fileIn.close()

def processQuestion(question, conjunction='+'):
    question = question.strip()
    if question[-1] == '?':
        question = question[:-1]
    wordList = question.lower().split()

    global googleWordList
    googleWordList = list(filter(lambda s: s not in ignoreList, wordList))

    googleSearchLink = conjunction.join(googleWordList)
    return googleSearchLink

def search(question):
    req = requests.get('https://www.google.com/search?q=' + processQuestion(question))
    processPage(req)

def processPage(req):
    soup = BeautifulSoup(req.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    global allText
    allText = allText + '\n\n\n' + text

def answer():
    wordList = allText.lower().split()
    wordList = list(map(lambda s: s.strip(punc), wordList))
    hits = []
    for option in options:
        counter = 0
        if not(option == str(option)):
            for optionWord in option:
                count = wordList.count(optionWord.lower())
                counter += count
        else:
            counter = wordList.count(option.lower())
        hits.append(counter)
    return hits

def main(question_str, options_list):
    global allText
    allText = ''

    global question
    question = question_str
    global options
    options = list(map(lambda s: s.lower().split(), options_list))
    ans = []
    for wordList in options:
        ans.append(list(filter(lambda s: s not in ignoreList, wordList)))
    options = ans

    search(question)
    print('Searching:', ' '.join(googleWordList))
    return answer()
