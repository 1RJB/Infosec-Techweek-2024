# CSRF Vulnerability
This is a web app with a vulnerability related to CSRF. There is 1 flag to find.
app.py is the insecure version and secure_app.py is the more secure version.
malicious_app.py is a malicious web server which will send the csrf attack.

# How to run
1. Make sure you have python installed and install requirements by running ```pip install -r requirements.txt```
2. Run ```python3 app.py``` and ```python3 malicious_app.py``` in another terminal
3. You can now view the website at 127.0.0.1:5000 and the malicious app is at 127.0.0.1:8080