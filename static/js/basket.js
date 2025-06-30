// Helper function to get the CSRF token from cookies
// This is needed to send POST requests with AJAX
// Source: https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Function to add product to basket from product detail page
function addToBasket(productId) {
  const quantityInput = document.getElementById('quantity-input-' + productId);
  const quantity = parseInt(quantityInput.value);
  
  if (isNaN(quantity) || quantity < 1) {
    toastr.error("Please enter a valid quantity.");
    return;
  }
  
  // First, get current basket quantity for this product
  const url = `/basket/info/${productId}/`;
  
  fetch(url, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
  })
  .then(response => response.json())
  .then(basketInfo => {
    const currentBasketQuantity = basketInfo.current_quantity;
    const maxStock = parseInt(quantityInput.getAttribute('max'));
    const totalQuantity = currentBasketQuantity + quantity;
    
    // Check if total quantity would exceed stock
    if (totalQuantity > maxStock) {
      const availableToAdd = maxStock - currentBasketQuantity;
      if (availableToAdd <= 0) {
        toastr.error(`You already have ${currentBasketQuantity} of this item in your basket. Maximum stock available: ${maxStock}`);
      } else {
        toastr.error(`You can only add ${availableToAdd} more of this item. You already have ${currentBasketQuantity} in your basket.`);
      }
      return;
    }
    
    // If validation passes, add to basket
    const addUrl = `/basket/add/${productId}/`;
    
    fetch(addUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrftoken
      },
      body: `quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        toastr.error(data.error);
        return;
      }
      
      // Update the basket UI elements
      updateBasketUI(data);
      
      // Show success message
      if (data.message) {
        toastr.success(data.message);
      }
      
      // Reset quantity to 1 after successful add
      quantityInput.value = 1;
    })
    .catch(error => {
      console.error('Error adding item to basket:', error);
      toastr.error("There was an error adding the product to the basket.");
    });
  })
  .catch(error => {
    console.error('Error getting basket info:', error);
    toastr.error("There was an error checking basket information.");
  });
}

// Helper function to get current basket quantity for a product
function getCurrentBasketQuantity(productId) {
  // Try to get quantity from basket page if we're on it
  const basketQuantityElement = document.getElementById('quantity-input-' + productId);
  if (basketQuantityElement) {
    return parseInt(basketQuantityElement.value) || 0;
  }
  
  // If not on basket page, we need to get this from the server
  // For now, we'll make a quick request to get basket info
  // This could be optimized by storing basket data in a global variable
  return 0; // Default to 0 if we can't determine
}

// Function to increase quantity on product detail page
function increaseQuantity(productId) {
  const quantityInput = document.getElementById('quantity-input-' + productId);
  const currentQuantity = parseInt(quantityInput.value);
  const maxStock = parseInt(quantityInput.getAttribute('max'));
  
  if (currentQuantity < maxStock) {
    quantityInput.value = currentQuantity + 1;
    // If we're on the basket page, update the basket
    if (window.location.pathname.includes('/basket/')) {
      updateQuantity(productId);
    }
  } else {
    toastr.warning(`Maximum stock available: ${maxStock}`);
  }
}

// Function to decrease quantity on product detail page
function decreaseQuantity(productId) {
  const quantityInput = document.getElementById('quantity-input-' + productId);
  const currentQuantity = parseInt(quantityInput.value);
  
  if (currentQuantity > 1) {
    quantityInput.value = currentQuantity - 1;
    // If we're on the basket page, update the basket
    if (window.location.pathname.includes('/basket/')) {
      updateQuantity(productId);
    }
  } else {
    // If quantity would be 0, remove the item (only on basket page)
    if (window.location.pathname.includes('/basket/')) {
      removeFromBasket(productId);
    }
  }
}

// Function to update quantity via AJAX (for basket page)
function updateQuantity(productId) {
  const quantityInput = document.getElementById('quantity-input-' + productId);
  const quantity = parseInt(quantityInput.value);
  
  if (isNaN(quantity) || quantity < 1) {
    quantityInput.value = 1;
    return;
  }
  
  const url = `/basket/update/${productId}/`;
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
    body: `quantity=${quantity}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      toastr.error(data.error);
      // Reset the input to the previous valid value
      quantityInput.value = data.product_quantity || 1;
      return;
    }
    
    // Update the basket UI elements
    updateBasketUI(data);
    
    // Show success message
    if (data.message) {
      toastr.success(data.message);
    }
  })
  .catch(error => {
    console.error('Error updating quantity:', error);
    toastr.error("There was an error updating the quantity.");
  });
}

