"""
Compliance Audit System - Master Execution Pipeline
Initializes the database, parses policies with NLP, loads evidence,
maps embeddings via SentenceTransformers, and launches the web portal.
"""

import os
import sys

# Ensure backend directory is in path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from database import init_db
from policy_parser import parse_policy
from evidence_loader import load_evidence
from mapper import map_evidence
from report_generator import generate_pdf


def run():
    print("🚀 Initializing Compliance Audit Database...")
    init_db()

    policy_file = os.path.abspath(os.path.join("..", "sample_data", "policy_documents.txt"))
    evidence_file = os.path.abspath(os.path.join("..", "sample_data", "evidence_artifacts.csv"))

    if os.path.exists(policy_file):
        print(f"📖 Parsing security policy documents from {policy_file}...")
        parse_policy(policy_file)
    else:
        print("⚠️ Policy documents file not found.")

    if os.path.exists(evidence_file):
        print(f"📥 Loading collected evidence artifacts from {evidence_file}...")
        load_evidence(evidence_file)
    else:
        print("⚠️ Evidence artifacts file not found.")

    print("🧠 Running SentenceTransformer semantic vector mapping...")
    try:
        map_evidence()
    except Exception as e:
        print(f"Note: Vector mapping skipped ({e}). Proceeding to report generation.")

    print("📄 Generating initial Compliance Audit PDF report...")
    try:
        generate_pdf()
    except Exception as e:
        print(f"Report generation note: {e}")

    print("\n✅ System pipeline ready! Starting Flask Web Portal on http://127.0.0.1:5000 ...")
    from app import app
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    run()
