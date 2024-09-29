from flask import Flask, render_template, request, make_response, redirect, jsonify
import json
import secrets

app = Flask(__name__)

def get_roles(username, token):
    # Returns None if invalid cookies
    with open("users.json", "r") as f:
        users = json.load(f)['users']

    for user in users:
        if user['username'] == username and user['token'] == token:
            return user['roles']

    return None

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    username = request.cookies.get("username")
    token = request.cookies.get("auth")
    roles = get_roles(username, token)
    if roles == None:
        return redirect("/login")

    with open("workspaces.json", "r") as f:
        workspaces = json.load(f)['workspaces']

    my_workspaces = []
    for workspace in workspaces:
        if username in workspace['users']:
            my_workspaces.append(workspace['title'])

    return render_template('dashboard.html', superadmin='super' in roles, admin='admin' in roles, workspaces=my_workspaces)

@app.route("/create_workspace", methods=['POST', 'GET'])
def create_workspace():
    username = request.cookies.get("username")
    token = request.cookies.get("auth")
    roles = get_roles(username, token)
    if roles == None:
        return redirect("/login")

    if request.method == "POST":
        print("shuh", request.data)
        data = request.get_json()
        print("ss", data)
        title = data['title']
        users = data['users']
        with open("workspaces.json", "r") as f:
            workspaces = json.load(f)

        with open("users.json", "r") as f:
            users_db = json.load(f)

        for user in users:
            valid_user = False
            for temp in users_db['users']:
                if temp['username'] == user:
                    valid_user = True

            if not valid_user:
                return jsonify({"success": "false", "msg": "Invalid user"}), 400

        workspaces['workspaces'].append({
            'title': title,
            'users': users
        })

        with open("workspaces.json", "w") as f:
            json.dump(workspaces, f, indent=4)
        
        return jsonify({"success": "true"}), 200

    return render_template('create_workspace.html')

@app.route("/api/modify_role/<username>/<role>")
def modify_role(username, role):
    if role not in {'admin', 'super'}:
        return '', 400

    if role == "super":
        # Add in authentication to only allow certain ppl to make ppl superadmin
        # For example, only allow superadmins to modify role to superadmin
        pass
    
    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users['users']:
        if user['username'] == username and role not in user['roles']:
            user['roles'].append(role)

            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)

            return '', 200

    return '', 200

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        with open("users.json", "r") as f:
            users = json.load(f)['users']

        for user in users:
            if user['username'] == username and user['password'] == password:
                resp = make_response(redirect('/dashboard'))
                resp.set_cookie('username', user['username'])
                resp.set_cookie('auth', user['token'])
                return resp

        return render_template('login.html', invalid=True)

    return render_template('login.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with open("users.json", "r") as f:
            users = json.load(f)

        token = secrets.token_urlsafe(32)

        for user in users['users']:
            if user['username'] == username:
                return render_template('signup.html', invalid=True)

        users['users'].append({
            'username': username,
            'password': password,
            'token': token,
            'roles': []
        })

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('username', username)
        resp.set_cookie('auth', token)
        return resp

    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)