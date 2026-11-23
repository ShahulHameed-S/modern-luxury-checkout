from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://localhost:8000/index.html')
    
    # 1. Add item & checkout
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    page.locator('[data-testid="customer-name-input"]').fill("Demo User")
    page.locator('[data-testid="place-order-btn"]').click()
    page.wait_for_selector('[data-testid="order-confirmation"]', state='visible')
    print("Checkout 1 complete")
    
    # 2. Start new order
    page.locator('[data-testid="start-new-order-btn"]').click()
    page.wait_for_selector('#checkout-view', state='visible')
    print("Reset complete")
    
    # 3. Enter name and click place order on empty cart
    page.locator('[data-testid="customer-name-input"]').fill("Demo User")
    page.locator('[data-testid="place-order-btn"]').click()
    page.wait_for_selector('#validation-container', state='visible')
    text = page.locator('#validation-container').inner_text()
    print("Validation container text:", repr(text))
    b.close()
