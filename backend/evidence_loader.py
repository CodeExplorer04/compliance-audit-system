import pandas as pd
from database import get_connection


def load_evidence(csv_file):

    df = pd.read_csv(csv_file)

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():

        cur.execute("""
        INSERT INTO evidence
        (
            evidence_id,
            requirement_id,
            description,
            confidence_score,
            verification_status,
            timestamp
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            row.get("evidence_id"),
            row.get("requirement_id"),
            row.get("description"),
            row.get("confidence_score", 0.8),
            row.get("verification_status", "verified"),
            row.get("timestamp")
        ))

    conn.commit()
    conn.close()

    print("Evidence Loaded Successfully")