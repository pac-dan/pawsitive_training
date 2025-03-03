from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Training, TrainingCategory

def category_trainings(request, category_slug):
    """
    Displays a paginated list of training videos for a given category.
    """
    category = get_object_or_404(TrainingCategory, slug=category_slug)
    trainings = category.trainings.all()  
    paginator = Paginator(trainings, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'category_trainings.html', context)

def training_display(request):
    """
    Displays a paginated list of all training videos.
    """
    trainings = Training.objects.all()
    paginator = Paginator(trainings, 8)  # 8 training videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'training_display.html', context)


def search(request):
    """
    Searches for training videos based on a query string provided via GET parameters.
    """
    query = None
    trainings = Training.objects.all()

    # Check if a search query exists and is non-empty.
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        trainings = trainings.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('training:training_display'))
    
    paginator = Paginator(trainings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_term': query,
    }
    return render(request, 'category_trainings.html', context)


def training_detail(request, pk):
    """
    Displays the detail view of a single training video.
    """
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'training_detail.html', {'training': training})