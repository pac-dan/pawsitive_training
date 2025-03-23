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

document.addEventListener('DOMContentLoaded', function() {
  // Handle add-to-basket buttons
  document.querySelectorAll('.add-to-basket').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default link behavior
      const url = this.href;
      
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
        const basketCountElement = document.getElementById('basket-count');
        if (basketCountElement) {
          basketCountElement.innerText = data.basket_items;
        }
        const basketTotalElement = document.getElementById('basket-total');
        if (basketTotalElement) {
          basketTotalElement.innerText = '$' + data.grand_total;
        }
        const quantityElement = document.getElementById('basket-quantity-' + data.product_id);
        if (quantityElement) {
          quantityElement.innerText = data.product_quantity;
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
        
        // Show a toast message if one is provided in the response
        if (data.message) {
          toastr.options = {
              "closeButton": true,
              "progressBar": true,
              "positionClass": "toast-top-right",
              "timeOut": "5000"
          };
          toastr.success(data.message);
        }
      })
      .catch(error => {
        console.error('Error adding item to basket:', error);
        toastr.options = {
              "closeButton": true,
              "progressBar": true,
              "positionClass": "toast-top-right",
              "timeOut": "5000"
          };
        toastr.error("There was an error adding the product to the basket.");
      });
    });
  });
  
  // Handle remove-from-basket buttons
  document.querySelectorAll('.remove-from-basket').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default link behavior
      const url = this.href;
      
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
        const basketCountElement = document.getElementById('basket-count');
        if (basketCountElement) {
          basketCountElement.innerText = data.basket_items;
        }
        const basketTotalElement = document.getElementById('basket-total');
        if (basketTotalElement) {
          basketTotalElement.innerText = '$' + data.grand_total;
        }
        const quantityElement = document.getElementById('basket-quantity-' + data.product_id);
        if (quantityElement) {
          quantityElement.innerText = data.product_quantity;
          // If quantity is 0, remove the product row from the table
          if (data.product_quantity === 0) {
            const rowElement = document.getElementById('basket-row-' + data.product_id);
            if (rowElement) {
              rowElement.remove();
            }
          }
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
        // If the basket is empty, update the container to show an empty message
        if (data.basket_items === 0) {
          const basketContainer = document.getElementById('basket-container');
          if (basketContainer) {
            basketContainer.innerHTML = '<p>Your basket is empty.</p>';
          }
        }
        
        
        if (data.message) {
          toastr.options = {
              "closeButton": true,
              "progressBar": true,
              "positionClass": "toast-top-right",
              "timeOut": "5000"
          };
          toastr.info(data.message);
        }
      })
      .catch(error => {
        console.error('Error removing item from basket:', error);
        toastr.options = {
              "closeButton": true,
              "progressBar": true,
              "positionClass": "toast-top-right",
              "timeOut": "5000"
          };
        toastr.error("There was an error removing the product from the basket.");
      });
    });
  });
});