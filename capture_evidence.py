"""
Script to execute browser-driven manual test scenarios and capture
genuine high-resolution screenshot evidence for TEST_RESULTS.md and documentation.
"""

import http.server
import socket
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent
SCREENSHOTS_DIR = WORKSPACE_ROOT / "evidence" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_ROOT), **kwargs)

    def log_message(self, format, *args):
        pass


def capture_evidence():
    port = find_free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}"
    print(f"Server started at {base_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # EVIDENCE 1: Pristine Landing Page / Initial State
        # -------------------------------------------------------------
        context1 = browser.new_context(viewport={"width": 1280, "height": 840})
        page1 = context1.new_page()
        page1.goto(f"{base_url}/index.html")
        page1.wait_for_selector("#checkout-view")
        shot1 = SCREENSHOTS_DIR / "01_initial_state_landing.png"
        page1.screenshot(path=str(shot1), full_page=True)
        print(f"Captured: {shot1.name}")

        # -------------------------------------------------------------
        # EVIDENCE 2: Manual Test Case TC-MAN-01 (Empty Cart Validation)
        # -------------------------------------------------------------
        # Step: Enter customer name "Neha Varma" and click Place Order with empty cart
        page1.locator('[data-testid="customer-name-input"]').fill("Neha Varma")
        page1.locator('[data-testid="place-order-btn"]').click()
        page1.wait_for_selector("#validation-container", state="visible")
        page1.evaluate("window.scrollTo(0, 0)")
        shot2 = SCREENSHOTS_DIR / "02_manual_tc01_empty_cart_validation.png"
        page1.screenshot(path=str(shot2), full_page=True)
        print(f"Captured: {shot2.name}")

        # -------------------------------------------------------------
        # EVIDENCE 3: Missing Customer Name Validation (TC-MAN-02 / TEST 2)
        # -------------------------------------------------------------
        context2 = browser.new_context(viewport={"width": 1280, "height": 840})
        page2 = context2.new_page()
        page2.goto(f"{base_url}/index.html")
        page2.locator('[data-testid="add-to-cart-smartwatch"]').click()
        page2.locator('[data-testid="place-order-btn"]').click()
        page2.wait_for_selector("#validation-container", state="visible")
        page2.evaluate("window.scrollTo(0, 0)")
        shot3 = SCREENSHOTS_DIR / "03_missing_customer_name_validation.png"
        page2.screenshot(path=str(shot3), full_page=True)
        print(f"Captured: {shot3.name}")

        # -------------------------------------------------------------
        # EVIDENCE 4: Quantity and Exact Totals Calculation (TEST 3)
        # -------------------------------------------------------------
        context3 = browser.new_context(viewport={"width": 1280, "height": 840})
        page3 = context3.new_page()
        page3.goto(f"{base_url}/index.html")
        # Add Headphones, qty 2
        page3.locator('[data-testid="add-to-cart-headphones"]').click()
        page3.locator('[data-testid="qty-increase-headphones"]').click()
        # Add Smart Watch, qty 3
        page3.locator('[data-testid="add-to-cart-smartwatch"]').click()
        page3.locator('[data-testid="qty-increase-smartwatch"]').click()
        page3.locator('[data-testid="qty-increase-smartwatch"]').click()
        page3.locator('[data-testid="customer-name-input"]').fill("Vikram Malhotra")
        page3.evaluate("window.scrollTo(0, 0)")
        shot4 = SCREENSHOTS_DIR / "04_quantity_exact_totals_calculation.png"
        page3.screenshot(path=str(shot4), full_page=True)
        print(f"Captured: {shot4.name}")

        # -------------------------------------------------------------
        # EVIDENCE 5: Manual Test Case TC-MAN-02 (Rapid Double Click & Submission Lock)
        # -------------------------------------------------------------
        # Click Place Order rapidly
        page3.locator('[data-testid="place-order-btn"]').click(click_count=2, delay=20)
        page3.wait_for_selector('[data-testid="order-confirmation"]', state="visible")
        page3.evaluate("window.scrollTo(0, 0)")
        shot5 = SCREENSHOTS_DIR / "05_order_confirmation_success.png"
        page3.screenshot(path=str(shot5), full_page=True)
        print(f"Captured: {shot5.name}")

        # -------------------------------------------------------------
        # EVIDENCE 6: Mobile Responsive Viewport (390x844 - iPhone 14)
        # -------------------------------------------------------------
        context_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        page_mobile = context_mobile.new_page()
        page_mobile.goto(f"{base_url}/index.html")
        page_mobile.locator('[data-testid="add-to-cart-headphones"]').click()
        page_mobile.evaluate("window.scrollTo(0, 0)")
        page_mobile.evaluate("document.querySelector('.app-header').style.position = 'relative'")
        shot6 = SCREENSHOTS_DIR / "06_mobile_responsive_view.png"
        page_mobile.screenshot(path=str(shot6), full_page=True)
        print(f"Captured: {shot6.name}")

        browser.close()

    server.shutdown()
    server.server_close()
    print("Evidence capture completed successfully.")


if __name__ == "__main__":
    capture_evidence()
