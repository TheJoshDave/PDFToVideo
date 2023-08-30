import os, re, PyPDF2


def rename_files(folder: str):
    ensure_folder(folder)
    for file in os.listdir(folder):
        number_in_file = re.sub(r"\D", "", file)  # gets number from filename
        new_name = (number_in_file + file.split(number_in_file)[1]).rjust(7, "0")  # formats assuming 3 digit number
        os.rename(folder + file, folder + new_name)  # renames file with correct number name like '037.mp4'


def save_file(path: str, content: str):
    with open(path, "w", encoding='utf-8') as f:
        f.write(content)


def count_pages(pdf_filepath: str) -> [int]:
    file = open(pdf_filepath, 'rb')
    return PyPDF2.PdfFileReader(file).numPages


def ensure_folder(folder: str):
    os.makedirs(os.path.dirname(folder), exist_ok=True)


def dir_list_txt(folder: str, output_txt_path: str, prefix="", seperator="\\"):
    ensure_folder(folder)
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for filename in os.listdir(folder):
            f.write(prefix + os.path.join(folder, filename).replace("\\", seperator) + "\n")


def configure_folders(pdf_filepath: str):
    root_folder = os.path.dirname(pdf_filepath) + "\\"
    png_folder = root_folder + "Images\\"
    mp3_folder = root_folder + "Audio\\"
    mp4_folder = root_folder + "Video\\"
    txt_folder = root_folder + "Text\\"
    for folder in [png_folder, mp3_folder, mp4_folder, txt_folder, root_folder]:
        ensure_folder(folder)
    return png_folder, mp3_folder, mp4_folder, txt_folder, root_folder


