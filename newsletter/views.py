from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import NewsletterSignupForm


def subscribe(request):
    """
    View to handle newsletter subscriptions with automated welcome email.
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Send welcome email
            try:
                subject = 'Welcome to Pawsitive Training Newsletter!'
                message = f"""Hello!

Thank you for subscribing to the Pawsitive Training newsletter!

You'll receive:
• Training tips and tricks for your furry friends
• Exclusive product offers and discounts
• Early access to new training videos
• Pet care advice from our experts

We're excited to have you in our community!

Best regards,
The Pawsitive Training Team

---
Visit us: https://pawsitive-training-8b1237150b97.herokuapp.com
To unsubscribe, contact us at {settings.DEFAULT_FROM_EMAIL}
"""
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                
                messages.success(
                    request,
                    "Thank you for subscribing! Check your inbox for a welcome email."
                )
            except Exception as e:
                messages.success(
                    request,
                    "Thank you for subscribing to our newsletter!"
                )
                print(f"Newsletter email error: {e}")
        else:
            messages.error(
                request,
                "There was an error with your subscription. "
                "This email may already be subscribed."
            )
    return redirect('welcome')
