/**
 * subscribe.js
 * This file handles the Stripe checkout session for subscriptions.
 * It binds click events to subscription buttons and redirects to Stripe Checkout.
 */

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    // Initialize Stripe using the global variable passed from the template
    const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
    console.log("Stripe object initialized:", stripe);

    /**
     * Redirect to Stripe Checkout session using the provided URL.
     * @param {string} url - The URL for the checkout session.
     */
    function redirectToCheckout(url) {
        console.log("redirectToCheckout called with URL:", url);
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Data received from checkout session:", data);
            if (data.error) {
                console.error("Error from checkout session:", data.error);
            } else {
                // Redirect to Stripe's Checkout
                stripe.redirectToCheckout({ sessionId: data.id }).then(function(result) {
                    if (result.error) {
                        console.error("Stripe redirect error:", result.error.message);
                    }
                });
            }
        })
        .catch(error => console.error("Fetch error:", error));
    }

    // Bind click events to subscription buttons using their data-checkout-url attributes
    const purchaseBtn = document.getElementById("purchase-subscription");
    if (purchaseBtn) {
        purchaseBtn.addEventListener("click", function(e) {
            e.preventDefault();
            console.log("Purchase subscription button clicked");
            let url = this.getAttribute("data-checkout-url");
            console.log("Using checkout URL:", url);
            redirectToCheckout(url);
        });
    } else {
        console.error("Purchase Subscription button not found");
    }

    const yearlyBtn = document.getElementById("purchase-subscription-yearly");
    if (yearlyBtn) {
        yearlyBtn.addEventListener("click", function(e) {
            e.preventDefault();
            console.log("Yearly subscription button clicked");
            let url = this.getAttribute("data-checkout-url");
            console.log("Using checkout URL:", url);
            redirectToCheckout(url);
        });
    } else {
        console.error("Yearly Subscription button not found");
    }

    const renewBtn = document.getElementById("renew-subscription");
    if (renewBtn) {
        renewBtn.addEventListener("click", function(e) {
            e.preventDefault();
            console.log("Renew subscription button clicked");
            let url = this.getAttribute("href");
            console.log("Using renew checkout URL:", url);
            redirectToCheckout(url);
        });
    } else {
        console.error("Renew Subscription button not found");
    }
});