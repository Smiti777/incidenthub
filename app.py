from flask import Flask, render_template, request, redirect
import sqlite3
from database import init_db

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("incidenthub.db")

    total = conn.execute(
        "SELECT COUNT(*) FROM incidents"
    ).fetchone()[0]

    open_count = conn.execute(
        "SELECT COUNT(*) FROM incidents WHERE status = 'Open'"
    ).fetchone()[0]

    investigating = conn.execute(
        "SELECT COUNT(*) FROM incidents WHERE status = 'Investigating'"
    ).fetchone()[0]

    resolved = conn.execute(
        "SELECT COUNT(*) FROM incidents WHERE status = 'Resolved'"
    ).fetchone()[0]

    incidents = conn.execute(
        "SELECT * FROM incidents ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        total=total,
        open_count=open_count,
        investigating=investigating,
        resolved=resolved,
        incidents=incidents
    )


@app.route("/create", methods=["GET", "POST"])
def create_incident():

    if request.method == "POST":
        title = request.form["title"]
        service = request.form["service"]
        severity = request.form["severity"]
        description = request.form["description"]
        assigned_to = request.form["assigned_to"]

        conn = sqlite3.connect("incidenthub.db")

        conn.execute("""
            INSERT INTO incidents
            (title, service, severity, description, assigned_to)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            service,
            severity,
            description,
            assigned_to
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("create_incident.html")

@app.route("/update/<int:incident_id>", methods=["POST"])
def update_incident(incident_id):
    status = request.form["status"]
    resolution = request.form.get("resolution", "")

    conn = sqlite3.connect("incidenthub.db")

    conn.execute(
        """
        UPDATE incidents
        SET status = ?, resolution = ?
        WHERE id = ?
        """,
        (status, resolution, incident_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")
    status = request.form["status"]

    conn = sqlite3.connect("incidenthub.db")

    conn.execute(
        "UPDATE incidents SET status = ? WHERE id = ?",
        (status, incident_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)