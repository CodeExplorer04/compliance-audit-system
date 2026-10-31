mapper.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database import get_connection

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def map_evidence():

    conn = get_connection()
    cur = conn.cursor()

    requirements = cur.execute(
        "SELECT * FROM requirements"
    ).fetchall()

    evidence = cur.execute(
        "SELECT * FROM evidence"
    ).fetchall()

    for req in requirements:

        req_embedding = model.encode(
            req["requirement_text"]
        )

        for ev in evidence:

            ev_embedding = model.encode(
                ev["description"]
            )

            score = cosine_similarity(
                [req_embedding],
                [ev_embedding]
            )[0][0]

            if score > 0.75:

                cur.execute("""
                INSERT INTO mappings
                (
                    requirement_id,
                    evidence_id,
                    similarity_score
                )
                VALUES(?,?,?)
                """,
                (
                    req["requirement_id"],
                    ev["evidence_id"],
                    float(score)
                ))

    conn.commit()
    conn.close()

    print("Evidence Mapping Complete")
    