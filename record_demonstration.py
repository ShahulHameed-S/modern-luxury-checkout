"""
Fynd Mini Checkout - Professional Browser Demonstration & Video Recorder
Executes the exact 13-step demonstration sequence requested by the user,
pacing each interaction naturally, and recording a desktop 1280x900 video.
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

FFMPEG_PATH = Path(r"C:\Users\shahu\AppData\Local\ms-playwright\ffmpeg-1013\ffmpeg-win64.exe")

# Set stdout to UTF-8 for currency symbol compatibility on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def inject_cursor_and_visual_effects(page):
    """
    Injects a subtle visual cursor trail and click ripple effect
    so every mouse movement and click is vividly visible in the recorded video.
    """
    page.evaluate("""
        (() => {
            const cursor = document.createElement('div');
            cursor.id = 'demo-virtual-cursor';
            cursor.style.width = '20px';
            cursor.style.height = '20px';
            cursor.style.border = '2px solid #4f46e5';
            cursor.style.backgroundColor = 'rgba(99, 102, 241, 0.45)';
            cursor.style.borderRadius = '50%';
            cursor.style.position = 'fixed';
            cursor.style.pointerEvents = 'none';
            cursor.style.zIndex = '999999';
            cursor.style.transition = 'transform 0.08s ease-out, background-color 0.15s ease';
            cursor.style.transform = 'translate(-50%, -50%)';
            cursor.style.display = 'none';
            document.body.appendChild(cursor);

            window.addEventListener('mousemove', (e) => {
                cursor.style.display = 'block';
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });

            window.addEventListener('mousedown', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(0.7)';
                cursor.style.backgroundColor = 'rgba(239, 68, 68, 0.7)';
            });

            window.addEventListener('mouseup', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
                cursor.style.backgroundColor = 'rgba(99, 102, 241, 0.45)';
            });
        })();
    """)


def highlight_element(page, selector, text_hint=""):
    """Smoothly moves cursor over an element and highlights it."""
    try:
        loc = page.locator(selector).first
        loc.scroll_into_view_if_needed()
        box = loc.bounding_box()
        if box:
            center_x = box["x"] + box["width"] / 2
            center_y = box["y"] + box["height"] / 2
            page.mouse.move(center_x, center_y, steps=10)
    except Exception:
        pass


def run_demonstration():
    app_url = "http://localhost:8000/index.html"
    print(f"[DEMO] Launching demonstration recorder on {app_url}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-web-security", "--allow-file-access-from-files"]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": 1280, "height": 900}
        )

        page = context.new_page()

        # Step 1: Open homepage and show products visually
        print("Step 1: Showing application homepage and available products...")
        page.goto(app_url)
        page.wait_for_selector("#checkout-view", state="visible")
        inject_cursor_and_visual_effects(page)
        
        # Hover over Product 1
        highlight_element(page, '[data-testid="product-card-headphones"]')
        time.sleep(1.2)
        # Hover over Product 2
        highlight_element(page, '[data-testid="product-card-smartwatch"]')
        time.sleep(1.2)
        # Hover over empty cart
        highlight_element(page, '[data-testid="empty-cart-message"]')
        time.sleep(1.0)

        # Step 2: Add Wireless Headphones to the cart
        print("Step 2: Adding Wireless Headphones to cart...")
        headphones_add_btn = page.locator('[data-testid="add-to-cart-headphones"]')
        box = headphones_add_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        headphones_add_btn.click()
        time.sleep(1.2)

        # Step 3: Add Smart Watch to the cart
        print("Step 3: Adding Smart Watch to cart...")
        smartwatch_add_btn = page.locator('[data-testid="add-to-cart-smartwatch"]')
        box = smartwatch_add_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        smartwatch_add_btn.click()
        time.sleep(1.5)

        # Step 4: Demonstrate increasing and decreasing product quantities
        print("Step 4: Demonstrating quantity increase and decrease controls...")
        # Increase Wireless Headphones to 2
        inc_headphones = page.locator('[data-testid="qty-increase-headphones"]')
        box = inc_headphones.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        inc_headphones.click()
        time.sleep(1.0)

        # Decrease Wireless Headphones back to 1
        dec_headphones = page.locator('[data-testid="qty-decrease-headphones"]')
        box = dec_headphones.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        dec_headphones.click()
        time.sleep(1.0)

        # Increase Smart Watch to 2
        inc_smartwatch = page.locator('[data-testid="qty-increase-smartwatch"]')
        box = inc_smartwatch.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        inc_smartwatch.click()
        time.sleep(1.0)

        # Decrease Smart Watch back to 1
        dec_smartwatch = page.locator('[data-testid="qty-decrease-smartwatch"]')
        box = dec_smartwatch.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        dec_smartwatch.click()
        time.sleep(1.2)

        # Step 5: Demonstrate removing a product
        print("Step 5: Demonstrating product removal (removing Smart Watch)...")
        remove_smartwatch = page.locator('[data-testid="remove-item-smartwatch"]')
        box = remove_smartwatch.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        remove_smartwatch.click()
        time.sleep(1.5)

        # Step 6: Add both products again
        print("Step 6: Adding Smart Watch back to cart...")
        smartwatch_add_btn = page.locator('[data-testid="add-to-cart-smartwatch"]')
        box = smartwatch_add_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        smartwatch_add_btn.click()
        time.sleep(1.5)

        # Step 7: Demonstrate checkout with empty customer name & show validation message
        print("Step 7: Demonstrating checkout with empty customer name...")
        place_order_btn = page.locator('[data-testid="place-order-btn"]')
        box = place_order_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        place_order_btn.click()
        time.sleep(1.0)

        # Highlight the validation banner
        highlight_element(page, '#validation-container')
        time.sleep(2.0)
        # Highlight the red outlined input
        highlight_element(page, '[data-testid="customer-name-input"]')
        time.sleep(1.2)

        # Step 8: Enter customer name: Demo User
        print("Step 8: Entering customer name: 'Demo User'...")
        name_input = page.locator('[data-testid="customer-name-input"]')
        box = name_input.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        name_input.click()
        name_input.type("Demo User", delay=90)
        time.sleep(1.2)

        # Step 9: Set quantities to Headphones: 2, Smart Watch: 3
        print("Step 9: Setting quantities (Headphones: 2, Smart Watch: 3)...")
        # Increase Headphones to 2
        inc_headphones = page.locator('[data-testid="qty-increase-headphones"]')
        box = inc_headphones.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        inc_headphones.click()
        time.sleep(1.0)

        # Increase Smart Watch to 3 (click twice)
        inc_smartwatch = page.locator('[data-testid="qty-increase-smartwatch"]')
        box = inc_smartwatch.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=6)
        time.sleep(0.3)
        inc_smartwatch.click()
        time.sleep(0.8)
        inc_smartwatch.click()
        time.sleep(1.2)

        # Step 10: Show the correct total of ₹10,495
        print("Step 10: Highlighting correct line totals and order total of ₹10,495...")
        highlight_element(page, '[data-testid="line-total-headphones"]')
        time.sleep(1.0)
        highlight_element(page, '[data-testid="line-total-smartwatch"]')
        time.sleep(1.0)
        highlight_element(page, '[data-testid="order-total"]')
        time.sleep(2.2)

        # Step 11: Click Place Order
        print("Step 11: Clicking Place Order...")
        place_order_btn = page.locator('[data-testid="place-order-btn"]')
        box = place_order_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.4)
        place_order_btn.click()

        # Step 12: Show successful order confirmation and generated order reference
        print("Step 12: Displaying order confirmation and reference...")
        page.wait_for_selector('[data-testid="order-confirmation"]', state="visible")
        time.sleep(0.8)
        highlight_element(page, '[data-testid="order-reference"]')
        time.sleep(1.5)
        highlight_element(page, '[data-testid="confirmation-total"]')
        time.sleep(1.5)
        highlight_element(page, '#confirm-items-list')
        time.sleep(2.5)

        # Step 13: Show the Start New Order functionality
        print("Step 13: Demonstrating 'Start New Order' reset...")
        new_order_btn = page.locator('[data-testid="start-new-order-btn"]')
        box = new_order_btn.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=8)
        time.sleep(0.5)
        new_order_btn.click()
        time.sleep(1.0)

        # Show the reset initial state
        page.wait_for_selector("#checkout-view", state="visible")
        highlight_element(page, '[data-testid="empty-cart-message"]')
        time.sleep(2.0)

        print("[DEMO] Demonstration sequence complete. Closing page and saving video...")
        raw_video = page.video
        page.close()
        context.close()
        browser.close()

        # Final video path
        video_path = raw_video.path()
        print(f"[DEMO] Raw WebM video saved at: {video_path}")

        # Rename to a clean user-friendly filename
        clean_webm_path = VIDEOS_DIR / "fynd_mini_checkout_demo.webm"
        if clean_webm_path.exists():
            clean_webm_path.unlink()
        shutil.move(video_path, clean_webm_path)
        print(f"[DEMO] Clean WebM video available at: {clean_webm_path}")

        # If ffmpeg is available, also produce MP4 version
        clean_mp4_path = VIDEOS_DIR / "fynd_mini_checkout_demo.mp4"
        if FFMPEG_PATH.exists():
            print(f"[DEMO] Converting to MP4 using ffmpeg...")
            cmd = [
                str(FFMPEG_PATH),
                "-y",
                "-i", str(clean_webm_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "22",
                "-pix_fmt", "yuv420p",
                str(clean_mp4_path)
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"[DEMO] MP4 video converted successfully: {clean_mp4_path}")
            except Exception as e:
                print(f"[DEMO] MP4 conversion notice: {e}")

        return clean_webm_path, clean_mp4_path


if __name__ == "__main__":
    run_demonstration()
