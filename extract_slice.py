import subprocess
from pathlib import Path

video = Path(r"C:\shahul\Desktop\fyd\evidence\videos\fynd_mini_checkout_final_demo.mp4")
out_dir = Path(r"C:\shahul\Desktop\fyd\evidence\screenshots\video_frames")
ffmpeg = r"D:\Project\ffmpeg\bin\ffmpeg.exe"

for sec in range(65, 78, 2):
    ts = f"00:01:{sec:02d}"
    out_file = out_dir / f"frame_{sec}s.png"
    cmd = [ffmpeg, "-y", "-ss", ts, "-i", str(video), "-vframes", "1", str(out_file)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Frame at {sec}s extracted")
