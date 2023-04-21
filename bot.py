from flask import Flask, render_template, request
import os
import aiml
from autocorrect import Speller
from AppKit import NSSpeechSynthesizer #Habilitar para MAC
#import pyttsx3  //Habilitar para OS Windows
#from bs4 import BeautifulSoup 

app = Flask(__name__)

BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
k = aiml.Kernel()

synthesizer = NSSpeechSynthesizer.alloc().init()
synthesizer.setRate_(90)

'''
html = '<p>Hola! Soy CoffeeBot, tu asistente virtual del Parque Del Café. Estoy aquí para darte una mano y resolver las dudas que puedas tener!</p>'
soup = BeautifulSoup(html, 'html.parser')
texto = soup.get_text()
'''
#engine = pyttsx3.init()
'''
engine.setProperty('voice', 'spanish')
engine.say(texto)
'''
#engine.setProperty('voice', 'spanish')

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


@app.route("/actualizar_velocidad", methods=["POST"])
def actualizar_velocidad():
    data = request.get_json()
    velocidad = int(data["velocidad"])
    synthesizer.setRate_(velocidad)
    print(velocidad)
    return {"status": "ok"}

@app.route("/get")
def get_bot_response():
    pr = Speller(lang='es')
    query = request.args.get('msg')
    query= pr(query)
    #query = [Speller().autocorrect_word(w) for w in (query.split())]
    print(query)
    response = k.respond(query)
    if response:
        synthesizer.startSpeakingString_(response)
        #os.system('echo "' + response + '" | festival --tts')
        #engine.say(response)
        #engine.runAndWait()
        
        return (str(response))
    else:
        response = "Hola! En el menor tiempo posible nos comunicaremos  contigo y resolveremos todas tus inquietudes. También puedes encontrar la información que necesitas en nuestra página web www.parquedelcafe.co"
        #engine.say(str(response))
        #engine.runAndWait()
        return (str(response))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port='5001')


