from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from orders.models import Order
from django.contrib.auth.models import User

@login_required
def profile_dashboard(request):
    # Get the current user's profile (available via the OneToOne relation)
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by('-created')  

    context = {
        'profile': profile,
        'orders': orders,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def edit_profile(request):
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
