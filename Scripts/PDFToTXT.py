import PyPDF2
import re
import sys
import tools
# python PDFToTXT.py <input_pdf_filepath>


def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)

        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        return pdf_text


def format_text(text):
    # spacing:
    text = re.sub(r" +\.", r".", text)  # removes space before periods
    text = re.sub(r"\.+", r".", text)  # removes double periods
    text = re.sub(r"—", r"•", text)  # dashed lists' to bullet point lists
    text = re.sub(r" *•+ *", r"• ", text)  # handles most bullet point lists' spacing
    text = re.sub(r" +", r" ", text)  # removes double spaces

    # lines:
    #text = re.sub(r"(\S)— ", r"\1\n• ", text)  # handles most dashed lists' taking one line
    text = re.sub(r"\n\s*\n", r"\n", text)  # removes double newline
    text = re.sub(r" \n(.)", r" \1", text)  # breaks in text
    #text = re.sub(r" ([A-Z \-:'’]{3,} )", r"\n\1\n", text)  # capital letters are assumed to be titles
    #text = re.sub(r"/\n(.)", r" \1", text)  # removes / 'slash' breaks in text
    #text = re.sub(r"(.)\n/", r"\1 ", text)  # removes / 'slash' breaks in text
    #text = re.sub(r"\n\s*\n", r"\n", text)  # removes double newline
    text = re.sub(r"(.)•", r"\1\n• ", text)  # handles most bullet point lists' taking one line
    text = re.sub(r"(\. \d+) ", r"\1\n", text)  # handles most numbered toc' taking one line

    text = re.sub(r"\n\Z", r"", text)  # removes newline at the end of page
    return text


if __name__ == '__main__':
    try: pdf_filepath = str(sys.argv[1]) # input_pdf_filepath
    except: pdf_filepath = input("pdf_filepath: ")
    png_folder, mp3_folder, mp4_folder, txt_folder, root_folder = tools.configure_folders(pdf_filepath)

    print("Loading pdf...")
    extracted_text = extract_text_from_pdf(pdf_filepath)  # gets array of page's text from pdf
    for page_num in range(len(extracted_text)):
        txt_path = txt_folder + str(page_num).rjust(3, "0") + ".txt"
        extracted_text[page_num] = format_text(extracted_text[page_num])
        tools.save_file(txt_path, extracted_text[page_num])
        print("Page text formatted: " + txt_path)
