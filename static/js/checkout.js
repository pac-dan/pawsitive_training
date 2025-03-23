/**
 * checkout.js
 * Handles the Stripe Checkout redirection for the payments page.
 */

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Stripe using the global variable STRIPE_PUBLISHABLE_KEY
    var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
    console.log("Stripe initialized:", stripe);

    // Bind event to the checkout button
    var checkoutButton = document.getElementById("checkout-button");
    if (checkoutButton) {
        checkoutButton.addEventListener("click", function () {
            fetch(CHECKOUT_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN
                },
                body: JSON.stringify({})  
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    stripe.redirectToCheckout({ sessionId: data.id }).then(function (result) {
                        if (result.error) {
                            console.error("Stripe redirect error:", result.error.message);
                        }
                    });
                }
            })
            .catch(error => console.error("Fetch error:", error));
        });
    } else {
        console.error("Checkout button not found!");
    }
});