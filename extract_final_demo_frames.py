import subprocess
from pathlib import Path

video = Path(r"C:\shahul\Desktop\fyd\evidence\videos\fynd_mini_checkout_final_demo.mp4")
out_dir = Path(r"C:\shahul\Desktop\fyd\evidence\screenshots\final_demo_frames")
out_dir.mkdir(parents=True, exist_ok=True)
ffmpeg = r"D:\Project\ffmpeg\bin\ffmpeg.exe"

timestamps = [
    ("scene1_intro_04s.png", "00:00:04"),
    ("scene2_selection_12s.png", "00:00:12"),
    ("scene3_quantities_24s.png", "00:00:24"),
    ("scene4_validation_35s.png", "00:00:35"),
    ("scene5_receipt_50s.png", "00:00:50"),
    ("scene6_reset_62s.png", "00:01:02"),
    ("scene7_empty_cart_71s.png", "00:01:11"),
    ("scene8_final_view_84s.png", "00:01:24"),
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
