from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class AddTextToFile:

    def __init__(self):
        print("Custom String")

    def add_new_text_to_string(self):
        file_packet = StringIO.StringIO()
        graphics = canvas.Canvas(file_packet,pagesize=letter)
        graphics.drawString(10, 100, "Test String")
        graphics.save()

        file_packet.seek(0);
        new_pdf_file = PdfFileReader(file_packet)
        existing_pdf_file = PdfFileReader(file("/users/deepak.babu/Downloads/Sample_pdf.pdf", "rb"))
        append_text = PdfFileWriter()
        page = existing_pdf_file.getPage(0)
        page.mergePage(new_pdf_file.getPage(0))
        append_text.addPage(page)

        output_stream = file("/users/deepak.babu/Downloads/Sample_pdf.pdf", "wb")
        append_text.write(output_stream)
        output_stream.close()
        print("Successfully modified")

