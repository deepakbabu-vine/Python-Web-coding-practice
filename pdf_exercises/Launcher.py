import PyPDF2
import re
import textract

from AddTextToFile import AddTextToFile


def read_pdf_file():
    """
    Reads the entire pdf file line by line
    """
    with open("/users/deepak.babu/Downloads/Sample_pdf.pdf", "rb") as targetPDFFile:
        pdfreader = PyPDF2.PdfFileReader(targetPDFFile, strict=False)
        pages = pdfreader.numPages
        index = 1
        while index < pages:
            pageobj = pdfreader.getPage(index)
            print(pageobj.extractText())
            print("Page No.", index)
            print("-----------------")
            index = index + 1


def word_count():
    """
    Returns the number of words in the pdf file
    :return: Number of words in the pdf file
    """
    content = textract.process("/users/deepak.babu/Downloads/Sample_pdf.pdf")
    words = re.findall(r"[^\W_]+", content, re.MULTILINE)
    return len(words)


read_pdf_file()
print("Words Count", word_count())

addTextToPdf = AddTextToFile()
addTextToPdf.add_new_text_to_string()
