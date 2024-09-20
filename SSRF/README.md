# SSRF Vulnerability
This is a web app with a vulnerability related to SSRF. There is 1 flag to find.

# How to run
1. Make sure you have python installed and install requirements by running ```pip install -r requirements.txt```
2. Open 2 terminals/cmd prompts as there are 2 scripts to run at the same time
3. Run ```python3 app.py``` in 1 terminal and ```python3 admin.py``` in the other terminal
4. You can now view the website at 127.0.0.1:5000
5. Do not directly view 127.0.0.1:8080, you must find a way to view 127.0.0.1:8080 from 127.0.0.1:5000