from flask import Flask, render_template, redirect
import subprocess
import sys
import sqlite3
from flask import request

app = Flask(__name__)

@app.route("/search")
def search():

    query = request.args.get("q", "")

    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE subject LIKE ?
       OR summary LIKE ?
       OR body LIKE ?
    ORDER BY relevance DESC
    """,
    (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"
    ))

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "search.html",
        results=results,
        query=query
    )

@app.route("/refresh", methods=["POST"])
def refresh():

    subprocess.run([
        sys.executable,
        "main.py"
    ])

    return redirect("/")


@app.route("/email/<email_id>")
def email_detail(email_id):

    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE email_id = ?
    """, (email_id,))

    email = cursor.fetchone()

    conn.close()

    return render_template(
        "email.html",
        email=email
    )


@app.route("/")
def home():

    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE category='INTERNSHIP'
    ORDER BY relevance DESC
    """)
    internships = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE category='ACADEMIC'
    ORDER BY relevance DESC
    """)
    academics = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE category='EVENT'
    ORDER BY relevance DESC
    """)
    events = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM emails
    WHERE category='MESS'
    ORDER BY relevance DESC
    """)
    mess = cursor.fetchall()

    cursor.execute("""
SELECT subject,
       category,
       deadline,
       relevance
FROM emails
WHERE deadline != 'NONE'
  AND deadline != ''
ORDER BY relevance DESC
""")

    deadlines = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        internships=internships,
        academics=academics,
        events=events,
        mess=mess,
        deadlines=deadlines
    )


if __name__ == "__main__":
    app.run(debug=True)