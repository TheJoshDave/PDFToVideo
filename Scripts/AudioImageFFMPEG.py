import os
import math
import sys
import librosa
import tools
# python AudioImageFFMPEG.py <input_pdf_filepath>


def make_videos(image_folder: str, audio_folder: str, video_folder: str):
    for image_num in range(len(os.listdir(image_folder))):
        image_path = image_folder + os.listdir(image_folder)[image_num]
        audio_path = audio_folder + os.listdir(audio_folder)[image_num]
        output_path = video_folder + str(image_num).rjust(3, "0") + ".mp4"
        os.system('ffmpeg -loop 1 -framerate 1 -i ' + image_path + ' -i ' + audio_path + ' -vf scale=-2:2160 -shortest -pix_fmt yuv420p -y -c:v h264_nvenc ' + output_path)


def merge_videos(folder):
    tools.dir_list_txt(folder, 'join_video.txt', 'file ', "/")
    os.system('ffmpeg -safe 0 -f concat -i join_video.txt -c:v h264_nvenc -y ' + folder + 'Completed.mp4')
    os.remove('join_video.txt')


def make_description(audio_folder: str, video_folder: str, state: str, year: str, month="", day=""):
    title = state + " Driver Handbook - Audio - " + year
    tools.save_file(video_folder + "title.txt", title)

    description = "The " + state + " Driver License Handbook - Audio - "
    if not month == "":
        description += month + " "
        if not day == "":
            description += day + ", "
    description += year + "\nDownload the handbook: \n"
    TotalAudioLength = 0
    for mp3 in os.listdir(audio_folder):
        hour = math.floor(math.floor(TotalAudioLength / 60) / 60) % 24
        minute = math.floor(TotalAudioLength / 60) % 60
        second = math.floor(TotalAudioLength % 60)
        if hour:
            description += str(hour) + ":" + str(minute).rjust(2, "0") + ":" + str(second).rjust(2, "0")
        elif minute:
            description += str(minute) + ":" + str(second).rjust(2, "0")
        else:
            description += "0:" + str(second).rjust(2, "0")
        description += "\n"
        TotalAudioLength += librosa.get_duration(path=audio_folder + mp3)
    tools.save_file(video_folder + "description.txt", description)

    tags = "Audio, Sound, Audiobook, Driver, Driving, Drive, Road, License, Licensing, Test, Exam, Learn, Education, DMV, Permit"
    tags += ", " + state
    tags += ", " + year
    if not month == "":
        tags += ", " + month
    tools.save_file(video_folder + "tags.txt", tags)


if __name__ == '__main__':
    try: pdf_filepath = str(sys.argv[1]) # input_pdf_filepath
    except: pdf_filepath = input("pdf_filepath: ")
    png_folder, mp3_folder, mp4_folder, txt_folder, root_folder = tools.configure_folders(pdf_filepath)

    make_videos(png_folder, mp3_folder, mp4_folder)
    merge_videos(mp4_folder)
    make_description(mp3_folder, mp4_folder, input("State: "), input("Year: "), input("Month: "), input("Day: "))

