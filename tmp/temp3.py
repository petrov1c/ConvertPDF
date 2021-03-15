from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from pathlib import Path

pdf = PdfFileReader("D:/Yjdz/doc06113320210311152437.pdf")

num_pages = pdf.getNumPages()
print('Количество страниц: ', num_pages)

ind = 0
for page in pdf.pages:
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(page)

    name_file = 'D:/Yjdz/pages/doc_' + str(ind) + '.pdf'
    with Path(name_file).open(mode="wb") as output_file:
        pdf_writer.write(output_file)

    ind = ind + 1