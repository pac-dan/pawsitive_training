from django.contrib import admin
from .models import NewsletterSubscriber


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """
    Admin class for the newsletter subscriber model.
    """
    list_display = ('email', 'subscribed_on')
    search_fields = ('email',)
    ordering = ('-subscribed_on',)
    date_hierarchy = 'subscribed_on'


admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
