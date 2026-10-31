import re
import spacy
from database import get_connection

nlp = spacy.load("en_core_web_sm")


def parse_policy(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    policy_blocks = text.split("---")

    conn = get_connection()
    cur = conn.cursor()

    for block in policy_blocks:

        policy_match = re.search(r"POLICY_ID:\s*(.*)", block)

        if not policy_match:
            continue

        policy_id = policy_match.group(1).strip()

        requirements = re.findall(
            r"REQUIREMENT\s*(\d+):(.*?)(?=REQUIREMENT|\Z)",
            block,
            re.S
        )

        for req_num, req_text in requirements:

            req_text = req_text.strip()

            evidence_match = re.search(
                r"Evidence Source:\s*(.*)",
                req_text
            )

            evidence_source = (
                evidence_match.group(1)
                if evidence_match
                else "Unknown"
            )

            cur.execute("""
            INSERT INTO requirements
            (
                policy_id,
                requirement_id,
                requirement_text,
                evidence_source
            )
            VALUES(?,?,?,?)
            """,
            (
                policy_id,
                f"{policy_id}-REQ-{req_num}",
                req_text,
                evidence_source
            ))

    conn.commit()
    conn.close()

    print("Policies Parsed Successfully")