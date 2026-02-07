#!/usr/bin/env python3
import subprocess
import os

# Paths
avatar = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/avartar/jeff.jpg"
audio = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01/voiceover-en.m4a"
bg_video = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01/final_video_en.mp4"
output = "/Users/kaizhen/zhenkaiii.github.io/myworkspace/twitter-bot/scripts/2026-02-01/final_video_en_talking.mp4"

# Create talking head overlay - circular avatar in bottom right
cmd = f"""ffmpeg -i {bg_video} -loop 1 -i {avatar} -filter_complex "
[1:v]scale=250:-1,crop=250:250,format=yuva420p,geq='lum=p(X,Y):a=if(gt(abs(W/2-X),W/2)*gt(abs(H/2-Y),H/2),0,255)'[avatar];
[0:v][avatar]overlay=W-w-30:H-h-30[v]
" -map "[v]" -map 0:a -c:v libx264 -c:a copy -t 445 {output} -y"""

os.system(cmd)

size = os.path.getsize(output) / (1024*1024)
result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', output], capture_output=True, text=True)
duration = float(result.stdout.strip())
print(f"\n✓ Talking head video: {output} ({size:.1f} MB, {int(duration//60)}:{int(duration%60):02d})")
