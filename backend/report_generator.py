from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from compliance_engine import (
    calculate_compliance
)


def generate_pdf():

    report = calculate_compliance()

    doc = SimpleDocTemplate(
        "Compliance_Report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Compliance Audit Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Compliance Score: "
            f"{report['score']}%",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 20))

    for item in report["results"]:

        content.append(
            Paragraph(
                f"{item['requirement_id']} "
                f"- {item['status']} "
                f"({item['risk']})",
                styles["BodyText"]
            )
        )

    doc.build(content)

    print("PDF Generated")