import subprocess
from pathlib import Path

video = Path(r"C:\shahul\Desktop\fyd\evidence\videos\fynd_mini_checkout_final_demo.mp4")
out_dir = Path(r"C:\shahul\Desktop\fyd\evidence\screenshots\video_frames")
out_dir.mkdir(parents=True, exist_ok=True)
ffmpeg = r"D:\Project\ffmpeg\bin\ffmpeg.exe"

timestamps = [
    ("frame_scene1_intro.png", "00:00:04"),
    ("frame_scene2_selection.png", "00:00:12"),
    ("frame_scene3_quantities.png", "00:00:24"),
    ("frame_scene4_validation.png", "00:00:38"),
    ("frame_scene5_confirmation.png", "00:00:52"),
    ("frame_scene6_reset.png", "00:01:02"),
    ("frame_scene7_empty_cart.png", "00:01:12"),
    ("frame_scene8_final_view.png", "00:01:25"),
]

for filename, ts in timestamps:
    out_file = out_dir / filename
    cmd = [
        ffmpeg, "-y",
        "-ss", ts,
        "-i", str(video),
        "-vframes", "1",
        str(out_file)
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted {filename} at {ts}: exists={out_file.exists()}, size={out_file.stat().st_size if out_file.exists() else 0}")
