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

def results():
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

def rec(question, hits):
    negative_words = ["not", "no", "none", "never"]

    question = question.strip()
    if question[-1] == '?':
        question = question[:-1]
    wordList = question.lower().split()

    strip_negatives = list(filter(lambda s: s not in negative_words, wordList))

    if (len(strip_negatives) == len(wordList)):
        max_hits = max(hits)
        if hits.count(max_hits) == 1:
            for x in range(0,4):
                if hits[x] == max_hits:
                    return x+1
        else:
            return -1;
    # Not question
    else:
        min_hits = min(hits)
        if hits.count(min_hits) == 1:
            for x in range(0,4):
                if hits[x] == min_hits:
                    return x+1
        else:
            return -1;

def answer(question_str, options_list):
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
    print('Search Query:', ' '.join(googleWordList))
    return results()
