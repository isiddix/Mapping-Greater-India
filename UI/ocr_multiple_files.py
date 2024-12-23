# Script that runs OCRmyPDF on all PDFs in current directory

import ocrmypdf
import os

# Wrapper for OCRmyPDF program
def ocrmypdf_process(input, output):
    if __name__ == '__main__':  # To ensure correct behavior on Windows and macOS
        ocrmypdf.ocr(input, output, deskew=True, sidecar=True, force_ocr=True)
    else:
        ocrmypdf.ocr(input, output, sidecar=True, force_ocr=True)


def ocr_main(directory):

    os.chdir(directory)

# Grab the current directory
    dir_list = os.listdir()

# Iterate through the directory
    for i in dir_list:
        length = len(i)
        # Make sure file is a PDF
        if i[length - 4:] == '.pdf':
            #only scan if the file is not scanned
            if i[:length - 4] + 'OCR.pdf.txt' not in dir_list:
                output = i[:length - 4] + 'OCR.pdf'
                # Run OCR
                ocrmypdf_process(i, output)

# Cleanup
    if not os.path.exists('OCR PDFs'):
        os.mkdir('OCR PDFs')
    if not os.path.exists('Text Docs'):
        os.mkdir('Text Docs')

    dir_list = os.listdir()
    for i in dir_list:
        length = len(i)
        # Putting newly made pdfs into new folder
        if i[length - 7:] == 'OCR.pdf':
            src_path = os.path.join(directory, i)
            dst_path = os.path.join(directory, 'OCR PDFs', i)
            os.rename(src_path, dst_path)
        # Putting newly made text documents into new folder
        elif i[length - 4:] == '.txt':
            src_path = os.path.join(directory, i)
            dst_path = os.path.join(directory, 'Text Docs', i)
            os.rename(src_path, dst_path)


