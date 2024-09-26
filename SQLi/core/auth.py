from .data import *

BANNED_KEYWORDS = ["SELECT", "UNION", "OR", "AND", "AS", "ORDER", "BY", "WHERE", "FROM"]

def sanitize_inpt(to_sanitize: str) -> str:
    for keyword in BANNED_KEYWORDS:
        to_sanitize = to_sanitize.replace(keyword, "").replace(keyword.lower(), "")
    return to_sanitize.replace(" ", "")

def check_login(staff_id: str, password: str, _safety: str) -> bool:
    connection = connect_db()
    cursor = connection.cursor()
    if _safety != "none":
        staff_id = sanitize_inpt(staff_id)
        password = sanitize_inpt(password)    
    
    try:
        query = f"SELECT username, type, data FROM accounts WHERE (staffID = '{staff_id}') AND (password = '{password}')"
        print(query)
        cursor.execute(query)
    except sqlite3.OperationalError:
        return (False, [])
    results = cursor.fetchall()
    print(results)
    return (True, results[0]) if results else (False, [])
