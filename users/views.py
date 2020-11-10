from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post
from django.contrib.auth.forms import PasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "user/register.html", {'form':form})


@login_required
def profile(request):
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile_page': 'active',
        'most_recent': most_recent,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)

@login_required
def change_password(request):
    if request.method =="POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your password has been changed')
            return redirect('profile')

    else:
        form = PasswordChangeForm(user=request.user)
    context = {
            'form': form
        }
    return render(request, 'user/change_password.html', context) 

        
