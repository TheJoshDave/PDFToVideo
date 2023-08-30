from gtts import gTTS
import sys
import pyttsx3
import tools
import os
# python TTS.py <input_pdf_filepath>


def basicgTTS(inputText, outputFilepath):
    myobj = gTTS(text=inputText, lang='en', slow=False, tld='us')
    myobj.save(outputFilepath)


def basicpyttsx3(inputText, outputFilepath, rate=100, voice=1):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    engine.save_to_file(inputText, outputFilepath)
    engine.runAndWait()


if __name__ == '__main__':
    try: pdf_filepath = str(sys.argv[1]) # input_pdf_filepath
    except: pdf_filepath = input("pdf_filepath: ")
    png_folder, mp3_folder, mp4_folder, txt_folder, root_folder = tools.configure_folders(pdf_filepath)

    for txt_num in range(len(os.listdir(txt_folder))):
        input_txt_filepath = txt_folder + os.listdir(txt_folder)[txt_num]
        output_mp3_filepath = mp3_folder + str(txt_num).rjust(3, "0") + ".mp3"
        with open(input_txt_filepath, "r", encoding='utf-8') as file:
            inputText = file.read()

        print("Reading: " + input_txt_filepath)
        print("Writing: " + output_mp3_filepath)
        basicpyttsx3(inputText, output_mp3_filepath, 140)
        #basicgTTS(inputText, outputFilepath)

