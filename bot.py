import sys
import os
from flask import Flask, render_template, request
import aiml
from autocorrect import Speller

if sys.platform.startswith('darwin'):
    from AppKit import NSSpeechSynthesizer # Sintetizador de voz para MacOS
        
    synthesizer = NSSpeechSynthesizer.alloc().init()
    synthesizer.setRate_(90) # Velocidad por defecto del sintetizador
elif sys.platform.startswith('win') or sys.platform.startswith('linux'):
    import pyttsx3 # Sintetizador de voz para Windows y Linux

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'spanish')


app = Flask(__name__)

BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
k = aiml.Kernel()

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
    
    if sys.platform.startswith('darwin'):
        synthesizer.setRate_(velocidad)
    elif sys.platform.startswith('win') or sys.platform.startswith('linux'):
        # Mapear la velocidad a los valores admitidos por pyttsx3
        if velocidad == 60:
            velocidadPyttsx3 = 100  # Configuración de velocidad mínima en pyttsx3
        elif velocidad == 90:
            velocidadPyttsx3 = 200  # Configuración de velocidad predeterminada en pyttsx3
        elif velocidad == 100:
            velocidadPyttsx3 = 300
        elif velocidad == 150:
            velocidadPyttsx3 = 400

        engine.setProperty('rate', velocidadPyttsx3)

    print(velocidad)
    return {"status": "ok"}

@app.route("/get")
def get_bot_response():
    pr = Speller(lang='es')
    query = request.args.get('msg')
    query= pr(query)
    print(query)
    response = k.respond(query)
    if response:
        
        if sys.platform.startswith('darwin'):
            synthesizer.startSpeakingString_(response)
        elif sys.platform.startswith('win') or sys.platform.startswith('linux'):
            engine.say(str(response))
            engine.runAndWait()
        
        return (str(response))
    else:
        response = "Hola! En el menor tiempo posible nos comunicaremos  contigo y resolveremos todas tus inquietudes. También puedes encontrar la información que necesitas en nuestra página web www.parquedelcafe.co"
        
        if sys.platform.startswith('darwin'):
            synthesizer.startSpeakingString_(response)
        elif sys.platform.startswith('win') or sys.platform.startswith('linux'):
            engine.say(str(response))
            engine.runAndWait()
        return (str(response))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port='5001')


