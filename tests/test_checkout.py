"""
Fynd Mini Checkout - End-to-End Automated Browser Test Suite
Built with Python, Pytest, and Playwright.

Covers all mandatory test requirements, regression checks,
and edge-case validation scenarios.
"""

import re
import pytest
from playwright.sync_api import Page, expect
from pathlib import Path

# Paths for evidence
EVIDENCE_SCREENSHOTS = Path(__file__).resolve().parent.parent / "evidence" / "screenshots"


# ==============================================================================
# MANDATORY TESTS (As specified in Hackathon Requirements)
# ==============================================================================

@pytest.mark.mandatory
def test_successful_checkout(clean_page: Page):
    """
    TEST 1: Successful Checkout (Mandatory)
    - Start with a clean application state.
    - Add a product.
    - Enter a valid customer name.
    - Click Place Order.
    - Assert that the order confirmation is visible.
    - Assert that an order reference is displayed.
    - Assert that the correct order total is displayed.
    """
    page = clean_page

    # 1. Start with clean state
    expect(page.locator('[data-testid="empty-cart-message"]')).to_be_visible()
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹0")

    # 2. Add Wireless Headphones (₹1,499)
    page.locator('[data-testid="add-to-cart-headphones"]').click()

    # Verify item in cart and initial total
    expect(page.locator('[data-testid="cart-item-headphones"]')).to_be_visible()
    expect(page.locator('[data-testid="line-total-headphones"]')).to_have_text("₹1,499")
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹1,499")

    # 3. Enter a valid customer name
    customer_input = page.locator('[data-testid="customer-name-input"]')
    customer_input.fill("Aarav Mehta")

    # 4. Click Place Order
    place_order_btn = page.locator('[data-testid="place-order-btn"]')
    expect(place_order_btn).to_be_enabled()
    place_order_btn.click()

    # 5. Assert that order confirmation is visible
    confirmation_section = page.locator('[data-testid="order-confirmation"]')
    expect(confirmation_section).to_be_visible()

    # 6. Assert that an order reference is displayed
    order_ref = page.locator('[data-testid="order-reference"]')
    expect(order_ref).to_be_visible()
    # Verify order reference pattern (ORD-YYMMDD-XXXX-XXXX)
    expect(order_ref).to_have_text(re.compile(r"^ORD-\d{6}-\d+-[A-Z0-9]+$"))

    # 7. Assert that the correct order total is displayed
    confirmation_total = page.locator('[data-testid="confirmation-total"]')
    expect(confirmation_total).to_be_visible()
    expect(confirmation_total).to_have_text("₹1,499")

    # Customer Name assertion on receipt
    expect(page.locator('[data-testid="confirmation-customer-name"]')).to_have_text("Aarav Mehta")


@pytest.mark.mandatory
def test_missing_required_customer_name(clean_page: Page):
    """
    TEST 2: Missing Required Field (Mandatory)
    - Start with a clean application state.
    - Add a product.
    - Leave the customer name empty.
    - Click Place Order.
    - Assert that checkout is blocked.
    - Assert that the correct validation message is visible.
    - Assert that the cart contents are preserved.
    - Assert that no confirmation is displayed.
    """
    page = clean_page

    # 1. Start with clean state
    expect(page.locator('[data-testid="empty-cart-message"]')).to_be_visible()

    # 2. Add Smart Watch (₹2,499)
    page.locator('[data-testid="add-to-cart-smartwatch"]').click()
    expect(page.locator('[data-testid="cart-item-smartwatch"]')).to_be_visible()
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹2,499")

    # 3. Leave customer name input completely empty
    customer_input = page.locator('[data-testid="customer-name-input"]')
    expect(customer_input).to_have_value("")

    # 4. Click Place Order
    place_order_btn = page.locator('[data-testid="place-order-btn"]')
    place_order_btn.click()

    # 5. Assert that checkout is blocked and validation message is visible
    validation_container = page.locator('#validation-container')
    expect(validation_container).to_be_visible()
    
    validation_text = page.locator('[data-testid="validation-error"]')
    expect(validation_text).to_contain_text("Customer name is required")

    # Assert input field is highlighted with error state
    expect(customer_input).to_have_class(re.compile(r"input-error"))

    # 6. Assert that cart contents are preserved
    expect(page.locator('[data-testid="cart-item-smartwatch"]')).to_be_visible()
    expect(page.locator('[data-testid="qty-input-smartwatch"]')).to_have_value("1")
    expect(page.locator('[data-testid="line-total-smartwatch"]')).to_have_text("₹2,499")
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹2,499")

    # 7. Assert that no confirmation is displayed
    expect(page.locator('[data-testid="order-confirmation"]')).not_to_be_visible()
    expect(page.locator('#checkout-view')).to_be_visible()


