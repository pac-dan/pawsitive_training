// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string starts with the name we want
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
  // Handle add-to-basket buttons
  document.querySelectorAll('.add-to-basket').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default link behavior
      const url = this.href;
      
      // Send a POST request using fetch
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
        // Update the basket count and total in the navbar
        const basketCountElement = document.getElementById('basket-count');
        if (basketCountElement) {
          basketCountElement.innerText = data.basket_items;
        }
        const basketTotalElement = document.getElementById('basket-total');
        if (basketTotalElement) {
          basketTotalElement.innerText = '$' + data.grand_total;
        }
        // Update quantity in the basket detail table if present
        const quantityElement = document.getElementById('basket-quantity-' + data.product_id);
        if (quantityElement) {
          quantityElement.innerText = data.product_quantity;
        }
        // Update overall basket total on the detail page if present
        const grandTotalElement = document.getElementById('basket-grand-total');
        if (grandTotalElement) {
          grandTotalElement.innerText = data.grand_total;
        }
      })
      .catch(error => {
        console.error('Error adding item to basket:', error);
      });
    });
  });
  
  // Handle remove-from-basket buttons
  document.querySelectorAll('.remove-from-basket').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default link behavior
      const url = this.href;
      
      // Send a POST request using fetch for removal
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
        // Update the basket count and total in the navbar
        const basketCountElement = document.getElementById('basket-count');
        if (basketCountElement) {
          basketCountElement.innerText = data.basket_items;
        }
        const basketTotalElement = document.getElementById('basket-total');
        if (basketTotalElement) {
          basketTotalElement.innerText = '$' + data.grand_total;
        }
        // Update quantity in the basket detail table if present
        const quantityElement = document.getElementById('basket-quantity-' + data.product_id);
        if (quantityElement) {
          quantityElement.innerText = data.product_quantity;
          //  if quantity is 0, remove the product row from the table
          if (data.product_quantity === 0) {
            const rowElement = document.getElementById('basket-row-' + data.product_id);
            if (rowElement) {
              rowElement.remove();
            }
          }
        }
        // Update overall basket total on the detail page if present
        const grandTotalElement = document.getElementById('basket-grand-total');
        if (grandTotalElement) {
          grandTotalElement.innerText = data.grand_total;
        }
        // If the basket is empty, update the container to show an empty message
        if (data.basket_items === 0) {
          const basketContainer = document.getElementById('basket-container');
          if (basketContainer) {
            basketContainer.innerHTML = '<p>Your basket is empty.</p>';
          }
        }
      })
      .catch(error => {
        console.error('Error removing item from basket:', error);
      });
    });
  });
});