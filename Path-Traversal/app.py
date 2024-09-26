from flask import Flask, request, send_file, abort, render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_root', 'templates'))

# Base directory for the application
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # Path where app.py is located
FILES_DIRECTORY = os.path.join(BASE_DIRECTORY, 'web_root', 'files')  # Path to the files directory
BIN_DIRECTORY = os.path.join(BASE_DIRECTORY, 'bin')  # Path to the bin directory

@app.route('/')
def index():
    hint = "Current directory is /web_root/files "
    
    # Get list of files from the files directory
    files = os.listdir(FILES_DIRECTORY)
    
    return render_template('index.html', hint=hint, files=files)

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('file')
    
    if filename is None:
        abort(400, description="Missing 'file' parameter")

    # Allow access to files in the files directory
    if filename.startswith('..'):
        # Handle requests for files in the bin directory
        bin_file_path = os.path.abspath(os.path.join(BIN_DIRECTORY, filename))
        if os.path.exists(bin_file_path) and not os.path.isdir(bin_file_path):
            return send_file(bin_file_path)

    # Handle requests for files in the files directory
    file_path = os.path.abspath(os.path.join(FILES_DIRECTORY, filename))
    print(f"Requested file path: {file_path}")

    # Validate the file path to restrict access and ensure it's not a directory
    if file_path.startswith(FILES_DIRECTORY):
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return send_file(file_path)

    abort(404, description="File not found or access denied")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def access_denied(e):
    return render_template('access_denied.html'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
