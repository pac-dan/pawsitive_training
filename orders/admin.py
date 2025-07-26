from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for the order model.
    """
    list_display = ('stripe_checkout_session_id', 'user', 'amount', 'payment_confirmed', 'status', 'shipped', 'created')
    list_filter = ('payment_confirmed', 'status', 'shipped', 'created', 'user')
    search_fields = ('stripe_checkout_session_id', 'user__username', 'user__email', 'tracking_number')
    ordering = ('-created',)
    readonly_fields = ('stripe_checkout_session_id', 'created', 'total_amount')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('stripe_checkout_session_id', 'user', 'amount', 'created', 'total_amount')
        }),
        ('Payment', {
            'fields': ('payment_confirmed', 'status')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'billing_address', 'shipping_cost', 'tax_amount', 'shipped', 'tracking_number')
        }),
    )

admin.site.register(Order, OrderAdmin)
