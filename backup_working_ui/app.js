/**
 * Fynd Mini Checkout - Frontend Application Logic
 * Implements strict integer arithmetic, responsive cart updates,
 * robust validation, and submission locking to prevent duplicate orders.
 */

(function () {
  'use strict';

  // --- 1. Product Catalog Definitions ---
  const PRODUCTS = [
    {
      id: 'headphones',
      name: 'Wireless Headphones',
      price: 1499, // Integer in Rupees
      sku: 'WHP-1001'
    },
    {
      id: 'smartwatch',
      name: 'Smart Watch',
      price: 2499, // Integer in Rupees
      sku: 'SMW-2002'
    }
  ];

  // Map for O(1) product lookup
  const PRODUCT_MAP = new Map(PRODUCTS.map((p) => [p.id, p]));

  // --- 2. Application State ---
  const state = {
    cart: {}, // Map of productId -> { product, quantity: integer }
    customerName: '',
    isSubmitting: false,
    isCompleted: false,
    orderConfirmation: null,
    validationErrors: []
  };

  // --- 3. DOM Elements Cache ---
  const dom = {
    // Buttons
    addHeadphonesBtn: document.getElementById('add-headphones-btn'),
    addSmartwatchBtn: document.getElementById('add-smartwatch-btn'),
    placeOrderBtn: document.getElementById('place-order-btn'),
    placeOrderBtnText: document.getElementById('place-order-btn-text'),
    startNewOrderBtn: document.getElementById('start-new-order-btn'),
    dismissAlertBtn: document.getElementById('dismiss-alert-btn'),

    // Input
    customerNameInput: document.getElementById('customer-name'),

    // Cart Section
    cartCountBadge: document.getElementById('cart-count-badge'),
    emptyCartState: document.getElementById('empty-cart-state'),
    cartItemsWrapper: document.getElementById('cart-items-wrapper'),
    cartItemsList: document.getElementById('cart-items-list'),

    // Totals
    summarySubtotal: document.getElementById('summary-subtotal'),
    orderTotal: document.getElementById('order-total'),

    // Validation
    validationContainer: document.getElementById('validation-container'),
    validationMessages: document.getElementById('validation-messages'),

    // Confirmation
    checkoutView: document.getElementById('checkout-view'),
    confirmationSection: document.getElementById('order-confirmation-section'),
    confirmOrderRef: document.getElementById('confirm-order-ref'),
    confirmCustomerName: document.getElementById('confirm-customer-name'),
    confirmOrderTotal: document.getElementById('confirm-order-total'),
    confirmOrderTime: document.getElementById('confirm-order-time'),
    confirmItemsList: document.getElementById('confirm-items-list')
  };

  // --- 4. Currency Formatter (Integer Safe) ---
  function formatINR(amountInRupees) {
    // Assert safe positive integer amount
    const safeAmount = Math.max(0, parseInt(amountInRupees, 10) || 0);
    return '₹' + safeAmount.toLocaleString('en-IN');
  }

  // --- 5. Calculation Helpers (Exact Integer Arithmetic) ---
  function calculateLineTotal(unitPrice, quantity) {
    const q = Math.max(0, parseInt(quantity, 10) || 0);
    const p = Math.max(0, parseInt(unitPrice, 10) || 0);
    return p * q;
  }

  function calculateCartTotal() {
    let grandTotal = 0;
    for (const item of Object.values(state.cart)) {
      grandTotal += calculateLineTotal(item.product.price, item.quantity);
    }
    return grandTotal;
  }

  function getCartItemCount() {
    let count = 0;
    for (const item of Object.values(state.cart)) {
      count += item.quantity;
    }
    return count;
  }

  // --- 6. Unique Order Reference Generator ---
  let orderSequenceCounter = 1000;
  function generateOrderReference() {
    orderSequenceCounter += Math.floor(Math.random() * 5) + 1;
    const now = new Date();
    const datePart = now.getFullYear().toString().slice(-2) +
      String(now.getMonth() + 1).padStart(2, '0') +
      String(now.getDate()).padStart(2, '0');
    const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `ORD-${datePart}-${orderSequenceCounter}-${randomHex}`;
  }

  // --- 7. Validation Logic ---
  function validateOrder() {
    const errors = [];
    const cartKeys = Object.keys(state.cart);

    // Rule 1: Cart must not be empty
    if (cartKeys.length === 0 || getCartItemCount() === 0) {
      errors.push('Your cart is empty. Please add at least one product before placing an order.');
    }

    // Rule 2: Customer Name is required
    const trimmedName = state.customerName.trim();
    if (!trimmedName) {
      errors.push('Customer name is required. Please enter your full name to proceed.');
    }

    return errors;
  }

  function displayValidationErrors(errors) {
    state.validationErrors = errors;

    if (!errors || errors.length === 0) {
      dom.validationContainer.style.display = 'none';
      dom.validationMessages.innerHTML = '';
      dom.customerNameInput.classList.remove('input-error');
      return;
    }

    // Build message content
    if (errors.length === 1) {
      dom.validationMessages.textContent = errors[0];
    } else {
      const list = document.createElement('ul');
      errors.forEach((err) => {
        const li = document.createElement('li');
        li.textContent = err;
        list.appendChild(li);
      });
      dom.validationMessages.innerHTML = '';
      dom.validationMessages.appendChild(list);
    }

    // Highlight input if name error present
    const hasNameError = errors.some((msg) => msg.toLowerCase().includes('name'));
    if (hasNameError) {
      dom.customerNameInput.classList.add('input-error');
    } else {
      dom.customerNameInput.classList.remove('input-error');
    }

    dom.validationContainer.style.display = 'flex';
    // Scroll alert into view if needed
    dom.validationContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function clearValidationErrors() {
    displayValidationErrors([]);
  }

  // --- 8. Cart Management Actions ---
  function addToCart(productId) {
    if (state.isCompleted) return;

    const product = PRODUCT_MAP.get(productId);
    if (!product) return;

    if (state.cart[productId]) {
      state.cart[productId].quantity += 1;
    } else {
      state.cart[productId] = {
        product: product,
        quantity: 1
      };
    }

    // Clear validation if it was previously complaining about empty cart
    if (state.validationErrors.some((e) => e.toLowerCase().includes('cart'))) {
      clearValidationErrors();
    }

    render();
  }

  function updateQuantity(productId, newQuantity) {
    if (state.isCompleted) return;

    const item = state.cart[productId];
    if (!item) return;

    // Strict positive integer validation: disallow negative or zero quantities
    const parsedQty = parseInt(newQuantity, 10);
    if (isNaN(parsedQty) || parsedQty < 1) {
      // Revert/ignore invalid or negative quantity
      render();
      return;
    }

    item.quantity = parsedQty;
    render();
  }

  function increaseQuantity(productId) {
    if (state.isCompleted) return;
    const item = state.cart[productId];
    if (!item) return;
    updateQuantity(productId, item.quantity + 1);
  }

  function decreaseQuantity(productId) {
    if (state.isCompleted) return;
    const item = state.cart[productId];
    if (!item) return;

    // Do not allow quantity to drop below 1 via decrement button
    if (item.quantity > 1) {
      updateQuantity(productId, item.quantity - 1);
    }
  }

  function removeFromCart(productId) {
    if (state.isCompleted) return;
    if (state.cart[productId]) {
      delete state.cart[productId];
      render();
    }
  }

  // --- 9. Checkout & Submission Lock Logic ---
  let submissionLockAcquired = false;

  async function handlePlaceOrder() {
    // Check Submission Locks
    if (submissionLockAcquired || state.isSubmitting || state.isCompleted) {
      console.warn('Place Order blocked by active submission lock.');
      return;
    }

    // 1. Immediately engage synchronous lock
    submissionLockAcquired = true;
    state.isSubmitting = true;

    // Update button visual state immediately
    dom.placeOrderBtn.disabled = true;
    dom.placeOrderBtnText.textContent = 'Processing Order...';

    // Sync current input value into state
    state.customerName = dom.customerNameInput.value;

    // 2. Validate Cart and Customer Name
    const errors = validateOrder();

    if (errors.length > 0) {
      // Display understandable validation messages
      displayValidationErrors(errors);

      // CRITICAL: Preserve customer's entered name and existing cart contents!
      // (State is kept intact; input retains value)
      
      // Release submission lock so customer can correct details and re-submit
      state.isSubmitting = false;
      submissionLockAcquired = false;
      dom.placeOrderBtn.disabled = false;
      dom.placeOrderBtnText.textContent = 'Place Order';
      return;
    }

    // 3. Validation passed - Clear any errors
    clearValidationErrors();

    // 4. Simulate a short asynchronous checkout processing step (150ms)
    // To strictly demonstrate debounce / rapid double-click protection
    await new Promise((resolve) => setTimeout(resolve, 150));

    // 5. Generate confirmation details
    const orderTotal = calculateCartTotal();
    const orderRef = generateOrderReference();
    const orderItems = Object.values(state.cart).map((item) => ({
      name: item.product.name,
      quantity: item.quantity,
      unitPrice: item.product.price,
      lineTotal: calculateLineTotal(item.product.price, item.quantity)
    }));

    state.orderConfirmation = {
      orderReference: orderRef,
      customerName: state.customerName.trim(),
      total: orderTotal,
      items: orderItems,
      dateString: new Date().toLocaleString('en-IN', {
        dateStyle: 'medium',
        timeStyle: 'short'
      })
    };

    // 6. Lock state permanently for this session
    state.isCompleted = true;
    state.isSubmitting = false;
    // submissionLockAcquired remains true to prevent ANY subsequent submit
    dom.placeOrderBtn.disabled = true;
    dom.placeOrderBtnText.textContent = 'Order Completed';

    // 7. Render Confirmation
    renderConfirmation();
  }

  // --- 10. Start New Order / Reset ---
  function resetOrder() {
    state.cart = {};
    state.customerName = '';
    state.isSubmitting = false;
    state.isCompleted = false;
    state.orderConfirmation = null;
    state.validationErrors = [];
    submissionLockAcquired = false;

    dom.customerNameInput.value = '';
    dom.customerNameInput.disabled = false;
    dom.customerNameInput.classList.remove('input-error');

    dom.placeOrderBtn.disabled = false;
    dom.placeOrderBtnText.textContent = 'Place Order';

    dom.confirmationSection.style.display = 'none';
    dom.checkoutView.style.display = 'grid';

    clearValidationErrors();
    render();
  }

  // --- 11. Render Methods ---
  function renderCart() {
    const items = Object.values(state.cart);
    const totalItemsCount = getCartItemCount();

    dom.cartCountBadge.textContent = `${totalItemsCount} ${totalItemsCount === 1 ? 'item' : 'items'}`;

    if (items.length === 0) {
      dom.emptyCartState.style.display = 'block';
      dom.cartItemsWrapper.style.display = 'none';
      dom.cartItemsList.innerHTML = '';
    } else {
      dom.emptyCartState.style.display = 'none';
      dom.cartItemsWrapper.style.display = 'block';

      // Rebuild cart rows
      dom.cartItemsList.innerHTML = '';

      items.forEach((item) => {
        const prod = item.product;
        const lineTotal = calculateLineTotal(prod.price, item.quantity);

        const row = document.createElement('div');
        row.className = 'cart-item-row';
        row.dataset.testid = `cart-item-${prod.id}`;

        // Product Name
        const nameCol = document.createElement('div');
        nameCol.className = 'cart-item-title';
        nameCol.textContent = prod.name;

        // Unit Price
        const priceCol = document.createElement('div');
        priceCol.className = 'cart-item-unit-price col-price';
        priceCol.textContent = formatINR(prod.price);

        // Quantity Controls
        const qtyCol = document.createElement('div');
        qtyCol.className = 'col-qty';

        const qtyGroup = document.createElement('div');
        qtyGroup.className = 'qty-control-group';

        const decBtn = document.createElement('button');
        decBtn.type = 'button';
        decBtn.className = 'qty-btn';
        decBtn.dataset.testid = `qty-decrease-${prod.id}`;
        decBtn.setAttribute('aria-label', `Decrease quantity of ${prod.name}`);
        decBtn.textContent = '−';
        decBtn.disabled = item.quantity <= 1 || state.isCompleted;
        decBtn.addEventListener('click', () => decreaseQuantity(prod.id));

        const qtyInput = document.createElement('input');
        qtyInput.type = 'number';
        qtyInput.className = 'qty-input';
        qtyInput.dataset.testid = `qty-input-${prod.id}`;
        qtyInput.value = item.quantity;
        qtyInput.min = '1';
        qtyInput.step = '1';
        qtyInput.disabled = state.isCompleted;
        qtyInput.setAttribute('aria-label', `Quantity of ${prod.name}`);
        
        // Prevent manual entry of negative or invalid values
        qtyInput.addEventListener('change', (e) => {
          const val = parseInt(e.target.value, 10);
          if (isNaN(val) || val < 1) {
            e.target.value = item.quantity;
          } else {
            updateQuantity(prod.id, val);
          }
        });
        qtyInput.addEventListener('keydown', (e) => {
          // Block '-' and 'e' keys
          if (e.key === '-' || e.key === 'e' || e.key === '+' || e.key === '.') {
            e.preventDefault();
          }
        });

        const incBtn = document.createElement('button');
        incBtn.type = 'button';
        incBtn.className = 'qty-btn';
        incBtn.dataset.testid = `qty-increase-${prod.id}`;
        incBtn.setAttribute('aria-label', `Increase quantity of ${prod.name}`);
        incBtn.textContent = '+';
        incBtn.disabled = state.isCompleted;
        incBtn.addEventListener('click', () => increaseQuantity(prod.id));

        qtyGroup.appendChild(decBtn);
        qtyGroup.appendChild(qtyInput);
        qtyGroup.appendChild(incBtn);
        qtyCol.appendChild(qtyGroup);

        // Line Total
        const totalCol = document.createElement('div');
        totalCol.className = 'cart-item-line-total col-total';
        totalCol.dataset.testid = `line-total-${prod.id}`;
        totalCol.textContent = formatINR(lineTotal);

        // Action: Remove Button
        const actionCol = document.createElement('div');
        actionCol.className = 'col-action';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn-remove-item';
        removeBtn.dataset.testid = `remove-item-${prod.id}`;
        removeBtn.setAttribute('aria-label', `Remove ${prod.name} from cart`);
        removeBtn.innerHTML = `
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
          Remove
        `;
        removeBtn.disabled = state.isCompleted;
        removeBtn.addEventListener('click', () => removeFromCart(prod.id));
        actionCol.appendChild(removeBtn);

        row.appendChild(nameCol);
        row.appendChild(priceCol);
        row.appendChild(qtyCol);
        row.appendChild(totalCol);
        row.appendChild(actionCol);

        dom.cartItemsList.appendChild(row);
      });
    }

    // Update Totals
    const grandTotal = calculateCartTotal();
    dom.summarySubtotal.textContent = formatINR(grandTotal);
    dom.orderTotal.textContent = formatINR(grandTotal);
  }

  function renderConfirmation() {
    if (!state.orderConfirmation) return;

    const conf = state.orderConfirmation;
    dom.confirmOrderRef.textContent = conf.orderReference;
    dom.confirmCustomerName.textContent = conf.customerName;
    dom.confirmOrderTotal.textContent = formatINR(conf.total);
    dom.confirmOrderTime.textContent = conf.dateString;

    // Render items summary list
    dom.confirmItemsList.innerHTML = '';
    conf.items.forEach((item) => {
      const itemRow = document.createElement('div');
      itemRow.className = 'confirm-item-row';
      itemRow.innerHTML = `
        <span class="confirm-item-name">${item.name} <span class="confirm-item-qty">× ${item.quantity}</span></span>
        <span class="confirm-item-total">${formatINR(item.lineTotal)}</span>
      `;
      dom.confirmItemsList.appendChild(itemRow);
    });

    // Hide checkout grid, show confirmation card
    dom.checkoutView.style.display = 'none';
    dom.confirmationSection.style.display = 'block';
    dom.confirmationSection.scrollIntoView({ behavior: 'smooth' });
  }

  function render() {
    renderCart();
  }

  // --- 12. Event Listeners ---
  function initEventListeners() {
    // Add product to cart buttons
    dom.addHeadphonesBtn.addEventListener('click', () => addToCart('headphones'));
    dom.addSmartwatchBtn.addEventListener('click', () => addToCart('smartwatch'));

    // Input typing keeps state in sync
    dom.customerNameInput.addEventListener('input', (e) => {
      state.customerName = e.target.value;
      if (dom.customerNameInput.classList.contains('input-error') && state.customerName.trim()) {
        dom.customerNameInput.classList.remove('input-error');
      }
    });

    // Place Order button
    dom.placeOrderBtn.addEventListener('click', (e) => {
      e.preventDefault();
      handlePlaceOrder();
    });

    // Reset / New Order
    dom.startNewOrderBtn.addEventListener('click', () => {
      resetOrder();
    });

    // Dismiss Alert
    dom.dismissAlertBtn.addEventListener('click', () => {
      clearValidationErrors();
    });
  }

  // --- 13. Application Initialization ---
  function init() {
    initEventListeners();
    render();
    console.log('Fynd Mini Checkout initialized.');
  }

  // Start when DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose state and API for testing/debugging verification if in window
  window.__MINI_CHECKOUT__ = {
    getState: () => ({ ...state }),
    calculateCartTotal,
    calculateLineTotal,
    addToCart,
    removeFromCart,
    updateQuantity,
    resetOrder
  };
})();
