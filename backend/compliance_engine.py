from datetime import datetime
from database import get_connection


def calculate_compliance():

    conn = get_connection()
    cur = conn.cursor()

    requirements = cur.execute(
        "SELECT * FROM requirements"
    ).fetchall()

    results = []

    compliant_count = 0

    for req in requirements:

        mapping = cur.execute("""
        SELECT *
        FROM mappings
        WHERE requirement_id=?
        """,
        (req["requirement_id"],)
        ).fetchone()

        if not mapping:

            status = "GAP"
            risk = "CRITICAL"

        else:

            ev = cur.execute("""
            SELECT *
            FROM evidence
            WHERE evidence_id=?
            """,
            (mapping["evidence_id"],)
            ).fetchone()

            status = "COMPLIANT"
            risk = "LOW"

            if ev:

                if ev["confidence_score"] < 0.70:
                    status = "LOW_CONFIDENCE"
                    risk = "HIGH"

                if (
                    ev["verification_status"]
                    == "rejected"
                ):
                    status = "NON_COMPLIANT"
                    risk = "CRITICAL"

            compliant_count += (
                status == "COMPLIANT"
            )

        results.append({
            "requirement_id":
                req["requirement_id"],
            "status":
                status,
            "risk":
                risk
        })

    total = len(requirements)

    score = (
        compliant_count / total * 100
        if total > 0 else 0
    )

    conn.close()

    return {
        "score": round(score, 2),
        "results": results
    }
