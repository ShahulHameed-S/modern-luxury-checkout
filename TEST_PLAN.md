# Test Plan: Fynd Mini Checkout & Browser Test Suite

## 1. Overview & Objective
This test plan defines the testing strategy, risk analysis, browser verification scenarios, and automation coverage for the **Fynd Mini Checkout** application. The objective is to verify that the checkout flow is robust, resilient to user errors and race conditions, handles integer monetary calculations accurately, and delivers an intuitive, accessible customer experience.

---

## 2. Risk Assessment & Prioritization

| Risk ID | Risk Description | Likelihood | Impact | Severity | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Duplicate Order Confirmation / Double Submission**: Rapid or double clicking "Place Order" leads to multiple order charges or duplicated order records. | High | Critical | **P0** | Immediate synchronous UI submission lock, disabling button, state flag check, and automated rapid-click testing. |
| **RSK-02** | **Floating Point Calculation Inaccuracy**: Using standard floating point arithmetic causes precision drift in price totals. | High | Critical | **P0** | Domain model represents all monetary amounts as whole integer Rupees (1499, 2499) and quantities as positive integers, completely avoiding fractional float operations. |
| **RSK-03** | **Empty Cart Checkout**: Users attempting to order with 0 items in cart. | High | High | **P1** | Explicit cart size check, accessible error messaging, blocking submission lock. |
| **RSK-04** | **Missing Customer Name**: Incomplete checkout missing required name. | High | High | **P1** | Required input validation, trimmed string verification, inline error styling and accessible alert. |
| **RSK-05** | **State Loss On Validation Failure**: Customer name or cart items being wiped out after a validation error occurs. | Medium | High | **P1** | Non-destructive state model preserving inputs and cart items upon validation rejection. |
| **RSK-06** | **Negative / Zero Quantity Glitch**: Decrementing quantity below 1 or typing negative numbers. | Medium | Medium | **P2** | Disabled decrement button at qty=1, input event sanitization, input min="1", integer clamping. |

---

## 3. Scope of Testing

### In-Scope
- Synthetic product presentation: Wireless Headphones (₹1,499) and Smart Watch (₹2,499).
- Cart interactions: Add, Remove, Increment (+), Decrement (-), Direct quantity input.
- Real-time line item total and order grand total integer calculation.
- Customer name input validation (required, trimmed).
- Submission locking against rapid multi-clicks.
- Order confirmation rendering with unique order reference and itemized receipt.
- Application state reset via "Start New Order".
- Responsive layout across desktop (1280px) and mobile viewports (390px).

### Out-of-Scope
- Third-party payment gateways, bank OTP integration, multi-page routing, server databases (standalone client application challenge scope).

---

## 4. Verification Scenarios (Browser-Automated & Manual Procedures)

> **Evaluation Note on Test Categorization:**  
> The scenarios below outline the required user acceptance procedures. In our automated verification scripts (`audit_browser_verification.py`), these were executed programmatically using Playwright Chromium to verify real browser behavior and capture screenshot evidence. When a human evaluator runs them directly in an interactive browser window, follow the exact steps below.

### SCENARIO A: Empty Cart Checkout Validation
- **Scenario ID:** `SCN-01`
- **Priority:** High (P1)
- **Preconditions:** Fresh application load, cart is empty (`0 items`, `₹0`).
- **Steps:**
  1. Open the application in browser (`http://localhost:8000/index.html`).
  2. In the "Customer Full Name" field, enter `"Neha Varma"`.
  3. Ensure cart contains zero items.
  4. Click the **"Place Order"** button.
- **Expected Result:**
  - Order submission is blocked.
  - Validation banner appears stating: *"Your cart is empty. Please add at least one product before placing an order."*
  - Entered customer name `"Neha Varma"` remains intact (preserved).
  - Order confirmation screen is NOT shown.
- **Execution Method:** Browser-Automated (Playwright) & Manual Procedure.
- **Status:** **PASS**
- **Evidence Reference:** `evidence/screenshots/scenario_a_empty_cart.png`

---

### SCENARIO B: Missing Required Customer Name
- **Scenario ID:** `SCN-02`
- **Priority:** High (P1)
- **Preconditions:** Smart Watch added to cart (1 unit, ₹2,499); customer name input left empty.
- **Steps:**
  1. Open application and add Smart Watch to cart.
  2. Leave customer name input field empty.
  3. Click **"Place Order"**.
- **Expected Result:**
  - Submission is blocked.
  - Validation banner displays: *"Customer name is required. Please enter your full name to proceed."*
  - Name input border highlights with error indicator (`input-error`).
  - Cart contents (Smart Watch, 1 unit, ₹2,499) are fully preserved.
  - No order confirmation is generated.
