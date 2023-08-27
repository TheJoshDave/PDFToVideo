import PyPDF2
import re
import sys
import os
# python PDFToTXT.py <input_pdf_filepath> <output_txt_folder>

def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        # no_pages = len(reader.pages)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return pdf_text


if __name__ == '__main__':
    pdf_filepath = str(sys.argv[1])  # input_pdf_filepath
    txt_filepath = str(sys.argv[2])  # output_txt_folder
    extracted_text = extract_text_from_pdf(pdf_filepath)  # gets array of page's text from pdf
    count = 1
    for page in extracted_text:
        # spacing:
        page = re.sub(r" +\.", r".", page)  # removes space before periods
        page = re.sub(r"\.+", r".", page)  # removes double periods
        page = re.sub(r"—", r"•", page)  # dashed lists' to bullet point lists
        page = re.sub(r" *•+ *", r"• ", page)  # handles most bullet point lists' spacing
        page = re.sub(r" +", r" ", page)  # removes double spaces

        # lines:
        #page = re.sub(r"(\S)— ", r"\1\n• ", page)  # handles most dashed lists' taking one line
        page = re.sub(r"\n\s*\n", r"\n", page)  # removes double newline
        page = re.sub(r" \n(.)", r" \1", page)  # breaks in text
        #page = re.sub(r" ([A-Z \-:'’]{3,} )", r"\n\1\n", page)  # capital letters are assumed to be titles
        #page = re.sub(r"/\n(.)", r" \1", page)  # removes / 'slash' breaks in text
        #page = re.sub(r"(.)\n/", r"\1 ", page)  # removes / 'slash' breaks in text
        #page = re.sub(r"\n\s*\n", r"\n", page)  # removes double newline
        page = re.sub(r"(.)•", r"\1\n• ", page)  # handles most bullet point lists' taking one line
        page = re.sub(r"(\. \d+) ", r"\1\n", page)  # handles most numbered toc' taking one line


        page = re.sub(r"\n\Z", r"", page)  # removes newline at the end of page


        os.makedirs(txt_filepath, exist_ok=True)  # makes sure there is a folder for the text files
        with open(txt_filepath + str(count).rjust(3, "0") + ".txt", "w", encoding='utf-8') as f:
            f.write(page)  # makes txt file for each page
        print("Page text formatted: " + str(count).rjust(3, "0"))
        count += 1
