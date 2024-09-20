from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def gallery():
    return render_template('administrator.html')

if __name__ == "__main__":
    app.run(port=8080)