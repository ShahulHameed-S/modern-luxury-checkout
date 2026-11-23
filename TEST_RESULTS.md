# Test Results Report: Fynd Mini Checkout Suite

**Execution Timestamp:** 2026-11-23 12:23:38 IST  
**Environment:** Windows 11 (win32), Python 3.11.2 / 3.14.0, Pytest 9.2.0, Playwright 1.65.2  
**Browser Engine:** Chromium Headless (CFT 159.0.8154.6)  
**Execution Target:** Mini Checkout Application (`http://127.0.0.1:<ephemeral-port>/index.html`)  

---

## 1. Executive Summary

| Category | Total | Passed | Failed | Skipped | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mandatory Automated Pytest Tests** | 3 | 3 | 0 | 0 | **100%** |
| **Extended Automated Pytest Tests** | 6 | 6 | 0 | 0 | **100%** |
| **Total Automated Pytest Suite** | **9** | **9** | **0** | **0** | **100%** |
| **Browser-Automated Verification Scenarios** | 5 | 5 | 0 | 0 | **100%** |

**Overall Status:** **ALL TESTS PASSED (GREEN)**

---

## 2. Automated Test Suite Execution Details

All automated tests were executed using Pytest and Playwright in isolated browser contexts. The generated JUnit XML report is archived at `evidence/test-results/junit.xml`.

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\shahul\Desktop\fyd
configfile: pytest.ini
testpaths: tests
plugins: playwright-0.10.0
collecting ... collected 9 items

tests/test_checkout.py::test_successful_checkout[chromium] PASSED        [ 11%]
tests/test_checkout.py::test_missing_required_customer_name[chromium] PASSED [ 22%]
tests/test_checkout.py::test_quantity_changes_and_exact_total_calculation[chromium] PASSED [ 33%]
tests/test_checkout.py::test_empty_cart_checkout_validation[chromium] PASSED [ 44%]
tests/test_checkout.py::test_both_cart_and_name_empty_validation[chromium] PASSED [ 55%]
tests/test_checkout.py::test_rapid_double_click_protection[chromium] PASSED [ 66%]
tests/test_checkout.py::test_product_removal_updates_cart_and_totals[chromium] PASSED [ 77%]
tests/test_checkout.py::test_quantity_cannot_become_negative_or_zero[chromium] PASSED [ 88%]
tests/test_checkout.py::test_start_new_order_resets_application_state[chromium] PASSED [100%]

