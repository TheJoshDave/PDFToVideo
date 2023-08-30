from pdf2image import convert_from_path
import sys
import tools
# python PDFToImages.py <input_pdf_filepath>


if __name__ == '__main__':
    try: pdf_filepath = str(sys.argv[1]) # input_pdf_filepath
    except: pdf_filepath = input("pdf_filepath: ")
    png_folder, mp3_folder, mp4_folder, txt_folder, root_folder = tools.configure_folders(pdf_filepath)

    print("Loading pdf...")
    pages = convert_from_path(pdf_filepath, 500, first_page=1, last_page=tools.count_pages(pdf_filepath), thread_count=12)  # array of pages
    for page_num in range(len(pages)):
        image_path = png_folder + str(page_num).rjust(3, "0") + ".png"
        pages[page_num].save(image_path, "PNG")  # saves
        print("Page saved: " + image_path)
