from django.contrib import admin
from .models import Training, TrainingCategory

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('title',)

admin.site.register(Training, TrainingAdmin)
admin.site.register(TrainingCategory)