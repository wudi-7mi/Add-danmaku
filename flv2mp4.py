'''
ArgParser Part
'''

import argparse

parser = argparse.ArgumentParser('Convert flv to mp4')
parser.add_argument('-folder', metavar='"..."',type=str, required=True, help='input the videos folder.')
args = parser.parse_args()

'''
FFmpeg Part
'''

import ffmpeg
import os

folder = os.path.abspath(args.folder)
print(f'Executing Script in "{folder}"')

for file in os.listdir(folder):
  if file.split('.')[-1] == 'flv':
    file_name = file[:-4]
    print(f'Dealing with file : "{file}"')

    file_path = os.path.abspath(f'{folder}/{file}')

    task = ffmpeg.input(file_path)
    task = ffmpeg.output(
      task,
      f'{folder}/{file_name}.mp4',
      loglevel='error',
      **{'y':None},
      **{'stats':None},
      acodec='copy',
      vcodec='copy'
    )
    ffmpeg.run(task)
    



'''
Console command:
ffmpeg \
-i [input video] \
-c copy \
[output video]
'''
