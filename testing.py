import subprocess
from random import randint 
# Add music to the video
DIR="static/"
init = randint(100,300)
music ="static/music/Blue_Mood-Robert_Munzinger.mp3"
command3 = f"ffmpeg -i {DIR}alice/final5.mp4 -ss {init} -i {music} -af 'afade=in:st=0:d=4,afade=out:st=55:d=3' -map 0:0 -map 1:0 -shortest -y {DIR}alice/Final_End.mp4"
subprocess.run(command3, shell=True)