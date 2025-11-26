from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterSignupForm


def subscribe(request):
    """
    View to handle newsletter subscriptions.
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for subscribing to our newsletter! "
                "Go check that inbox."
            )
        else:
            messages.error(
                request,
                "There was an error with your subscription, or you have "
                "already subscribed. Please try again and check your emails."
            )
    return redirect('welcome')
