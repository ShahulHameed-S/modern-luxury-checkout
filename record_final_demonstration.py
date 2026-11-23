"""
Fynd Mini Checkout - Final Professional Demonstration & Screen Recording
Follows the exact 8-scene sequence requested in user instructions:
  Scene 1: Introduction (0-7s)
  Scene 2: Product Selection (7-18s)
  Scene 3: Quantity Management (18-32s)
  Scene 4: Validation (32-47s)
  Scene 5: Successful Checkout (47-65s)
  Scene 6: New Order (65-75s)
  Scene 7: Empty Cart Validation (75-85s)
  Scene 8: Final View (85-95s)

Output Target:
  - Resolution: 1920x1080 (30 FPS)
  - Target Duration: 85-95 seconds
  - Format: MP4 (H.264) + WebM
  - File: evidence/videos/fynd_mini_checkout_final_demo.mp4
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = WORKSPACE_ROOT / "evidence" / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MP4_PATH = VIDEOS_DIR / "fynd_mini_checkout_final_demo.mp4"
FINAL_WEBM_PATH = VIDEOS_DIR / "fynd_mini_checkout_final_demo.webm"

FFMPEG_EXE = Path(r"D:\Project\ffmpeg\bin\ffmpeg.exe")

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def inject_cursor_effects(page):
    """
    Injects a luxury translucent violet virtual mouse cursor with subtle click ripple.
    """
    page.evaluate("""
        (() => {
            if (document.getElementById('demo-virtual-cursor')) return;
            const cursor = document.createElement('div');
            cursor.id = 'demo-virtual-cursor';
            cursor.style.width = '24px';
            cursor.style.height = '24px';
            cursor.style.border = '2px solid #635BDB';
            cursor.style.backgroundColor = 'rgba(99, 91, 219, 0.28)';
            cursor.style.borderRadius = '50%';
            cursor.style.position = 'fixed';
            cursor.style.pointerEvents = 'none';
            cursor.style.zIndex = '9999999';
            cursor.style.transition = 'transform 0.08s ease-out, background-color 0.12s ease, border-color 0.12s ease';
            cursor.style.transform = 'translate(-50%, -50%)';
            cursor.style.boxShadow = '0 0 12px rgba(99, 91, 219, 0.45)';
            cursor.style.display = 'none';
            document.body.appendChild(cursor);

            window.addEventListener('mousemove', (e) => {
                cursor.style.display = 'block';
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });

            window.addEventListener('mousedown', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(0.65)';
                cursor.style.backgroundColor = 'rgba(79, 70, 229, 0.65)';
                cursor.style.borderColor = '#4338CA';
            });

            window.addEventListener('mouseup', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
                cursor.style.backgroundColor = 'rgba(99, 91, 219, 0.28)';
                cursor.style.borderColor = '#635BDB';
            });
        })();
    """)


def smooth_move(page, selector, steps=12, offset_x=0, offset_y=0):
    """Smoothly moves the virtual mouse to the target element."""
    try:
        loc = page.locator(selector).first
        loc.scroll_into_view_if_needed()
        box = loc.bounding_box()
        if box:
            target_x = box["x"] + box["width"] / 2 + offset_x
            target_y = box["y"] + box["height"] / 2 + offset_y
            page.mouse.move(target_x, target_y, steps=steps)
            return box
    except Exception as e:
        print(f"[WARN] smooth_move warning for {selector}: {e}")
    return None


def run_recording():
    app_url = "http://localhost:8000/index.html"
    print(f"[RECORDER] Target: {app_url}")
    print("[RECORDER] Configuring 1920x1080 30FPS recording session...")

    session_start = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-web-security",
                "--window-size=1920,1080",
                "--hide-scrollbars",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        # =========================================================================
        # SCENE 1 — INTRODUCTION (Target: 0 to 7 seconds)
        # =========================================================================
        print("\n>>> SCENE 1 (0-7s): Introduction & Catalogue Presentation")
        page.goto(app_url)
        page.wait_for_selector("#checkout-view", state="visible")
        inject_cursor_effects(page)
        time.sleep(0.5)

        # Highlight brand monogram and name
        smooth_move(page, ".brand", steps=10)
        time.sleep(1.0)

        # Highlight editorial collection headline
        smooth_move(page, ".hero-title", steps=10)
        time.sleep(1.2)

        # Hover over product catalogue
        smooth_move(page, '[data-testid="product-card-headphones"]', steps=10)
        time.sleep(1.0)
        smooth_move(page, '[data-testid="product-card-smartwatch"]', steps=10)
        time.sleep(1.0)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 1 completed.")

        # =========================================================================
        # SCENE 2 — PRODUCT SELECTION (Target: 7 to 18 seconds)
        # =========================================================================
        print("\n>>> SCENE 2 (7-18s): Product Selection & Live Cart Counts")
        # Add Wireless Headphones (₹1,499)
        smooth_move(page, '[data-testid="add-to-cart-headphones"]', steps=10)
        time.sleep(0.5)
        page.locator('[data-testid="add-to-cart-headphones"]').click()
        time.sleep(0.6)

        # Show header cart pill update to 1
        smooth_move(page, "#header-cart-pill", steps=8)
        time.sleep(1.0)

        # Show Headphones appearing in cart table
        smooth_move(page, '[data-testid="cart-item-headphones"]', steps=10)
        time.sleep(1.2)

        # Add Smart Watch (₹2,499)
        smooth_move(page, '[data-testid="add-to-cart-smartwatch"]', steps=10)
        time.sleep(0.5)
        page.locator('[data-testid="add-to-cart-smartwatch"]').click()
        time.sleep(0.6)

        # Show header cart pill update to 2
        smooth_move(page, "#header-cart-pill", steps=8)
        time.sleep(1.0)

        # Hover over Smart Watch in cart table
        smooth_move(page, '[data-testid="cart-item-smartwatch"]', steps=10)
        time.sleep(1.2)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 2 completed.")

        # =========================================================================
        # SCENE 3 — QUANTITY MANAGEMENT (Target: 18 to 32 seconds)
        # =========================================================================
        print("\n>>> SCENE 3 (18-32s): Quantity Management & Calculation (Target: ₹10,495)")
        # 1. Increase Headphones from 1 to 2
        smooth_move(page, '[data-testid="qty-increase-headphones"]', steps=10)
        time.sleep(0.5)
        page.locator('[data-testid="qty-increase-headphones"]').click()
        time.sleep(0.5)

        # Highlight line total for Headphones (2 x ₹1,499 = ₹2,998)
        smooth_move(page, '[data-testid="line-total-headphones"]', steps=8)
        time.sleep(1.5)

        # 2. Increase Smart Watch from 1 to 2
        smooth_move(page, '[data-testid="qty-increase-smartwatch"]', steps=10)
        time.sleep(0.5)
        page.locator('[data-testid="qty-increase-smartwatch"]').click()
        time.sleep(0.8)

        # 3. Increase Smart Watch from 2 to 3
        smooth_move(page, '[data-testid="qty-increase-smartwatch"]', steps=8)
        time.sleep(0.5)
        page.locator('[data-testid="qty-increase-smartwatch"]').click()
        time.sleep(0.5)

        # Highlight line total for Smart Watch (3 x ₹2,499 = ₹7,497)
        smooth_move(page, '[data-testid="line-total-smartwatch"]', steps=8)
        time.sleep(1.8)

        # 4. Highlight Order Summary and Grand Total: ₹10,495
        smooth_move(page, "#summary-subtotal", steps=8)
        time.sleep(1.0)
        smooth_move(page, '[data-testid="order-total"]', steps=10)
        time.sleep(2.5)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 3 completed.")

        # =========================================================================
        # SCENE 4 — VALIDATION (Target: 32 to 47 seconds)
        # =========================================================================
        print("\n>>> SCENE 4 (32-47s): Form Validation & State Preservation")
        # Ensure customer name is empty
        name_input = page.locator('[data-testid="customer-name-input"]')
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(0.6)

        # Click Place Order without entering customer name
        smooth_move(page, '[data-testid="place-order-btn"]', steps=10)
        time.sleep(0.5)
        page.locator('[data-testid="place-order-btn"]').click()
        time.sleep(0.6)

        # Validation banner displays
        page.wait_for_selector("#validation-container", state="visible")
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(0.4)
        smooth_move(page, "#validation-container", steps=10)
        time.sleep(2.5)

        # Demonstrate customer name field error outline (.input-error)
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(1.5)

        # Demonstrate cart contents & quantities remain completely preserved!
        smooth_move(page, '[data-testid="cart-item-headphones"]', steps=8)
        time.sleep(1.0)
        smooth_move(page, '[data-testid="cart-item-smartwatch"]', steps=8)
        time.sleep(1.0)

        # Enter valid customer name: "Demo User"
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(0.4)
        name_input.click()
        time.sleep(0.2)
        name_input.type("Demo User", delay=95)
        time.sleep(0.8)
        smooth_move(page, "#customer-name-help", steps=6)
        time.sleep(1.2)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 4 completed.")

        # =========================================================================
        # SCENE 5 — SUCCESSFUL CHECKOUT (Target: 47 to 65 seconds)
        # =========================================================================
        print("\n>>> SCENE 5 (47-65s): Checkout & Order Confirmation Receipt")
        # Move to Place Order
        smooth_move(page, '[data-testid="place-order-btn"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="place-order-btn"]').click()
        time.sleep(1.0)

        # Wait for Order Confirmation view
        page.wait_for_selector('[data-testid="order-confirmation"]', state="visible")
        time.sleep(0.8)

        # Smooth move over Order Confirmation Header
        smooth_move(page, ".confirmation-header", steps=10)
        time.sleep(2.0)

        # Hover over unique Order Reference
        smooth_move(page, '[data-testid="order-reference"]', steps=8)
        time.sleep(2.0)

        # Hover over Customer Name
        smooth_move(page, '[data-testid="confirmation-customer-name"]', steps=8)
        time.sleep(1.5)

        # Hover over Total Amount Paid: ₹10,495
        smooth_move(page, '[data-testid="confirmation-total"]', steps=10)
        time.sleep(2.2)

        # Hover over Purchased Items breakdown list
        smooth_move(page, "#confirm-items-list", steps=10)
        time.sleep(3.2)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 5 completed.")

        # =========================================================================
        # SCENE 6 — NEW ORDER (Target: 65 to 75 seconds)
        # =========================================================================
        print("\n>>> SCENE 6 (65-75s): Start New Order & State Reset")
        # Move to Start New Order button
        smooth_move(page, '[data-testid="start-new-order-btn"]', steps=10)
        time.sleep(0.8)
        page.locator('[data-testid="start-new-order-btn"]').click()
        time.sleep(1.0)

        # Checkout grid returns
        page.wait_for_selector("#checkout-view", state="visible")
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(0.6)

        # Hover over empty cart placeholder
        smooth_move(page, '[data-testid="empty-cart-message"]', steps=10)
        time.sleep(2.0)

        # Hover over reset Order Summary (₹0)
        smooth_move(page, '[data-testid="order-total"]', steps=8)
        time.sleep(1.6)

        # Hover over reset customer name input
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(1.6)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 6 completed.")

        # =========================================================================
        # SCENE 7 — EMPTY CART VALIDATION (Target: 75 to 85 seconds)
        # =========================================================================
        print("\n>>> SCENE 7 (75-85s): Empty Cart Checkout Validation")
        # Enter customer name "Demo User" while cart is completely empty
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(0.4)
        name_input.click()
        time.sleep(0.2)
        name_input.type("Demo User", delay=95)
        time.sleep(0.8)

        # Click Place Order on empty cart
        smooth_move(page, '[data-testid="place-order-btn"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="place-order-btn"]').click()
        time.sleep(0.6)

        # Validation banner displays empty cart error
        page.wait_for_selector("#validation-container", state="visible")
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        time.sleep(0.4)
        smooth_move(page, "#validation-container", steps=10)
        time.sleep(3.2)

        # Show that customer name input is still intact
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(1.5)
        print(f"[T = {time.time() - session_start:.2f}s] Scene 7 completed.")

        # =========================================================================
        # SCENE 8 — FINAL VIEW (Target: 85 to 95 seconds)
        # =========================================================================
        print("\n>>> SCENE 8 (85-95s): Final Catalogue View & Brand Signoff")
        # Dismiss error banner cleanly
        try:
            smooth_move(page, "#dismiss-alert-btn", steps=8)
            time.sleep(0.5)
            page.locator("#dismiss-alert-btn").click()
            time.sleep(0.8)
        except Exception as e:
            print(f"[INFO] Alert dismiss fallback: {e}")

        # Smooth glide across the curated product catalogue
        smooth_move(page, '[data-testid="product-card-headphones"]', steps=10)
        time.sleep(1.2)
        smooth_move(page, '[data-testid="product-card-smartwatch"]', steps=10)
        time.sleep(1.2)

        # Move to brand header monogram and title for final outro
        smooth_move(page, ".brand", steps=12)
        time.sleep(2.0)

        # Ensure we stay within 85-95s
        elapsed_so_far = time.time() - session_start
        if elapsed_so_far < 88.0:
            remaining = 89.0 - elapsed_so_far
            print(f"[RECORDER] Smooth outro hold: {remaining:.1f}s to reach target window...")
            time.sleep(remaining)

        print(f"[T = {time.time() - session_start:.2f}s] Scene 8 completed. Total session elapsed.")

        # Conclude browser recording
        raw_video = page.video
        page.close()
        context.close()
        browser.close()

        raw_path = Path(raw_video.path())
        total_recorded = time.time() - session_start
        print(f"\n[RECORDER] Browser automation finished in {total_recorded:.2f} seconds.")
        print(f"[RECORDER] Raw Playwright recording: {raw_path}")

        # Move / copy raw recording to WebM
        if FINAL_WEBM_PATH.exists():
            FINAL_WEBM_PATH.unlink()
        shutil.copy2(str(raw_path), str(FINAL_WEBM_PATH))
        print(f"[RECORDER] Saved WebM: {FINAL_WEBM_PATH} ({FINAL_WEBM_PATH.stat().st_size:,} bytes)")

    # =========================================================================
    # TRANSCODE TO 1080p 30FPS MP4 (H.264) USING FFMPEG
    # =========================================================================
    if FFMPEG_EXE.exists():
        print(f"\n[FFMPEG] Transcoding WebM to MP4 at 1920x1080 30FPS via {FFMPEG_EXE}...")
        if FINAL_MP4_PATH.exists():
            FINAL_MP4_PATH.unlink()

        cmd = [
            str(FFMPEG_EXE),
            "-y",
            "-i", str(FINAL_WEBM_PATH),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-movflags", "+faststart",
            str(FINAL_MP4_PATH)
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and FINAL_MP4_PATH.exists():
            print(f"[FFMPEG] Transcode SUCCESS! Saved: {FINAL_MP4_PATH} ({FINAL_MP4_PATH.stat().st_size:,} bytes)")
        else:
            print(f"[FFMPEG] Warning: Transcode returned code {result.returncode}:\n{result.stderr[-400:]}")
    else:
        print(f"[FFMPEG] ffmpeg executable not found at {FFMPEG_EXE}. Keeping WebM as primary.")

    # =========================================================================
    # INSPECT GENERATED VIDEO SPECS
    # =========================================================================
    inspect_video(FINAL_MP4_PATH if FINAL_MP4_PATH.exists() else FINAL_WEBM_PATH)


def inspect_video(target_file: Path):
    """Inspects duration, resolution, frame rate, and size."""
    print(f"\n[VERIFICATION] Inspecting video specs for {target_file.name}...")
    if not target_file.exists():
        print(f"[ERROR] Target file does not exist: {target_file}")
        return

    size_mb = target_file.stat().st_size / (1024 * 1024)
    print(f"  File size: {size_mb:.2f} MB ({target_file.stat().st_size:,} bytes)")

    if FFMPEG_EXE.exists():
        cmd = [str(FFMPEG_EXE), "-i", str(target_file)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # ffmpeg outputs stream info to stderr
        output = res.stderr
        for line in output.splitlines():
            if "Duration:" in line or "Stream #0" in line:
                print(f"  {line.strip()}")


if __name__ == "__main__":
    run_recording()
