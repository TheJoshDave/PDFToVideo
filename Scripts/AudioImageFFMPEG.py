import os
import math
import re
import sys
# python AudioImageFFMPEG.py <input_images_folder> <input_audio_folder> <output_video_folder>
image_folder = ""  # global folder path
audio_folder = ""  # global folder path
video_folder = ""  # global folder path


def rename_files(folder):
    for file in os.listdir(folder):
        number_in_file = re.sub(r"\D", "", file)  # gets number from filename
        new_name = (number_in_file + file.split(number_in_file)[1]).rjust(7, "0")  # formats assuming 3 digit number
        os.rename(folder + file, folder + new_name)  # renames file with correct number name like '037.mp4'


def make_videos():
    rename_files(image_folder)  # corrects images filenames
    rename_files(audio_folder)  # corrects audio filenames
    loop_count = 0
    for image in os.listdir(image_folder):
        loop_count += 1  # loop to make all video segments
        image_path = image_folder + image
        audio_path = audio_folder + os.listdir(audio_folder)[loop_count-1]
        output_path = video_folder + str(loop_count).rjust(3, "0") + ".mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # makes sure there is a folder for the video file
        os.system('ffmpeg -loop 1 -framerate 1 -i ' + image_path + ' -i ' + audio_path + ' -vf scale=-2:2160 -shortest -pix_fmt yuv420p -y -c:v h264_nvenc ' + output_path)


def merge_videos(folder):
    with open('../join_video.txt', 'w') as f:
        for filename in os.listdir(folder):
            f.write('file ' + os.path.join(folder, filename).replace("\\", "/") + "\n")
    os.system('ffmpeg -safe 0 -f concat -i join_video.txt -c:v h264_nvenc -y ' + folder + 'Completed.mp4')
    os.remove('join_video.txt')

if __name__ == '__main__':
    image_folder = str(sys.argv[1])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Images\\"
    audio_folder = str(sys.argv[2])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Audio\\"
    video_folder = str(sys.argv[3])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Video\\"
    make_videos()
    merge_videos(video_folder)

