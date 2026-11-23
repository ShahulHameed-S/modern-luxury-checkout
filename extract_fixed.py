import subprocess
from pathlib import Path

video = Path(r"C:\shahul\Desktop\fyd\evidence\videos\fynd_mini_checkout_final_demo.mp4")
out_dir = Path(r"C:\shahul\Desktop\fyd\evidence\screenshots\video_frames")
ffmpeg = r"D:\Project\ffmpeg\bin\ffmpeg.exe"

for total_sec in [68, 69, 70, 71, 72, 73]:
    m = total_sec // 60
    s = total_sec % 60
    ts = f"00:{m:02d}:{s:02d}"
    out_file = out_dir / f"frame_actual_{total_sec}s.png"
    cmd = [ffmpeg, "-y", "-ss", ts, "-i", str(video), "-vframes", "1", str(out_file)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted {total_sec}s ({ts}): exists={out_file.exists()}, size={out_file.stat().st_size if out_file.exists() else 0}")
