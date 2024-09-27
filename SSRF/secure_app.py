from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
import re

app = Flask(__name__)

images = []

def is_ipv4(url):
    # Checks if the url is a domain or an ip
    regex = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
    return re.fullmatch(regex, url)

# Can check in /etc/hosts or C:/Windows/System32/Drivers/etc/hosts for internal dns and domain names to blacklist
BLACK_LIST = {'localhost', 'someotherdomain', 'someotherdomain2'}

@app.route('/')
def gallery():
    return render_template('gallery.html', gallery=images)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        url = request.form.get("url")
        title = request.form.get("title")
        desc = request.form.get("desc")

        # Validating URL
        parsed_url = urlparse(url)
        if is_ipv4(parsed_url.hostname):
            return render_template('upload.html', invalid=True)

        if parsed_url.hostname in BLACK_LIST:
            return render_template('upload.html', invalid=True)

        file_path = f'image-{str(len(images)+1)}'

        res = requests.get(url)
        with open("static/uploads/" + file_path, 'wb') as f:
            f.write(res.content)

        images.append((file_path, title, desc))

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(port=5000)