// Function to remove item from basket
function removeFromBasket(productId) {
  const url = `/basket/remove/${productId}/`;
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
  })
  .then(response => response.json())
  .then(data => {
    // Update the basket UI elements
    updateBasketUI(data);
    
    // If quantity is 0, remove the product row from the table
    if (data.product_quantity === 0) {
      const rowElement = document.getElementById('basket-row-' + data.product_id);
      if (rowElement) {
        rowElement.remove();
      }
    }
    
    // If the basket is empty, update the container to show an empty message
    if (data.basket_items === 0) {
      const basketContainer = document.querySelector('.basket-contents');
      if (basketContainer) {
        basketContainer.innerHTML = '<h1>Your Basket</h1><p>Your basket is empty.</p>';
      }
    }
    
    // Show message
    if (data.message) {
      toastr.info(data.message);
    }
  })
  .catch(error => {
    console.error('Error removing item from basket:', error);
    toastr.error("There was an error removing the product from the basket.");
  });
}

// Function to update basket UI elements
function updateBasketUI(data) {
  const basketCountElement = document.getElementById('basket-count');
  if (basketCountElement) {
    basketCountElement.innerText = data.basket_items;
  }
  
  const basketTotalElement = document.getElementById('basket-total');
  if (basketTotalElement) {
    basketTotalElement.innerText = '$' + data.grand_total;
  }
  
  const quantityInput = document.getElementById('quantity-input-' + data.product_id);
  if (quantityInput) {
    quantityInput.value = data.product_quantity;
  }
  
  const priceElement = document.getElementById('basket-price-' + data.product_id);
  if (priceElement) {
    priceElement.innerText = '€' + parseFloat(data.product_price).toFixed(2);
  }
  
  const subtotalElement = document.getElementById('basket-subtotal-' + data.product_id);
  if (subtotalElement) {
    subtotalElement.innerText = '€' + parseFloat(data.line_total).toFixed(2);
  }
  
  const grandTotalElement = document.getElementById('basket-grand-total');
  if (grandTotalElement) {
    grandTotalElement.innerText = data.grand_total;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Load basket information for product detail pages
  loadBasketInfo();
  
  // Note: Simple "Add to Basket" buttons on products display page now use form submission
  // and redirect to basket page, so no AJAX handling is needed here.
  // Only product detail page quantity controls use AJAX.
});

// Function to load basket information for product detail pages
function loadBasketInfo() {
  // Check if we're on a product detail page
  const quantitySection = document.querySelector('.quantity-section');
  if (!quantitySection) return;
  
  // Find the product ID from the quantity input
  const quantityInput = quantitySection.querySelector('.quantity-input');
  if (!quantityInput) return;
  
  const productId = quantityInput.id.replace('quantity-input-', '');
  
  // Get basket information for this product
  const url = `/basket/info/${productId}/`;
  
  fetch(url, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
  })
  .then(response => response.json())
  .then(basketInfo => {
    const basketInfoElement = document.getElementById('basket-info-' + productId);
    const currentQuantityElement = document.getElementById('current-basket-quantity-' + productId);
    
    if (basketInfo.current_quantity > 0) {
      // Show basket info if product is in basket
      basketInfoElement.style.display = 'block';
      currentQuantityElement.textContent = basketInfo.current_quantity;
      
      // Update the max attribute to reflect available stock
      const availableToAdd = basketInfo.available_stock - basketInfo.current_quantity;
      quantityInput.setAttribute('max', availableToAdd);
      
      // Update the label to show available to add
      const label = quantityInput.parentElement.previousElementSibling;
      if (label && label.tagName === 'LABEL') {
        label.textContent = `Quantity (${availableToAdd} available to add):`;
      }
    }
  })
  .catch(error => {
    console.error('Error loading basket info:', error);
  });
}