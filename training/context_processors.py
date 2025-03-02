from .models import TrainingCategory

def training_categories(request):
    return {
        'training_categories': TrainingCategory.objects.all()
    }
