from moviepy.editor import AudioFileClip


def mp4_to_mp3(file_path):
    video = AudioFileClip(f'{file_path}.mp4')
    print(f'writing to {file_path}.mp3')
    video.write_audiofile(f'{file_path}.mp3')
