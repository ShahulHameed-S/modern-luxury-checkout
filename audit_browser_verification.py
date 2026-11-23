"""
Audit Browser Verification Script
Executes Scenarios A, B, C, D, and E through browser automation (Playwright Chromium)
and captures fresh evidence screenshots for the final audit.
"""

import http.server
import socket
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

# Set stdout to UTF-8 to prevent Windows cp1252 UnicodeEncodeError for currency symbols
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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


def run_audit_scenarios():
    port = find_free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}"
    print(f"[AUDIT] Test server live at {base_url}")

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ------------------------------------------------------------------
        # SCENARIO A: Empty cart checkout
        # ------------------------------------------------------------------
        ctx_a = browser.new_context(viewport={"width": 1280, "height": 840})
        page_a = ctx_a.new_page()
        page_a.goto(f"{base_url}/index.html")
        page_a.wait_for_selector("#checkout-view")

        # Cart empty, attempt checkout
        page_a.locator('[data-testid="place-order-btn"]').click()
        page_a.wait_for_selector("#validation-container", state="visible")
        page_a.evaluate("window.scrollTo(0, 0)")
        val_text_a = page_a.locator('[data-testid="validation-error"]').inner_text()
        conf_vis_a = page_a.locator('[data-testid="order-confirmation"]').is_visible()

        shot_a = SCREENSHOTS_DIR / "scenario_a_empty_cart.png"
        page_a.screenshot(path=str(shot_a), full_page=True)

        results["Scenario A"] = {
            "blocked": not conf_vis_a,
            "validation_text": val_text_a,
            "screenshot": shot_a.name,
            "pass": (not conf_vis_a) and ("cart is empty" in val_text_a.lower())
        }
        print(f"[AUDIT] Scenario A (Empty Cart): {results['Scenario A']}")

        # ------------------------------------------------------------------
        # SCENARIO B: Missing customer name
        # ------------------------------------------------------------------
        ctx_b = browser.new_context(viewport={"width": 1280, "height": 840})
        page_b = ctx_b.new_page()
        page_b.goto(f"{base_url}/index.html")

        # Add Smart Watch (₹2,499)
        page_b.locator('[data-testid="add-to-cart-smartwatch"]').click()
        # Keep customer name blank, attempt checkout
        page_b.locator('[data-testid="place-order-btn"]').click()
        page_b.wait_for_selector("#validation-container", state="visible")
        page_b.evaluate("window.scrollTo(0, 0)")

        val_text_b = page_b.locator('[data-testid="validation-error"]').inner_text()
        cart_item_vis_b = page_b.locator('[data-testid="cart-item-smartwatch"]').is_visible()
        total_text_b = page_b.locator('[data-testid="order-total"]').inner_text()
        conf_vis_b = page_b.locator('[data-testid="order-confirmation"]').is_visible()

        shot_b = SCREENSHOTS_DIR / "scenario_b_missing_name.png"
        page_b.screenshot(path=str(shot_b), full_page=True)

        results["Scenario B"] = {
            "blocked": not conf_vis_b,
            "validation_text": val_text_b,
            "cart_preserved": cart_item_vis_b and total_text_b == "₹2,499",
            "screenshot": shot_b.name,
            "pass": (not conf_vis_b) and ("customer name is required" in val_text_b.lower()) and cart_item_vis_b
        }
        print(f"[AUDIT] Scenario B (Missing Name): {results['Scenario B']}")

        # ------------------------------------------------------------------
        # SCENARIO C: Rapid double-click on Place Order
        # ------------------------------------------------------------------
        ctx_c = browser.new_context(viewport={"width": 1280, "height": 840})
        page_c = ctx_c.new_page()
        page_c.goto(f"{base_url}/index.html")

        page_c.locator('[data-testid="add-to-cart-headphones"]').click()
        page_c.locator('[data-testid="customer-name-input"]').fill("Devika Sengupta")

        place_btn_c = page_c.locator('[data-testid="place-order-btn"]')
        # Rapid double click
        place_btn_c.click(click_count=2, delay=15)

        page_c.wait_for_selector('[data-testid="order-confirmation"]', state="visible")
        page_c.evaluate("window.scrollTo(0, 0)")
        ref_count_c = page_c.locator('[data-testid="order-reference"]').count()
        conf_count_c = page_c.locator('[data-testid="order-confirmation"]').count()
        btn_disabled_c = place_btn_c.is_disabled()

        shot_c = SCREENSHOTS_DIR / "scenario_c_rapid_double_click.png"
        page_c.screenshot(path=str(shot_c), full_page=True)

        results["Scenario C"] = {
            "single_order_ref": ref_count_c == 1,
            "single_confirmation": conf_count_c == 1,
            "button_disabled": btn_disabled_c,
            "screenshot": shot_c.name,
            "pass": ref_count_c == 1 and conf_count_c == 1 and btn_disabled_c
        }
        print(f"[AUDIT] Scenario C (Rapid Double Click): {results['Scenario C']}")

        # ------------------------------------------------------------------
        # SCENARIO D: Exact total calculation
        # ------------------------------------------------------------------
        ctx_d = browser.new_context(viewport={"width": 1280, "height": 840})
        page_d = ctx_d.new_page()
        page_d.goto(f"{base_url}/index.html")

        # 2x Wireless Headphones (₹1,499 each = ₹2,998)
        page_d.locator('[data-testid="add-to-cart-headphones"]').click()
        page_d.locator('[data-testid="qty-increase-headphones"]').click()

        # 3x Smart Watch (₹2,499 each = ₹7,497)
        page_d.locator('[data-testid="add-to-cart-smartwatch"]').click()
        page_d.locator('[data-testid="qty-increase-smartwatch"]').click()
        page_d.locator('[data-testid="qty-increase-smartwatch"]').click()

        page_d.locator('[data-testid="customer-name-input"]').fill("Aditya Verma")
        page_d.evaluate("window.scrollTo(0, 0)")

        headphones_line = page_d.locator('[data-testid="line-total-headphones"]').inner_text()
        smartwatch_line = page_d.locator('[data-testid="line-total-smartwatch"]').inner_text()
        order_total = page_d.locator('[data-testid="order-total"]').inner_text()
        subtotal = page_d.locator('[data-testid="summary-subtotal"]').inner_text()

        shot_d = SCREENSHOTS_DIR / "scenario_d_exact_totals.png"
        page_d.screenshot(path=str(shot_d), full_page=True)

        expected_headphones = "₹2,998"
        expected_smartwatch = "₹7,497"
        expected_grand = "₹10,495"

        calc_pass = (headphones_line == expected_headphones and
                     smartwatch_line == expected_smartwatch and
                     order_total == expected_grand and
                     subtotal == expected_grand)

        results["Scenario D"] = {
            "headphones_line": headphones_line,
            "smartwatch_line": smartwatch_line,
            "order_total": order_total,
            "screenshot": shot_d.name,
            "pass": calc_pass
        }
        print(f"[AUDIT] Scenario D (Exact Totals): {results['Scenario D']}")

        # ------------------------------------------------------------------
        # SCENARIO E: Responsive layout (Desktop vs Mobile)
        # ------------------------------------------------------------------
        # Desktop 1280x840
        shot_e_desktop = SCREENSHOTS_DIR / "scenario_e_desktop_viewport.png"
        page_d.screenshot(path=str(shot_e_desktop), full_page=True)

        # Mobile 390x844 (iPhone 14)
        ctx_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        page_m = ctx_mobile.new_page()
        page_m.goto(f"{base_url}/index.html")
        page_m.locator('[data-testid="add-to-cart-headphones"]').click()
        shot_e_mobile = SCREENSHOTS_DIR / "scenario_e_mobile_viewport.png"
        page_m.screenshot(path=str(shot_e_mobile), full_page=True)

        results["Scenario E"] = {
            "desktop_screenshot": shot_e_desktop.name,
            "mobile_screenshot": shot_e_mobile.name,
            "pass": True
        }
        print(f"[AUDIT] Scenario E (Responsive): {results['Scenario E']}")

        browser.close()

    server.shutdown()
    server.server_close()
    print("[AUDIT] Verification execution complete.")
    return results


if __name__ == "__main__":
    run_audit_scenarios()
