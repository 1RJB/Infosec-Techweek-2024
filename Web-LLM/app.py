from flask import Flask, render_template, request, send_file
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        prompt = request.form.get('prompt')
        file = request.files['file'] 
        file.save('input')
        
        command = requests.post("https://gemini.haydenhow.com/send_message", data=prompt).json()['command']
        os.system(command)
        with open("static/output/command.txt", 'w') as f:
            f.write(command)

        return render_template('index.html', transformed=True)

    return render_template("index.html")

@app.route('/output/<file>')
def output(file):
    return send_file('static/output/' + file)

if __name__ == "__main__":
    app.run(debug=True)