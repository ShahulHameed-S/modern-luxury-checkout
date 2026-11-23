"""
Fynd Mini Checkout - Master Professional Demonstration & Video Recorder
Target duration: 85-90 seconds (Minimum required: 70s).
Records a clean desktop 1280x900 WebM (VP9) video of the 10-phase demonstration timeline.
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

FINAL_VIDEO_NAME = "fynd_mini_checkout_demo_final.webm"
FINAL_VIDEO_PATH = VIDEOS_DIR / FINAL_VIDEO_NAME

FFMPEG_PATH = Path(r"C:\Users\shahu\AppData\Local\ms-playwright\ffmpeg-1013\ffmpeg-win64.exe")

# Set stdout to UTF-8 for Windows console safety
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def inject_cursor_effects(page):
    """
    Injects a professional virtual mouse cursor ring with smooth click feedback
    so every mouse move, hover, and click is crystal clear to evaluators.
    """
    page.evaluate("""
        (() => {
            const cursor = document.createElement('div');
            cursor.id = 'demo-virtual-cursor';
            cursor.style.width = '22px';
            cursor.style.height = '22px';
            cursor.style.border = '2.5px solid #4f46e5';
            cursor.style.backgroundColor = 'rgba(79, 70, 229, 0.35)';
            cursor.style.borderRadius = '50%';
            cursor.style.position = 'fixed';
            cursor.style.pointerEvents = 'none';
            cursor.style.zIndex = '9999999';
            cursor.style.transition = 'transform 0.1s ease-out, background-color 0.15s ease, border-color 0.15s ease';
            cursor.style.transform = 'translate(-50%, -50%)';
            cursor.style.boxShadow = '0 0 10px rgba(79, 70, 229, 0.4)';
            cursor.style.display = 'none';
            document.body.appendChild(cursor);

            window.addEventListener('mousemove', (e) => {
                cursor.style.display = 'block';
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });

            window.addEventListener('mousedown', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(0.65)';
                cursor.style.backgroundColor = 'rgba(220, 38, 38, 0.6)';
                cursor.style.borderColor = '#dc2626';
            });

            window.addEventListener('mouseup', (e) => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
                cursor.style.backgroundColor = 'rgba(79, 70, 229, 0.35)';
                cursor.style.borderColor = '#4f46e5';
            });
        })();
    """)


def smooth_move(page, selector, steps=12):
    """Smoothly moves the virtual mouse to the center of a given selector."""
    try:
        loc = page.locator(selector).first
        loc.scroll_into_view_if_needed()
        box = loc.bounding_box()
        if box:
            center_x = box["x"] + box["width"] / 2
            center_y = box["y"] + box["height"] / 2
            page.mouse.move(center_x, center_y, steps=steps)
            return box
    except Exception as e:
        print(f"Move notice for {selector}: {e}")
    return None


def run_master_demonstration():
    app_url = "http://localhost:8000/index.html"
    print(f"[RECORDER] Launching Master Demonstration on {app_url}...")
    start_time = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-web-security"]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": 1280, "height": 900}
        )

        page = context.new_page()

        # -------------------------------------------------------------
        # TIMELINE 00:00 - 00:09 (9s): Homepage, Products & Honest Demo Badge
        # -------------------------------------------------------------
        print("[00:00 - 00:09] Phase 1: Showing homepage, product cards, prices, and demo badge...")
        page.goto(app_url)
        page.wait_for_selector("#checkout-view", state="visible")
        inject_cursor_effects(page)
        time.sleep(0.8)

        # Show header & honest demo badge
        smooth_move(page, ".brand", steps=10)
        time.sleep(1.2)
        smooth_move(page, ".demo-badge", steps=10)
        time.sleep(1.6)

        # Inspect Wireless Headphones (₹1,499)
        smooth_move(page, '[data-testid="product-card-headphones"]', steps=12)
        time.sleep(2.0)

        # Inspect Smart Watch (₹2,499)
        smooth_move(page, '[data-testid="product-card-smartwatch"]', steps=12)
        time.sleep(2.0)

        # -------------------------------------------------------------
        # TIMELINE 00:09 - 00:19 (10s): Add both products to cart
        # -------------------------------------------------------------
        print("[00:09 - 00:19] Phase 2: Adding Wireless Headphones and Smart Watch to cart...")
        smooth_move(page, '[data-testid="add-to-cart-headphones"]', steps=12)
        time.sleep(0.8)
        page.locator('[data-testid="add-to-cart-headphones"]').click()
        time.sleep(0.8)
        # Highlight updated cart
        smooth_move(page, '[data-testid="cart-item-headphones"]', steps=10)
        time.sleep(1.8)

        # Add Smart Watch
        smooth_move(page, '[data-testid="add-to-cart-smartwatch"]', steps=12)
        time.sleep(0.8)
        page.locator('[data-testid="add-to-cart-smartwatch"]').click()
        time.sleep(0.8)
        smooth_move(page, '[data-testid="cart-item-smartwatch"]', steps=10)
        time.sleep(2.5)

        # -------------------------------------------------------------
        # TIMELINE 00:19 - 00:30 (11s): Demonstrate quantity increase & decrease
        # -------------------------------------------------------------
        print("[00:19 - 00:30] Phase 3: Demonstrating quantity increase and decrease...")
        # Increase Headphones to 2
        smooth_move(page, '[data-testid="qty-increase-headphones"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-increase-headphones"]').click()
        time.sleep(0.4)
        smooth_move(page, '[data-testid="line-total-headphones"]', steps=8)
        time.sleep(1.6)

        # Decrease Headphones back to 1
        smooth_move(page, '[data-testid="qty-decrease-headphones"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-decrease-headphones"]').click()
        time.sleep(0.4)
        smooth_move(page, '[data-testid="line-total-headphones"]', steps=8)
        time.sleep(1.6)

        # Increase Smart Watch to 2
        smooth_move(page, '[data-testid="qty-increase-smartwatch"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-increase-smartwatch"]').click()
        time.sleep(0.4)
        smooth_move(page, '[data-testid="line-total-smartwatch"]', steps=8)
        time.sleep(1.6)

        # Decrease Smart Watch back to 1
        smooth_move(page, '[data-testid="qty-decrease-smartwatch"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-decrease-smartwatch"]').click()
        time.sleep(0.4)
        smooth_move(page, '[data-testid="line-total-smartwatch"]', steps=8)
        time.sleep(1.6)

        # -------------------------------------------------------------
        # TIMELINE 00:30 - 00:38 (8s): Remove Smart Watch and add it back
        # -------------------------------------------------------------
        print("[00:30 - 00:38] Phase 4: Removing Smart Watch and re-adding...")
        smooth_move(page, '[data-testid="remove-item-smartwatch"]', steps=10)
        time.sleep(0.8)
        page.locator('[data-testid="remove-item-smartwatch"]').click()
        time.sleep(2.0)

        # Re-add Smart Watch
        smooth_move(page, '[data-testid="add-to-cart-smartwatch"]', steps=12)
        time.sleep(0.8)
        page.locator('[data-testid="add-to-cart-smartwatch"]').click()
        time.sleep(2.0)

        # -------------------------------------------------------------
        # TIMELINE 00:38 - 00:48 (10s): Attempt checkout with empty name & show validation
        # -------------------------------------------------------------
        print("[00:38 - 00:48] Phase 5: Demonstrating empty customer name validation...")
        smooth_move(page, '[data-testid="place-order-btn"]', steps=12)
        time.sleep(0.8)
        page.locator('[data-testid="place-order-btn"]').click()
        time.sleep(0.8)

        # Highlight error notification
        smooth_move(page, '#validation-container', steps=12)
        time.sleep(3.0)

        # Highlight red error focus ring on input
        smooth_move(page, '[data-testid="customer-name-input"]', steps=10)
        time.sleep(2.0)

        # Hover over preserved cart items
        smooth_move(page, '#cart-items-wrapper', steps=10)
        time.sleep(1.6)

        # -------------------------------------------------------------
        # TIMELINE 00:48 - 00:56 (8s): Enter customer name: Demo User
        # -------------------------------------------------------------
        print("[00:48 - 00:56] Phase 6: Entering customer name: 'Demo User'...")
        name_input = page.locator('[data-testid="customer-name-input"]')
        smooth_move(page, '[data-testid="customer-name-input"]', steps=8)
        time.sleep(0.6)
        name_input.click()
        time.sleep(0.4)
        # Type naturally at ~120ms per char
        name_input.type("Demo User", delay=120)
        time.sleep(0.8)
        smooth_move(page, '#customer-name-help', steps=8)
        time.sleep(3.2)

        # -------------------------------------------------------------
        # TIMELINE 00:56 - 01:06 (10s): Set Headphones: 2, Smart Watch: 3
        # -------------------------------------------------------------
        print("[00:56 - 01:06] Phase 7: Setting quantities (Headphones: 2, Smart Watch: 3)...")
        # Increase Headphones to 2
        smooth_move(page, '[data-testid="qty-increase-headphones"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-increase-headphones"]').click()
        time.sleep(2.0)

        # Increase Smart Watch to 2, then 3
        smooth_move(page, '[data-testid="qty-increase-smartwatch"]', steps=10)
        time.sleep(0.6)
        page.locator('[data-testid="qty-increase-smartwatch"]').click()
        time.sleep(1.2)
        page.locator('[data-testid="qty-increase-smartwatch"]').click()
        time.sleep(2.8)

        # -------------------------------------------------------------
        # TIMELINE 01:06 - 01:13 (7s): Clearly show the ₹10,495 grand total
        # -------------------------------------------------------------
        print("[01:06 - 01:13] Phase 8: Highlighting exact calculation and ₹10,495 total...")
        # Hover over Headphones line: ₹2,998
        smooth_move(page, '[data-testid="line-total-headphones"]', steps=8)
        time.sleep(1.8)

        # Hover over Smart Watch line: ₹7,497
        smooth_move(page, '[data-testid="line-total-smartwatch"]', steps=8)
        time.sleep(1.8)

        # Hover over Grand Total: ₹10,495
        smooth_move(page, '[data-testid="order-total"]', steps=10)
        time.sleep(2.5)

        # -------------------------------------------------------------
        # TIMELINE 01:13 - 01:20 (7s): Place order & show confirmation
        # -------------------------------------------------------------
        print("[01:13 - 01:20] Phase 9: Placing order with submission lock...")
        smooth_move(page, '[data-testid="place-order-btn"]', steps=12)
        time.sleep(0.8)
        page.locator('[data-testid="place-order-btn"]').click()
        time.sleep(1.2)

        # Confirmation view rendered
        page.wait_for_selector('[data-testid="order-confirmation"]', state="visible")
        smooth_move(page, '.confirmation-header', steps=12)
        time.sleep(3.8)

        # -------------------------------------------------------------
        # TIMELINE 01:20 - 01:28 (8s): Receipt inspection & Start New Order
        # -------------------------------------------------------------
        print("[01:20 - 01:28] Phase 10: Keeping receipt visible and demonstrating Start New Order...")
        # Order reference
        smooth_move(page, '[data-testid="order-reference"]', steps=10)
        time.sleep(1.6)

        # Customer name
        smooth_move(page, '[data-testid="confirmation-customer-name"]', steps=8)
        time.sleep(1.2)

        # Total paid (₹10,495)
        smooth_move(page, '[data-testid="confirmation-total"]', steps=8)
        time.sleep(1.6)

        # Itemized breakdown
        smooth_move(page, '#confirm-items-list', steps=10)
        time.sleep(1.6)

        # Click Start New Order
        smooth_move(page, '[data-testid="start-new-order-btn"]', steps=12)
        time.sleep(1.0)
        page.locator('[data-testid="start-new-order-btn"]').click()
        time.sleep(1.2)

        # Show the reset store state
        page.wait_for_selector("#checkout-view", state="visible")
        smooth_move(page, '[data-testid="empty-cart-message"]', steps=10)
        time.sleep(2.0)

        # Conclude recording
        print("[RECORDER] Master demonstration actions completed.")
        raw_video = page.video
        page.close()
        context.close()
        browser.close()

        raw_path = raw_video.path()
        elapsed = time.time() - start_time
        print(f"[RECORDER] Elapsed session time: {elapsed:.2f}s")
        print(f"[RECORDER] Raw video saved at: {raw_path}")

        # Save to FINAL_VIDEO_PATH
        if FINAL_VIDEO_PATH.exists():
            FINAL_VIDEO_PATH.unlink()
        shutil.move(raw_path, FINAL_VIDEO_PATH)
        print(f"[RECORDER] Master demonstration video saved successfully at: {FINAL_VIDEO_PATH}")

        return FINAL_VIDEO_PATH


if __name__ == "__main__":
    run_master_demonstration()
