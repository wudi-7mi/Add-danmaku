'''
Some Configurations
'''

video_format = ['flv']

'''
ArgParser Part
'''

import argparse

parser = argparse.ArgumentParser('Conver flv&ass to mp4')
parser.add_argument('-folder', metavar='"..."',type=str, required=True, help='input the videos folder.')
parser.add_argument('-b', metavar='"..."',type=str, required=True, help='input the videos bitrate.')
args = parser.parse_args()

'''
FFmpeg Part
'''

import ffmpeg
import os

folder = os.path.abspath(args.folder)
print(f'Executing Script in "{folder}"')

bitrate = 5000
if args.b:
  bitrate = int(args.b) * 1000

print(f"Video bitrate {bitrate}k.")

for file in os.listdir(folder):
  if file.split('.')[-1] in video_format:
    file_name = file[:-4]
    print(f'Dealing with file : "{file}"')

    file_path = os.path.abspath(f'{folder}/{file}')
    ass_path = os.path.abspath(f'{folder}/{file_name}.ass')
    ass_path = ass_path.replace('\\', '/')
    ass_path = ass_path.replace(':', '\\\\:')

    task = ffmpeg.input(file_path, hwaccel='cuda')
    task = ffmpeg.output(
      task,
      f'{folder}/{file_name}.mp4',
      loglevel='error',
      **{'y':None},
      **{'stats':None},
      vf=f'fps=60,scale=1920:1080,subtitles={ass_path}',
      vcodec='h264_nvenc',
      video_bitrate=f'{bitrate}k',
      acodec='aac',
      audio_bitrate='320k'
    )
    ffmpeg.run(task)
