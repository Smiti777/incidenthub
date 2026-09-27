from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os
from database import init_db

app = Flask(__name__)
init_db()

# GET COMMIT ID FROM RENDER (passed by deploy hook)
COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]


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
        incidents=incidents,
        commit=COMMIT
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


@app.route("/health")
def health():
    """Health check endpoint for CI/CD pipeline"""
    return jsonify({"status": "ok", "commit": COMMIT})


@app.route("/api/incidents")
def api_incidents():
    """JSON API endpoint returning incidents as JSON"""
    conn = sqlite3.connect("incidenthub.db")
    incidents = conn.execute(
        "SELECT id, title, service, severity, status FROM incidents ORDER BY id DESC"
    ).fetchall()
    conn.close()
    
    return jsonify({
        "incidents": [
            {
                "id": inc[0],
                "title": inc[1],
                "service": inc[2],
                "severity": inc[3],
                "status": inc[4]
            }
            for inc in incidents
        ]
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)