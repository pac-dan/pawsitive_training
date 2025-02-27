from django.shortcuts import render, get_object_or_404
from .models import Training


def training_display(request):
    trainings = Training.objects.all()
    return render(request, 'training_display.html', {'trainings': trainings})

def training_detail(request, pk):    
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'training_detail.html', {'training': training})