@pytest.mark.mandatory
def test_quantity_changes_and_exact_total_calculation(clean_page: Page):
    """
    TEST 3: Quantity and Exact Total (Mandatory)
    - Start with a clean application state.
    - Add Wireless Headphones.
    - Change its quantity to 2.
    - Add Smart Watch.
    - Change its quantity to 3.
    - Assert the exact line totals:
        Wireless Headphones: ₹1,499 × 2 = ₹2,998
        Smart Watch: ₹2,499 × 3 = ₹7,497
    - Assert the exact order total:
        Final order total: ₹10,495
    """
    page = clean_page

    # 1. Add Wireless Headphones
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    expect(page.locator('[data-testid="cart-item-headphones"]')).to_be_visible()

    # 2. Change Headphones quantity to 2 using increment button
    page.locator('[data-testid="qty-increase-headphones"]').click()
    expect(page.locator('[data-testid="qty-input-headphones"]')).to_have_value("2")

    # 3. Add Smart Watch
    page.locator('[data-testid="add-to-cart-smartwatch"]').click()
    expect(page.locator('[data-testid="cart-item-smartwatch"]')).to_be_visible()

    # 4. Change Smart Watch quantity to 3 (click increment twice)
    page.locator('[data-testid="qty-increase-smartwatch"]').click()
    page.locator('[data-testid="qty-increase-smartwatch"]').click()
    expect(page.locator('[data-testid="qty-input-smartwatch"]')).to_have_value("3")

    # 5. Assert the exact line totals
    # Wireless Headphones: ₹1,499 × 2 = ₹2,998
    expect(page.locator('[data-testid="line-total-headphones"]')).to_have_text("₹2,998")

    # Smart Watch: ₹2,499 × 3 = ₹7,497
    expect(page.locator('[data-testid="line-total-smartwatch"]')).to_have_text("₹7,497")

    # 6. Assert the exact order total
    # Final order total: ₹10,495
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹10,495")
    expect(page.locator('[data-testid="summary-subtotal"]')).to_have_text("₹10,495")


# ==============================================================================
# ADDITIONAL EXTENDED TESTS (Robustness & Edge-Cases)
# ==============================================================================

@pytest.mark.extended
def test_empty_cart_checkout_validation(clean_page: Page):
    """
    Verifies that attempting to place an order with an empty cart is blocked,
    displays a descriptive validation error, and does not show order confirmation.
    """
    page = clean_page

    # Enter customer name with no products in cart
    customer_input = page.locator('[data-testid="customer-name-input"]')
    customer_input.fill("Priya Patel")

    # Click Place Order
    page.locator('[data-testid="place-order-btn"]').click()

    # Assert validation error is visible and mentions empty cart
    validation_container = page.locator('#validation-container')
    expect(validation_container).to_be_visible()
    expect(page.locator('[data-testid="validation-error"]')).to_contain_text("Your cart is empty")

    # Assert customer's entered name is preserved!
    expect(customer_input).to_have_value("Priya Patel")

    # Assert confirmation is NOT shown
    expect(page.locator('[data-testid="order-confirmation"]')).not_to_be_visible()


@pytest.mark.extended
def test_both_cart_and_name_empty_validation(clean_page: Page):
    """
    Verifies that when both cart is empty and name is omitted,
    the application displays clear validation errors for both requirements.
    """
    page = clean_page

    # Click Place Order directly from pristine state
    page.locator('[data-testid="place-order-btn"]').click()

    # Assert validation container displays both issues
    validation_container = page.locator('#validation-container')
    expect(validation_container).to_be_visible()
    
    validation_text = page.locator('[data-testid="validation-error"]').inner_text()
    assert "cart is empty" in validation_text.lower()
    assert "customer name is required" in validation_text.lower()


