from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin class for the profile model.
    """
    list_display = ('user', 'image_tag', 'bio', 'location', 'birth_date')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """
        Display an image in the admin.
        """
        if obj.image:
            return mark_safe(
                '<img src="%s" width="50" height="50" '
                'style="object-fit: cover; border-radius: 50%%;" />' % obj.image.url
            )
        else:
            return "No Image"
    image_tag.short_description = 'Profile Image'


admin.site.register(Profile, ProfileAdmin)
