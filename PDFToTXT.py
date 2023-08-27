import PyPDF2
import re
import sys
import os

# python C:\Users\Dave\PycharmProjects\pythonProject\PDFToTextConverter\main.py C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\California_7-2022.pdf C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Unformated.txt

def extract_text_from_pdf(pdf_file: str) -> [str]:
    # Open the PDF file of your choice
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        # no_pages = len(reader.pages)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return pdf_text

if __name__ == '__main__':
    pdf_filepath = str(sys.argv[1])  # pdf filepath for input, from command line
    txt_filepath = str(sys.argv[2])  # txt filepath for output, from command line
    extracted_text = extract_text_from_pdf(pdf_filepath)  # gets array of page's text from pdf
    formatted_text = ""
    count = 0
    for page in extracted_text:
        # spacing:
        page = re.sub(r"\.+", r".", page)  # removes double periods
        page = re.sub(r" +\.", r".", page)  # removes space before periods
        page = re.sub(r"—", r"•", page)  # dashed lists' to bullet point lists
        page = re.sub(r" *•+ *", r"• ", page)  # handles most bullet point lists' spacing
        page = re.sub(r" +", r" ", page)  # removes double spaces

        # lines:
        page = re.sub(r"(\S)• ", r"\1\n• ", page)  # handles most bullet point lists' taking one line
        page = re.sub(r"(\S)— ", r"\1\n• ", page)  # handles most dashed lists' taking one line
        page = re.sub(r"\n\s*\n", r"\n", page)  # removes double newline
        page = re.sub(r" \n(.)", r" \1", page)  # breaks in text
        page = re.sub(r"/\n(.)", r" \1", page)  # removes / 'slash' breaks in text
        page = re.sub(r"(.)\n/", r"\1 ", page)  # removes / 'slash' breaks in text
        page = re.sub(r"\n\s*\n", r"\n", page)  # removes double newline
        page = re.sub(r"\n\Z", r"", page)  # removes newline at the end of page

        formatted_text += page + "\n\n\n"  # inserts each page will 2 blank lines between
        count += 1
        print("Page text formatted: " + str(count))
    os.makedirs(os.path.dirname(txt_filepath), exist_ok=True)  # makes sure there is a folder for the text file
    with open(txt_filepath, "w", encoding='utf-8') as f:
        f.write(formatted_text)  # makes the txt file with the formatted text from all the pages
