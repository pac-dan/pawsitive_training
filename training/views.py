from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Training, TrainingCategory
from django.utils import timezone
from subscriptions.models import Subscription
from django.contrib.admin.views.decorators import staff_member_required
from .forms import TrainingForm

def category_trainings(request, category_slug):
    """
    Displays a paginated list of training videos for a given category.
    """

    # Get the category object based on the slug.
    category = get_object_or_404(TrainingCategory, slug=category_slug)
    trainings = category.trainings.all()  
    paginator = Paginator(trainings, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if the user has an active subscription.
    context = {
        'category': category,
        'page_obj': page_obj,
        'has_subscription': request.user.subscription.is_active() if request.user.is_authenticated and hasattr(request.user, 'subscription') else False,
    }
    return render(request, 'training/category_trainings.html', context)

def training_display(request):
    """
    Displays a paginated list of all training videos.
    """

    # Get all training videos and paginate them.
    trainings = Training.objects.all()
    paginator = Paginator(trainings, 8)  # 8 training videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if the user has an active subscription.
    context = {
        'page_obj': page_obj,
        'has_subscription': request.user.subscription.is_active() if request.user.is_authenticated and hasattr(request.user, 'subscription') else False,
    }
    return render(request, 'training/training_display.html', context)


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
    # If no results are found, display an error message.
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('training:training_display'))
    
    # Paginate the results.
    paginator = Paginator(trainings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if the user has an active subscription.
    context = {
        'page_obj': page_obj,
        'search_term': query,
        'has_subscription': request.user.subscription.is_active() if request.user.is_authenticated and hasattr(request.user, 'subscription') else False,
    }
    return render(request, 'training/category_trainings.html', context)


def training_detail(request, pk):
    """
    Displays the detail view of a single training video.
    
    - If the video is marked as free (training.is_free is True), any logged-in user can view it.
    - Otherwise, the user must have an active subscription.
    - If the user is not logged in, they are redirected to the login page.
    """
    training = get_object_or_404(Training, pk=pk)
    
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    # If the training video is free, allow access immediately.
    if training.is_free:
        return render(request, 'training/training_detail.html', {'training': training})
    
    # Otherwise, require an active subscription.
    try:
        subscription = request.user.subscription
        if subscription.active and subscription.expiry_date > timezone.now():
            return render(request, 'training/training_detail.html', {'training': training})
        else:
            return redirect('subscriptions:subscribe')
    except Subscription.DoesNotExist:
        return redirect('subscriptions:subscribe')


@staff_member_required
def training_list(request):
    """
    View for staff to see all training videos for management.
    """
    trainings = Training.objects.all().order_by('order', 'title')
    return render(request, 'training/training_list.html', {'trainings': trainings})


@staff_member_required
def create_training(request):
    """
    View for staff to create a new training video.
    """
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            try:
                storage = getattr(training.video_file, "storage", None)
                if storage:
                    print(
                        "STORAGE:",
                        storage.__class__.__name__,
                        getattr(storage, "bucket_name", ""),
                    )
                training.save()
                form.save_m2m()
                print("Saved key:", training.video_file.name)
            except Exception as exc:
                print("Save error:", exc)
                raise
            messages.success(
                request, 
                f'Training video "{training.title}" created successfully!'
            )
            return redirect('training:training_detail', pk=training.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainingForm()
    
    return render(request, 'training/training_form.html', {
        'form': form,
        'title': 'Create New Training Video',
        'button_text': 'Create Training'
    })


@staff_member_required
def edit_training(request, training_id):
    """
    View for staff to edit an existing training video.
    """
    training = get_object_or_404(Training, id=training_id)
    
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            training = form.save()
            messages.success(
                request, 
                f'Training video "{training.title}" updated successfully!'
            )
            return redirect('training:training_detail', pk=training.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainingForm(instance=training)
    
    return render(request, 'training/training_form.html', {
        'form': form,
        'training': training,
        'title': f'Edit {training.title}',
        'button_text': 'Update Training'
    })


@staff_member_required
def delete_training(request, training_id):
    """
    View for staff to delete a training video.
    """
    training = get_object_or_404(Training, id=training_id)
    
    if request.method == 'POST':
        training_title = training.title
        training.delete()
        messages.success(
            request, 
            f'Training video "{training_title}" has been deleted.'
        )
        return redirect('training:training_list')
    
    return render(request, 'training/training_confirm_delete.html', {
        'training': training
    })