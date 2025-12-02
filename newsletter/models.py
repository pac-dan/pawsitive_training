from django.db import models


class NewsletterSubscriber(models.Model):
    """
    Model to store newsletter subscribers.
    """
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
