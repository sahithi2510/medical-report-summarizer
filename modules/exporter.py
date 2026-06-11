import io

from fpdf import FPDF


def export_pdf(summary):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.multi_cell(
        0,
        10,
        summary
    )

    pdf_bytes = pdf.output(
        dest="S"
    )

    return io.BytesIO(
        pdf_bytes.encode("latin1")
    )


def export_txt(summary):

    return io.BytesIO(
        summary.encode("utf-8")
    )