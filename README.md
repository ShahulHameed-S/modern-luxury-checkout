# Fynd Mini Checkout & Automated Browser Test Suite

A responsive, production-quality mini checkout web application and automated Playwright browser test suite developed for the **Fynd Hiring Hackathon**.

The application allows users to browse synthetic products, adjust quantities, view real-time integer-accurate price calculations, validate required customer information, and complete an order with submission lock protection against duplicate confirmations.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Design & Implementation Decisions](#design--implementation-decisions)
6. [Prerequisites](#prerequisites)
7. [Installation & Setup](#installation--setup)
8. [Running the Application](#running-the-application)
9. [Running Automated Tests](#running-automated-tests)
10. [Automated Test Scenarios](#automated-test-scenarios)
11. [Manual Testing & Evidence](#manual-testing--evidence)
12. [Verification Checklist](#verification-checklist)

---

## Project Overview

This project was built to satisfy all requirements of the **Fynd Hiring Hackathon**:
- **Synthetic Product Catalog:**
  - **Wireless Headphones:** ₹1,499
  - **Smart Watch:** ₹2,499
- **Cart Management:** Add, remove, increment, decrement, and direct input sanitization.
- **Strict Integer Arithmetic:** Guaranteed precision for currency operations, eliminating floating-point drift.
- **Form Validation & State Preservation:** Accessible validation alerts for empty cart or missing name, preserving entered data.
- **Submission Lock & Debounce:** Synchronous state locking to prevent rapid multi-click double-ordering.
- **Automated Testing Suite:** 9 end-to-end tests written with Pytest and Playwright asserting customer-facing behavior.

---

## Key Features

### Frontend (Application)
- **Modern Responsive Design:** Crafted with clean typography, balanced spacing, and responsive layouts for desktop, tablet, and mobile (iPhone / Android) screens.
- **Real-Time Synchronized Cart:** Dynamic calculation of line items and order totals.
- **Strict Integer Math:** Prices and quantities are computed strictly as whole integer numbers.
- **Negative Quantity Prevention:** The decrement button is disabled when quantity is 1; keyboard inputs below 1 or non-numeric characters are automatically sanitized.
- **Defensive Submission Locking:** Synchronous lock prevents duplicate order submissions when "Place Order" is clicked repeatedly or rapidly.
- **Order Confirmation & Reset:** Displays a unique order reference (`ORD-YYMMDD-XXXX-XXXX`), itemized list, and an option to start a new order.

### Quality Assurance & SDET
- **100% Test Pass Rate:** 9/9 automated Playwright tests passing on Chromium.
- **Isolated Browser Contexts:** Every test launches with an independent session to eliminate test pollution.
- **Failure Screenshot Capture:** Configured pytest hook to capture failure evidence automatically if any test fails.
- **Zero Fixed Sleeps:** All assertions utilize Playwright's locator wait conditions (`expect(locator).to_be_visible()`, `expect(locator).to_have_text()`).

---

## Technology Stack

### Frontend:
- **HTML5:** Semantic structure, accessible WAI-ARIA attributes (`role="alert"`, `aria-live`, `aria-required`).
- **CSS3:** Custom responsive layout using Flexbox, CSS Grid, CSS custom properties (variables), no bulky third-party CSS frameworks.
- **Vanilla JavaScript (ES6+):** Pure client-side state machine with strict integer arithmetic.

### Testing & Automation:
- **Python 3.11+ / 3.14:** Core automation environment.
- **Playwright (v1.65+):** Modern, reliable browser automation engine.
- **Pytest (v9.2+):** Test runner, assertion engine, and lifecycle fixtures.
- **pytest-playwright:** Pytest integration for browser orchestration.

---

## Project Structure

```text
fynd-mini-checkout/
│
├── index.html                  # Main semantic checkout markup
├── styles.css                  # Responsive, modern stylesheet
├── app.js                      # Vanilla JavaScript application state & logic
├── requirements.txt            # Python dependencies for automated testing
├── pytest.ini                  # Pytest configuration, markers, and filters
├── capture_evidence.py         # Evidence generation script for manual tests
│
├── tests/
│   ├── conftest.py             # Ephemeral HTTP server fixture & failure screenshots
│   └── test_checkout.py        # 9 automated Playwright test cases (Mandatory + Extended)
│
├── evidence/
│   ├── screenshots/            # High-resolution screenshots of all test scenarios
│   │   ├── 01_initial_state_landing.png
│   │   ├── 02_manual_tc01_empty_cart_validation.png
│   │   ├── 03_missing_customer_name_validation.png
│   │   ├── 04_quantity_exact_totals_calculation.png
│   │   ├── 05_order_confirmation_success.png
│   │   └── 06_mobile_responsive_view.png
│   ├── test-results/
│   │   ├── junit.xml           # Standard JUnit test execution XML report
│   │   └── pytest_output.txt   # Complete stdout from pytest run
│   └── videos/
│       ├── fynd_mini_checkout_demo_final.webm  # Master 84s 1280x900 professional demonstration video (85-90s timeline)
│       └── fynd_mini_checkout_demo.webm        # Initial demonstration video
│
├── README.md                   # Comprehensive documentation and setup guide
├── TEST_PLAN.md                # Risk assessment, test strategy, and manual test cases
└── TEST_RESULTS.md             # Execution report, defect log, and SDET sign-off
```

---

## Design & Implementation Decisions

1. **Whole Integer Arithmetic for Monetary Precision:**
   Standard floating-point numbers in JavaScript (IEEE 754) can suffer from decimal drift (e.g. `0.1 + 0.2 = 0.30000000000000004`). In this application, all prices are fixed integers in Rupees (`1499` and `2499`), and quantities are strictly positive integers. Because JavaScript safely represents integers exactly up to `Number.MAX_SAFE_INTEGER` ($2^{53} - 1$), computing `price * quantity` and summing line items entirely avoids fractional floating-point inaccuracies. Defensive integer parsing (`parseInt(..., 10)`) is used on user inputs:
   ```javascript
   function calculateLineTotal(unitPrice, quantity) {
     const q = Math.max(0, parseInt(quantity, 10) || 0);
     const p = Math.max(0, parseInt(unitPrice, 10) || 0);
     return p * q;
   }
   ```
2. **Synchronous Submission Locking:**
   To eliminate duplicate submissions from rapid double-clicks:
   ```javascript
   if (submissionLockAcquired || state.isSubmitting || state.isCompleted) {
     return;
   }
   submissionLockAcquired = true;
   state.isSubmitting = true;
   dom.placeOrderBtn.disabled = true;
   dom.placeOrderBtnText.textContent = 'Processing Order...';
   ```
   The lock is engaged synchronously *before* any validation or async operations, guaranteeing duplicate events are immediately dropped.
3. **Data Preservation on Validation Failure:**
   When validation errors occur (e.g., missing name or empty cart), the input fields and cart state remain completely untouched. The user does not need to re-enter information or re-add items.
4. **Isolated Test Execution with Local HTTP Server:**
   Rather than loading raw `file://` URLs, `tests/conftest.py` starts a background ephemeral Python HTTP server on `127.0.0.1`. Each test gets an isolated Playwright page context, ensuring tests never leak state to one another.

---

## Prerequisites

- **Python 3.10+** (Python 3.11+ recommended)
- **uv** (recommended for ultra-fast setup) or standard **pip**
- **Modern Web Browser:** (Google Chrome, Chromium, Edge, Firefox, or Safari)

---

## Installation & Setup

### 1. Clone or Extract the Project:
Open your terminal in the project directory:
```powershell
cd c:\shahul\Desktop\fyd
```

### 2. Create Virtual Environment and Install Dependencies:

**Using `uv` (Recommended):**
```powershell
uv venv .venv
.\.venv\Scripts\activate
uv pip install -r requirements.txt
playwright install chromium
```

**Using Standard `pip`:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

---

## Running the Application

To run the application locally in your browser:

### Option A: Using Python's Built-in HTTP Server (Recommended)
```powershell
python -m http.server 8000
```
Open your browser and navigate to:
```
http://localhost:8000/index.html
```

### Option B: Direct File Opening
You can double-click `index.html` or open it directly in any modern browser:
```powershell
Start-Process "index.html"
```

---

## Running Automated Tests

Make sure your virtual environment is active:
```powershell
.\.venv\Scripts\activate
```

### Run All Automated Tests:
```powershell
pytest -v
```

### Run Only Mandatory Tests:
```powershell
pytest -v -m mandatory
```

### Run with Headed Browser (Visible Window):
```powershell
pytest -v --headed
```

### Generate JUnit XML Test Report:
```powershell
pytest -v --junitxml=evidence/test-results/junit.xml
```

---

## Automated Test Scenarios

The suite (`tests/test_checkout.py`) provides 9 comprehensive tests:

| Marker | Test Name | Objective |
| :--- | :--- | :--- |
| `@pytest.mark.mandatory` | `test_successful_checkout` | Adds product, fills customer name, places order, verifies confirmation, order reference, and exact total. |
| `@pytest.mark.mandatory` | `test_missing_required_customer_name` | Leaves customer name empty, asserts checkout is blocked, validation message shown, and cart items preserved. |
| `@pytest.mark.mandatory` | `test_quantity_changes_and_exact_total_calculation` | Adds 2x Headphones (₹2,998) + 3x Smart Watch (₹7,497), asserts line totals and exact grand total (₹10,495). |
| `@pytest.mark.extended` | `test_empty_cart_checkout_validation` | Attempts checkout with 0 items, verifies validation alert and preservation of customer name. |
| `@pytest.mark.extended` | `test_both_cart_and_name_empty_validation` | Verifies compound validation messages when both cart is empty and name is missing. |
| `@pytest.mark.extended` | `test_rapid_double_click_protection` | Rapidly double-clicks Place Order; verifies synchronous lock and guarantees exactly 1 order confirmation. |
| `@pytest.mark.extended` | `test_product_removal_updates_cart_and_totals` | Removes items from cart; verifies dynamic total recomputation and empty state trigger. |
| `@pytest.mark.extended` | `test_quantity_cannot_become_negative_or_zero` | Tests decrease button disabling at qty=1 and input sanitization against negative inputs. |
| `@pytest.mark.extended` | `test_start_new_order_resets_application_state` | Tests the post-checkout reset flow, verifying clean state restoration for subsequent orders. |

---

## Manual Testing & Evidence

Full test cases and execution logs are detailed in [TEST_PLAN.md](file:///c:/shahul/Desktop/fyd/TEST_PLAN.md) and [TEST_RESULTS.md](file:///c:/shahul/Desktop/fyd/TEST_RESULTS.md).

Screenshots captured during test execution are stored in `evidence/screenshots/`:
1. `01_initial_state_landing.png` - Initial clean store layout.
2. `02_manual_tc01_empty_cart_validation.png` - Empty cart checkout validation banner.
3. `03_missing_customer_name_validation.png` - Missing name validation with red field highlighting.
4. `04_quantity_exact_totals_calculation.png` - Exact integer total calculation for ₹10,495.
5. `05_order_confirmation_success.png` - Order receipt card with unique order reference.
6. `06_mobile_responsive_view.png` - Viewport layout on mobile devices.

To re-generate all visual evidence screenshots:
```powershell
python capture_evidence.py
```

---

## Verification Checklist

- [x] Product 1: Wireless Headphones (₹1,499) implemented.
- [x] Product 2: Smart Watch (₹2,499) implemented.
- [x] Integer arithmetic for all currency calculations.
- [x] Cart addition, quantity increment/decrement, and removal.
- [x] Quantity clamped to minimum of 1; non-negative validation.
- [x] Customer name required field with validation.
- [x] Cart contents and customer name preserved on validation failures.
- [x] Order confirmation with unique reference and correct total.
- [x] Rapid multi-click submission lock protection.
- [x] Responsive layout for mobile and desktop screens.
- [x] TEST 1: Successful Checkout passed.
- [x] TEST 2: Missing Required Field passed.
- [x] TEST 3: Quantity and Exact Total passed (₹10,495).
- [x] Empty cart validation automated and manual tests passed.
- [x] Double-click protection automated and manual tests passed.
- [x] Genuine screenshot evidence captured and documented.
- [x] Zero defects encountered; test suite passes 100%.
