from flask import Flask, render_template, request
import requests

app = Flask(__name__)

images = []

@app.route('/')
def gallery():
    return render_template('gallery.html', gallery=images)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        url = request.form.get("url")
        title = request.form.get("title")
        desc = request.form.get("desc")
        file_path = f'image-{str(len(images)+1)}'

        res = requests.get(url)
        with open("static/uploads/" + file_path, 'wb') as f:
            f.write(res.content)

        images.append((file_path, title, desc))

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(port=5000)