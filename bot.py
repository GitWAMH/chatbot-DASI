from flask import Flask, render_template, request
import os
import aiml
from autocorrect import Speller
#import pyfestival as p

app = Flask(__name__)

BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
k = aiml.Kernel()

#p.init()
##pyfestival.close()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    query = [Speller().autocorrect_word(w) for w in (query.split())]
    question = " ".join(query)
    response = k.respond(question)
    if response:
        os.system('echo "' + response + '" | festival --tts')
        return (str(response))
    else:
        return (str(":)"))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port='5000')


