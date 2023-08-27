from moviepy.editor import *
import os
import math
import re
import sys
image_folder = ""  # global folder path
audio_folder = ""  # global folder path
video_folder = ""  # global folder path
#python C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\AudioPlusImagesToVideo.py <image_folder> <audio_folder> <video_folder>
#python C:\Users\Dave\Desktop\Programming\Code\Python\PDFToConverter\AudioPlusImagesToVideo.py C:\Users\Dave\Documents\Handbooks\Step1\Texas_1_2022\Images\ C:\Users\Dave\Documents\Handbooks\Step1\Texas_1_2022\Audio\ C:\Users\Dave\Documents\Handbooks\Step1\Texas_1_2022\Video\


def rename_files(folder):
    for file in os.listdir(folder):
        number_in_file = re.sub(r"\D", "", file)  # gets number from filename
        new_name = (number_in_file + file.split(number_in_file)[1]).rjust(7, "0")  # formats assuming 3 digit number
        os.rename(folder + file, folder + new_name)  # renames file with correct number name like '037.mp4'


def even_video(video):
    video = video.resize(height=2160)
    return video.resize((math.ceil(int(video.w)/2)*2, 2160))  # makes video even


def combine_audio_and_image(image_path, audio_path, output_path):
    audio_clip = AudioFileClip(audio_path)  # create the audio clip object
    image_clip = ImageClip(image_path)  # create the image clip object
    video_clip = image_clip.set_audio(audio_clip)  # combine audio and image
    video_clip = video_clip.set_duration(audio_clip.duration)  # duration of clip is duration of audio
    video_clip = even_video(video_clip)  # makes video even
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # makes sure there is a folder for the video file
    video_clip.write_videofile(output_path, 1, codec="libx264", preset="ultrafast", ffmpeg_params=['-vf', 'format=yuv420p'], threads=12)  # writes the video file
    video_clip.close()
    audio_clip.close()


def make_videos():
    rename_files(image_folder)  # corrects images filenames
    rename_files(audio_folder)  # corrects audio filenames
    loop_count = 0
    for image in os.listdir(image_folder):
        loop_count += 1  # loop to make all video segments
        combine_audio_and_image(image_folder + image, audio_folder + os.listdir(audio_folder)[loop_count-1], video_folder + str(loop_count).rjust(3, "0") + ".mp4")


def combine_videos(fps=60):
    complete_video = ""
    first_video = True
    for video in os.listdir(video_folder):
        next_video = VideoFileClip(video_folder + video)
        if first_video:
            complete_video = next_video  # makes first video the base for adding
            first_video = False
            continue
        complete_video = concatenate_videoclips([complete_video.audio_fadeout(0.01), next_video.audio_fadein(0.01)])  # adds each video one at a time
        print(video)

    complete_video = even_video(complete_video)  # makes video even

    complete_video.write_videofile(video_folder + "complete.mp4", fps, codec="libx264", preset="ultrafast", ffmpeg_params=['-vf', 'format=yuv420p'], threads=12)  # writes the video file
    complete_video.close()



if __name__ == '__main__':
    image_folder = str(sys.argv[1])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Images\\"
    audio_folder = str(sys.argv[2])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Audio\\"
    video_folder = str(sys.argv[3])  # r"C:\Users\Dave\Documents\Handbooks\Step1\California_7-2022\Video\\"
    make_videos()
    combine_videos()