@pytest.mark.extended
def test_rapid_double_click_protection(clean_page: Page):
    """
    Verifies rapid double-click protection:
    Rapidly firing multiple clicks on Place Order does NOT result in duplicate
    order processing or corrupted state. The button is locked immediately upon first click.
    """
    page = clean_page

    # Add product and customer name
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    page.locator('[data-testid="customer-name-input"]').fill("Rohan Gupta")

    place_order_btn = page.locator('[data-testid="place-order-btn"]')

    # Perform rapid repeated clicks
    place_order_btn.click(click_count=2, delay=20)

    # Wait for confirmation screen
    confirmation_section = page.locator('[data-testid="order-confirmation"]')
    expect(confirmation_section).to_be_visible()

    # Confirm exactly ONE order reference is rendered
    order_refs = page.locator('[data-testid="order-reference"]')
    expect(order_refs).to_have_count(1)

    # Confirm order total is single correct amount
    expect(page.locator('[data-testid="confirmation-total"]')).to_have_text("₹1,499")

    # Confirm checkout button in background is disabled
    expect(place_order_btn).to_be_disabled()


@pytest.mark.extended
def test_product_removal_updates_cart_and_totals(clean_page: Page):
    """
    Verifies that removing a product from the cart completely deletes the item,
    recalculates totals, and returns to empty state if no other items exist.
    """
    page = clean_page

    # Add both products
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    page.locator('[data-testid="add-to-cart-smartwatch"]').click()

    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹3,998")

    # Remove Headphones
    page.locator('[data-testid="remove-item-headphones"]').click()

    # Assert Headphones row is gone
    expect(page.locator('[data-testid="cart-item-headphones"]')).not_to_be_visible()
    # Assert Smart Watch remains
    expect(page.locator('[data-testid="cart-item-smartwatch"]')).to_be_visible()
    # Assert total updated to only Smart Watch price
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹2,499")

    # Now remove Smart Watch
    page.locator('[data-testid="remove-item-smartwatch"]').click()

    # Assert empty cart message is visible again and total is ₹0
    expect(page.locator('[data-testid="empty-cart-message"]')).to_be_visible()
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹0")


@pytest.mark.extended
def test_quantity_cannot_become_negative_or_zero(clean_page: Page):
    """
    Verifies that quantity cannot be decreased below 1 using UI controls,
    and manual entry of negative or zero values is sanitized/reverted.
    """
    page = clean_page

    # Add product
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    qty_input = page.locator('[data-testid="qty-input-headphones"]')
    dec_btn = page.locator('[data-testid="qty-decrease-headphones"]')

    # Initial quantity is 1
    expect(qty_input).to_have_value("1")

    # Decrease button must be disabled when quantity is 1
    expect(dec_btn).to_be_disabled()

    # Increase quantity to 2
    page.locator('[data-testid="qty-increase-headphones"]').click()
    expect(qty_input).to_have_value("2")
    expect(dec_btn).to_be_enabled()

    # Decrease back to 1
    dec_btn.click()
    expect(qty_input).to_have_value("1")
    expect(dec_btn).to_be_disabled()

    # Attempt manual invalid input: fill "-5" and trigger change
    qty_input.fill("-5")
    qty_input.press("Enter")
    # Must revert back to valid minimum (1)
    expect(qty_input).to_have_value("1")
    expect(page.locator('[data-testid="line-total-headphones"]')).to_have_text("₹1,499")


@pytest.mark.extended
def test_start_new_order_resets_application_state(clean_page: Page):
    """
    Verifies that clicking 'Start New Order' on the confirmation screen
    cleanly resets cart, customer name, and UI state for the next purchase.
    """
    page = clean_page

    # Complete a standard checkout
    page.locator('[data-testid="add-to-cart-headphones"]').click()
    page.locator('[data-testid="customer-name-input"]').fill("Sneha Rao")
    page.locator('[data-testid="place-order-btn"]').click()

    # Confirm order confirmation is visible
    expect(page.locator('[data-testid="order-confirmation"]')).to_be_visible()

    # Click "Start New Order"
    page.locator('[data-testid="start-new-order-btn"]').click()

    # Assert checkout view is restored
    expect(page.locator('#checkout-view')).to_be_visible()
    expect(page.locator('[data-testid="order-confirmation"]')).not_to_be_visible()

    # Assert cart is empty
    expect(page.locator('[data-testid="empty-cart-message"]')).to_be_visible()
    expect(page.locator('[data-testid="order-total"]')).to_have_text("₹0")

    # Assert customer name input is cleared and enabled
    name_input = page.locator('[data-testid="customer-name-input"]')
    expect(name_input).to_have_value("")
    expect(name_input).to_be_enabled()
