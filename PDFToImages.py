from pdf2image import convert_from_path
import PyPDF2
import sys
import os

# python C:\Users\Dave\PycharmProjects\pythonProject\PDFToTextConverter\PDFToImages.py <pdf_filepath> <images_folder_filepath>
# python C:\Users\Dave\PycharmProjects\pythonProject\PDFToTextConverter\main.py C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\California_7-2022.pdf C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Images\


def count_pages(pdf_filepath):
    file = open(pdf_filepath, 'rb')
    return PyPDF2.PdfFileReader(file).numPages

if __name__ == '__main__':
    pdf_filepath = str(sys.argv[1])  # pdf filepath for input, from command line
    images_folder = str(sys.argv[2])  # images folder filepath for output, from command line Texas_1_2022
    os.makedirs(os.path.dirname(images_folder), exist_ok=True)  # makes folder if not there

    total_pages = count_pages(pdf_filepath)
    page_num = 0
    while page_num < total_pages:
        page_num += 1
        pages = convert_from_path(pdf_filepath, 500, first_page=page_num, last_page=page_num, thread_count=12)  # gets array of page from pdf
        pages[0].save(images_folder + str(page_num) + ".png", "PNG")  # saves each page in folder based on page number
        print("Page saved: " + str(page_num))
