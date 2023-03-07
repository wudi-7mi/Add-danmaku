import subprocess
import ffmpeg
import os
import argparse
import platform
from incomestat import getfolderstat


def detectSys():
  if platform.system() == "Windows":
    execFileName = os.path.abspath("DF_REL1.62CLI.exe")
  elif platform.system() == "Linux":
    execFileName = os.path.abspath("DanmakuFactory")
  else:
    print("不支持该系统")
    exit()
  return execFileName


def trans(folder:str, bitrate:int):
  '''
  folder: videos' folder
  bitrate: kbps
  '''
  for file in os.listdir(folder):
    if file.split('.')[-1] in video_format:
      file_name = file[:-4]
      print(f'Dealing with file : "{file}"')

      execFileName = detectSys()
      file_path = os.path.abspath(f'{folder}/{file}')
      xml_path = os.path.abspath(f'{folder}/{file_name}.xml')
      ass_path = os.path.abspath(f'{folder}/{file_name}.ass')
      subprocess.run([execFileName, "--showmsgbox", "FALSE", "-i", xml_path, "-o", ass_path])
      # subprocess.call(f'{execFileName} --showmsgbox FALSE -i "{xml_path}" -o "{ass_path}"')
      ass_path = ass_path.replace('\\', '/')
      ass_path = ass_path.replace(':', '\\\\:')

      task = ffmpeg.input(file_path, hwaccel='cuda')
      task = ffmpeg.output(
        task,
        f'{folder}/{file_name}.mp4',
        loglevel='error',
        y = None,
        stats = None,
        vf=f'fps=60,scale=1920:1080,subtitles={ass_path}',
        vcodec='h264_nvenc',
        video_bitrate=f'{bitrate}k',
        acodec='aac',
        audio_bitrate='320k'
      )
      ffmpeg.run(task)
    
    
if __name__ == "__main__":
  video_format = ['flv']
  
  parser = argparse.ArgumentParser('Convert xml&flv to mp4')
  parser.add_argument('-folder', metavar='"..."',type=str, required=True, help='input the videos folder.')
  parser.add_argument('-b', metavar='"..."',type=str, required=True, help='input the videos bitrate.')
  args = parser.parse_args()

  folder = os.path.abspath(args.folder)
  print(f'Executing Script in "{folder}"')

  bitrate = 6500
  if args.b:
    bitrate = int(args.b) * 1000
    
  print(f"Video bitrate {bitrate}k.")

  trans(folder, bitrate)
  
  print("直播流水信息：")
  getfolderstat(folder)
  

'''
Console command:
ffmpeg \
-hwaccel cuda -c:v h264_cuvid -y -hide_banner \
-i [input video] \
-vf fps=fps=60,scale=1920:1080,subtitles=[input ass] \
-b:v 5000k -vcodec h264_nvenc \
[output video]
'''
