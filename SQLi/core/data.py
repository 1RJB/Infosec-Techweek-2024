from dotenv import load_dotenv
from pathlib import Path
from .config import DB_URL
import sqlite3
import re
import os

def connect_db() -> sqlite3.Connection:
    return sqlite3.connect(DB_URL)

def parse_query(query: str):
    # Compiles a set of expressions to be matched to
    expressions = {
        "name": re.compile(r"name:([^\s]+)"),
        "status": re.compile(r"status:([^\s]+)")
    }
    matches = {"name": [], "status": []}
    for key, value in expressions.items():
        matches[key] = value.findall(query)
        query = value.sub("", query).strip() # Removes all matched elements from the original query

    connection = connect_db()
    cursor = connection.cursor()
    sqlquery = "SELECT name, description, status FROM projects WHERE "
    params = []
    if matches["name"] or matches["status"]:
        if matches["name"]:
            sqlquery += "name LIKE ?"
            params.append("%" + matches["name"][0] + "%")
        if matches["status"]:
            if matches["name"]: query += " AND "
            sqlquery += "status = ?"
            params.append(matches["status"][0])
    else:
        sqlquery += " name LIKE ? OR description LIKE ?"
        params.extend(["%" + query + "%", "%" + query + "%"])
    sqlquery += " COLLATE NOCASE"
    cursor.execute(sqlquery, params)
    results = cursor.fetchall() 
    connection.close()
    return results
