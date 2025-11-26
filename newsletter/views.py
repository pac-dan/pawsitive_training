from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .forms import NewsletterSignupForm


def subscribe(request):
    """
    View to handle newsletter subscriptions with automated HTML welcome email.
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Send welcome email (HTML + plain text)
            try:
                subject = 'Welcome to Pawsitive Training Newsletter! 🐾'
                
                # Plain text version (fallback)
                text_content = f"""Hello!

Thank you for subscribing to the Pawsitive Training newsletter!

You'll receive:
• Training tips and tricks for your furry friends
• Exclusive product offers and discounts
• Early access to new training videos
• Pet care advice from our experts

We're excited to have you in our community!

Visit us: https://pawsitive-training-8b1237150b97.herokuapp.com
Shop Products: https://pawsitive-training-8b1237150b97.herokuapp.com/products/
Watch Training Videos: https://pawsitive-training-8b1237150b97.herokuapp.com/training/

Best regards,
The Pawsitive Training Team

---
To unsubscribe, contact us at {settings.DEFAULT_FROM_EMAIL}
"""
                
                # HTML version
                html_content = render_to_string('newsletter/welcome_email.html', {
                    'subscriber_email': subscriber.email,
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                })
                
                # Create email with both versions
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                
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
