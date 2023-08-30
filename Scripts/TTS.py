from gtts import gTTS
import sys
import pyttsx3
#python TTS.py <input_txt_filepath> <output_mp3_filepath>


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
    txt_filepath = str(sys.argv[1])  # input_txt_filepath
    outputFilepath = str(sys.argv[2])  # output_mp3_filepath
    with open(txt_filepath, "r", encoding='utf-8') as file:
        inputText = file.read()

    print(txt_filepath)
    print(outputFilepath)
    #basicgTTS(inputText, outputFilepath)
    basicpyttsx3(inputText, outputFilepath, 140)

