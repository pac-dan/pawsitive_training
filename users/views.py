from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from orders.models import Order
from subscriptions.models import Subscription


@login_required
def profile_dashboard(request):
    """ A view to return the user's profile dashboard """
    # Ensure the user has a profile
    if not hasattr(request.user, 'profile'):
        from .models import Profile
        Profile.objects.create(user=request.user)
    
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        subscription = None

    # Compute active status using our model method
    subscription_active = subscription.is_active() if subscription else False
    orders = Order.objects.filter(user=request.user).order_by('-created')
    context = {
        'profile': request.user.profile, 
        'subscription': subscription,
        'subscription_active': subscription_active,
        'orders': orders,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def edit_profile(request):
    """ A view to handle the user's profile editing """
    
    # Check if the user has an active subscription
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'users/edit_profile.html', {'form': form})
