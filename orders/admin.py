from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for the order model.
    """
    list_display = ('stripe_checkout_session_id', 'user', 'amount', 'status', 'created')
    list_filter = ('status', 'created', 'user')
    search_fields = ('stripe_checkout_session_id', 'user__username', 'user__email')
    ordering = ('-created',)

admin.site.register(Order, OrderAdmin)
