from django.contrib import admin
from .models import Training

admin.site.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('title',)