-- generated xml file: C:\shahul\Desktop\fyd\evidence\test-results\junit.xml --
============================= 9 passed in 10.83s ==============================
```

### Detailed Automated Test Breakdown:

#### 1. `test_successful_checkout` (MANDATORY TEST 1)
- **Status:** `PASSED`
- **Duration:** ~1.2s
- **Verified Requirements:**
  - Starts with empty cart state (`0 items`, `₹0`).
  - Adds Wireless Headphones (`₹1,499`).
  - Fills valid customer name (`"Aarav Mehta"`).
  - Triggers Place Order.
  - Verifies order confirmation card is visible.
  - Verifies unique order reference generated matching `^ORD-\d{6}-\d+-[A-Z0-9]+$`.
  - Verifies exact confirmation total is `₹1,499`.
  - Verifies receipt customer name matches `"Aarav Mehta"`.

#### 2. `test_missing_required_customer_name` (MANDATORY TEST 2)
- **Status:** `PASSED`
- **Duration:** ~0.9s
- **Verified Requirements:**
  - Adds Smart Watch (`₹2,499`).
  - Customer name left empty.
  - Triggers Place Order.
  - Checkout is strictly blocked.
  - Validation message `"Customer name is required..."` is displayed in accessible alert container.
  - Red border focus class (`input-error`) applied to customer name input.
  - Smart Watch cart line item and order total (`₹2,499`) are **completely preserved**.
  - No order confirmation is shown.

#### 3. `test_quantity_changes_and_exact_total_calculation` (MANDATORY TEST 3)
- **Status:** `PASSED`
- **Duration:** ~1.3s
- **Verified Requirements:**
  - Adds Wireless Headphones (`₹1,499`); increments quantity to `2`.
  - Line total for Headphones: `₹1,499 × 2 = ₹2,998` (Exact).
  - Adds Smart Watch (`₹2,499`); increments quantity to `3`.
  - Line total for Smart Watch: `₹2,499 × 3 = ₹7,497` (Exact).
  - Grand total: `₹2,998 + ₹7,497 = ₹10,495` (Exact integer arithmetic).
  - Order summary subtotal and checkout grand total are synchronized.

#### 4. `test_empty_cart_checkout_validation`
- **Status:** `PASSED`
- **Duration:** ~0.8s
- **Verified Requirements:**
  - Enters customer name `"Priya Patel"`.
  - Attempts Place Order with empty cart.
  - Checkout is blocked; alert banner displays `"Your cart is empty..."`.
  - Customer name `"Priya Patel"` is **preserved** in the input field.

#### 5. `test_both_cart_and_name_empty_validation`
- **Status:** `PASSED`
- **Duration:** ~0.7s
- **Verified Requirements:**
  - Direct click on Place Order from pristine state.
  - Application renders compound validation error notifying user of both empty cart and missing customer name.

#### 6. `test_rapid_double_click_protection`
- **Status:** `PASSED`
- **Duration:** ~1.4s
- **Verified Requirements:**
  - Cart loaded with items and customer name provided.
  - High-frequency consecutive clicks (`click_count=2`, delay `20ms`) dispatched on "Place Order".
  - Synchronous submission lock engages instantly.
  - Exactly one order confirmation rendered.
  - Order reference count in DOM equals `1`.
  - Total is uncorrupted.
  - Place Order button is disabled.

#### 7. `test_product_removal_updates_cart_and_totals`
- **Status:** `PASSED`
- **Duration:** ~1.1s
- **Verified Requirements:**
  - Adds both products.
  - Removes Wireless Headphones; Smart Watch remains with updated total (`₹2,499`).
  - Removes Smart Watch; empty cart placeholder re-appears and total resets to `₹0`.

#### 8. `test_quantity_cannot_become_negative_or_zero`
- **Status:** `PASSED`
- **Duration:** ~1.0s
- **Verified Requirements:**
  - When quantity is 1, decrement button is disabled (`disabled="true"`).
  - Incrementing to 2 enables decrement button.
  - Direct keyboard entry of negative values (`-5`) or zero is automatically sanitized back to minimum quantity `1`.

#### 9. `test_start_new_order_resets_application_state`
- **Status:** `PASSED`
- **Duration:** ~1.2s
- **Verified Requirements:**
  - After successful order placement, clicking "Start New Order" cleanly restores the store layout, clears the cart, clears customer name input, re-enables controls, and hides confirmation.

---

## 3. Browser-Automated Verification Scenarios & Evidence

In accordance with strict SDET reporting standards, browser interactions executed programmatically via Playwright are explicitly categorized as **Browser-Automated Verification**. Fresh screenshots were captured during the audit execution of `audit_browser_verification.py`.

| Scenario ID | Scenario Description | Expected Outcome | Actual Result | Status | Screenshot Evidence |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Scenario A** | Empty cart checkout attempt | Validation error displayed, entered customer name preserved, checkout blocked | Error banner displayed, name preserved, order blocked | **PASS** | `evidence/screenshots/scenario_a_empty_cart.png` |
| **Scenario B** | Missing required customer name | Validation error displayed, input highlighted in red, cart preserved | Input outlined in red, alert shown, cart preserved | **PASS** | `evidence/screenshots/scenario_b_missing_name.png` |
| **Scenario C** | Rapid double-click on Place Order | Synchronous lock prevents duplicate submission, single order confirmation | Submission lock locked immediately, single order confirmed | **PASS** | `evidence/screenshots/scenario_c_rapid_double_click.png` |
| **Scenario D** | Quantity calculation (2x Headphones + 3x Watch) | Headphones = ₹2,998; Watch = ₹7,497; Grand Total = ₹10,495 | Exact totals displayed, integer math verified | **PASS** | `evidence/screenshots/scenario_d_exact_totals.png` |
| **Scenario E** | Viewport responsiveness (Desktop & Mobile) | Layout adapts cleanly; mobile stacks into single column, touch targets clear | Verified at 1280x840 (desktop) and 390x844 (mobile) | **PASS** | `evidence/screenshots/scenario_e_desktop_viewport.png`, `evidence/screenshots/scenario_e_mobile_viewport.png` |

---

## 4. Defect Log

| Defect ID | Description | Severity | Steps to Reproduce | Resolution |
| :--- | :--- | :---: | :--- | :--- |
| *None* | **Zero Defects Found** | N/A | Full regression test suite passed with 100% assertion adherence. | All edge cases (rapid click, negative quantity, empty cart, input preservation) were built with defensive code upfront. |

---

## 5. SDET Quality Assessment & Sign-Off

1. **State Preservation:** When validation errors trigger, neither customer name nor cart line items are cleared. The user does not lose work.
2. **Double Submission Protection:** Both synchronous boolean locking (`submissionLockAcquired`) and DOM button disabling (`disabled = true`) are enforced before any asynchronous execution occurs.
3. **Monetary Precision:** The domain model restricts all monetary values to whole integer Rupees (`1499`, `2499`) and quantities to positive integers (`1, 2, ...`). Multiplying and summing whole integers guarantees zero floating-point precision drift.
4. **Accessibility:** WAI-ARIA roles (`role="alert"`, `aria-live="assertive"`, `aria-required="true"`) are implemented for assistive technology compatibility.
