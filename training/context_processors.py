from .models import TrainingCategory


def training_categories(request):
    """
    A context processor to add training categories to the context.
    """
    return {
        'training_categories': TrainingCategory.objects.all()
    }