- **Execution Method:** Browser-Automated (Playwright) & Manual Procedure.
- **Status:** **PASS**
- **Evidence Reference:** `evidence/screenshots/scenario_b_missing_name.png`

---

### SCENARIO C: Rapid Double-Click on Place Order (Submission Lock)
- **Scenario ID:** `SCN-03`
- **Priority:** Critical (P0)
- **Preconditions:** Wireless Headphones added to cart (1 unit, ₹1,499); valid customer name entered (`"Devika Sengupta"`).
- **Steps:**
  1. Open application and add Wireless Headphones to cart.
  2. Enter `"Devika Sengupta"` in the customer name input.
  3. Click the **"Place Order"** button rapidly twice in succession (< 50ms interval).
- **Expected Result:**
  - Submission lock immediately activates on first click.
  - Button text changes to *"Processing Order..."* and becomes disabled.
  - Exactly **one** order confirmation is generated.
  - Exactly **one** unique Order Reference is created (no duplicates).
  - Total reflects single purchase amount (₹1,499).
- **Execution Method:** Browser-Automated (Playwright) & Manual Procedure.
- **Status:** **PASS**
- **Evidence Reference:** `evidence/screenshots/scenario_c_rapid_double_click.png`

---

### SCENARIO D: Multi-Item Quantity Arithmetic & Exact Total Verification
- **Scenario ID:** `SCN-04`
- **Priority:** Critical (P0)
- **Preconditions:** Application in initial clean state.
- **Steps:**
  1. Add Wireless Headphones; click `+` to increase quantity to 2.
  2. Add Smart Watch; click `+` twice to increase quantity to 3.
  3. Inspect line totals and grand total.
- **Expected Result:**
  - Wireless Headphones: `₹1,499 × 2 = ₹2,998`
  - Smart Watch: `₹2,499 × 3 = ₹7,497`
  - Order Grand Total: `₹2,998 + ₹7,497 = ₹10,495`
- **Execution Method:** Browser-Automated (Playwright) & Manual Procedure.
- **Status:** **PASS**
- **Evidence Reference:** `evidence/screenshots/scenario_d_exact_totals.png`

---

### SCENARIO E: Responsive Viewport Usability (Desktop vs. Mobile)
- **Scenario ID:** `SCN-05`
- **Priority:** Medium (P2)
- **Preconditions:** Application opened on Desktop (1280x840) and Mobile (390x844).
- **Steps:**
  1. View application layout on desktop viewport.
  2. Resize/view application on 390px mobile viewport (iPhone 14 / Android).
  3. Check card layout, sticky checkout summary, buttons, and touch tap targets.
- **Expected Result:**
  - Responsive single-column stacked layout on mobile; two-column grid on desktop.
  - No horizontal scrolling, broken borders, or overlapping text.
- **Execution Method:** Browser-Automated (Playwright) & Manual Inspection.
- **Status:** **PASS**
- **Evidence Reference:** `evidence/screenshots/scenario_e_desktop_viewport.png`, `evidence/screenshots/scenario_e_mobile_viewport.png`

---

## 5. Automated Regression Test Suite Mapping

| Test Function | Type | Focus Area | Status |
| :--- | :--- | :--- | :--- |
| `test_successful_checkout` | Mandatory | Full Happy Path E2E Journey | **PASS** |
| `test_missing_required_customer_name` | Mandatory | Form Validation & Cart Preservation | **PASS** |
| `test_quantity_changes_and_exact_total_calculation` | Mandatory | Integer Arithmetic & Exact Currency Totals | **PASS** |
| `test_empty_cart_checkout_validation` | Extended | Empty State Validation & Name Preservation | **PASS** |
| `test_both_cart_and_name_empty_validation` | Extended | Compound Validation Errors | **PASS** |
| `test_rapid_double_click_protection` | Extended | Submission Lock & Race Condition Prevention | **PASS** |
| `test_product_removal_updates_cart_and_totals` | Extended | Cart Item Removal & Real-time Recomputation | **PASS** |
| `test_quantity_cannot_become_negative_or_zero` | Extended | Input Sanitization & Boundary Protections | **PASS** |
| `test_start_new_order_resets_application_state` | Extended | Clean Application State Reset Flow | **PASS** |

---

## 6. Execution Tools & Environment
- **Browser Automation:** Playwright Chromium 159.0.8154.6
- **Test Runner:** Pytest 9.2.0 + pytest-playwright 0.10.0
- **Runtime:** Python 3.11 / 3.14 on Windows 11
- **Local Web Server:** Ephemeral HTTP server on `127.0.0.1`
