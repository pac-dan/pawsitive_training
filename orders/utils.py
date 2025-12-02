from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """
    Send order confirmation email to customer
    """
    if not order.customer_email:
        print(f"No email for order {order.id}")
        return False

    try:
        subject = f'Order Confirmation - Pawsitive Training'

        text_content = f"""
Order Confirmation

Thank you for your order!

Order Number: {order.stripe_checkout_session_id}
Order Date: {order.created.strftime('%B %d, %Y at %I:%M %p')}
Total: ${order.amount:.2f}

Items Ordered:
"""
        for item in order.items.all():
            text_content += f"\n- {item.product.name} x {item.quantity} @ ${item.price:.2f} = ${item.item_total:.2f}"

        if order.shipping_address:
            text_content += f"""

Shipping Address:
{order.shipping_address}
"""

        text_content += f"""

You can view your order history in your profile dashboard.

Thank you for shopping with Pawsitive Training!

Best regards,
The Pawsitive Training Team
"""

        html_content = render_to_string('emails/order_confirmation.html', {
            'order': order,
        })

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

