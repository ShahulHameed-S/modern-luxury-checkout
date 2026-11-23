import zipfile
from pathlib import Path

workspace = Path(__file__).resolve().parent
zip_path = workspace / "fynd-mini-checkout.zip"

include_patterns = [
    "index.html",
    "styles.css",
    "app.js",
    "requirements.txt",
    "pytest.ini",
    "README.md",
    "TEST_PLAN.md",
    "TEST_RESULTS.md",
    "FINAL_AUDIT_REPORT.md",
    "record_final_demonstration.py",
    "capture_evidence.py",
]

include_dirs = [
    ("tests", ["*.py"]),
    ("assets/images", ["*.jpg", "*.png", "*.svg"]),
    ("evidence/screenshots", ["*.png"]),
    ("evidence/videos", ["fynd_mini_checkout_final_demo.mp4", "fynd_mini_checkout_final_demo.webm"]),
]

print(f"Creating updated submission package: {zip_path.name}...")
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for file_name in include_patterns:
        file_path = workspace / file_name
        if file_path.exists():
            zf.write(file_path, arcname=file_name)
            print(f"  + Added: {file_name}")

    for dir_rel, patterns in include_dirs:
        dir_path = workspace / dir_rel
        if dir_path.exists():
            for p in patterns:
                for match in dir_path.glob(p):
                    rel = match.relative_to(workspace)
                    zf.write(match, arcname=str(rel).replace("\\", "/"))
                    print(f"  + Added: {rel}")

zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
print(f"\nSuccessfully generated {zip_path.name} ({zip_size_mb:.2f} MB, {zip_path.stat().st_size:,} bytes).")
