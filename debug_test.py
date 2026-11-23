from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto('http://localhost:8000/index.html')
    page.locator('[data-testid="customer-name-input"]').fill('Demo User')
    page.locator('[data-testid="place-order-btn"]').click()
    page.wait_for_selector('#validation-container', state='visible')
    box = page.locator('#validation-container').bounding_box()
    display = page.eval_on_selector('#validation-container', 'el => window.getComputedStyle(el).display')
    text = page.locator('#validation-container').inner_text()
    print('Box:', box)
    print('Display:', display)
    print('Text:', repr(text))
    page.screenshot(path='evidence/screenshots/debug_empty_cart_error.png')
    b.close()
