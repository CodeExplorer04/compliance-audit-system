import os
from flask import Flask, jsonify, render_template, send_file, request
from flask_cors import CORS

from database import init_db
from compliance_engine import calculate_compliance
from report_generator import generate_pdf

app = Flask(__name__)
CORS(app)

# Initialize database schema if not present
init_db()


@app.route("/")
def home():
    # If client accepts HTML, render dashboard; else return API status
    if request.accept_mimetypes.accept_html:
        return render_template("index.html")
    return jsonify({
        "message": "Compliance Audit System API",
        "status": "online",
        "endpoints": ["/score", "/requirements", "/evidence", "/download-report"]
    })


@app.route("/api/status")
def api_status():
    return jsonify({
        "message": "Compliance Audit System API",
        "version": "1.0.0"
    })


@app.route("/score")
def score():
    return jsonify(calculate_compliance())


@app.route("/requirements")
def requirements():
    from database import get_connection
    conn = get_connection()
    rows = conn.execute("SELECT * FROM requirements").fetchall()
    conn.close()
    return jsonify([dict(x) for x in rows])


@app.route("/evidence")
def evidence():
    from database import get_connection
    conn = get_connection()
    rows = conn.execute("SELECT * FROM evidence").fetchall()
    conn.close()
    return jsonify([dict(x) for x in rows])


@app.route("/download-report")
def download_report():
    # Generate fresh PDF scorecard
    generate_pdf()
    pdf_path = os.path.join(os.path.dirname(__file__), "Compliance_Report.pdf")
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name="Enterprise_Compliance_Audit_Report.pdf")
    return jsonify({"error": "Report generation failed"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
