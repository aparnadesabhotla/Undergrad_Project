from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from user import models as user_models
from django.contrib.auth import models as auth_models
from user.forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'An account was successfully created for {username}')
            register_form.save()
            return redirect('user:register')
        else:
            messages.error(request, f'An account was not created. Check out the red alerts below the fields and try again.')
    else:
        register_form = RegisterForm()
    context = {'register_form': register_form}
    template = 'user/register.html'
    return render(request, template, context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('blog:question-index')
        else:
            messages.error(request, f'Username or Password was invalid.')
    else:
        login_form = LoginForm()
    context = {'login_form': login_form}
    template = 'user/login.html'
    return render(request, template, context)


def logout(request):
    username = request.user
    auth_logout(request)
    context = {'username': username}
    template = 'user/logout.html'
    return render(request, template, context)


def profile(request, user_id):
    if request.method == 'POST':
        if request.user.id == user_id:
            user_update_form = UserUpdateForm(request.POST, instance=request.user)
            profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_update_form.is_valid() and profile_update_form.is_valid():
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, f'Your profile has been updated')
                return redirect('user:profile', user_id)
        else:
            template = 'user/permission_denied.html'
            return render(request, template)
    else:
        url_user = get_object_or_404(auth_models.User, pk=user_id)
        user_update_form = UserUpdateForm(instance=url_user)
        if not hasattr(url_user, 'profile'):
            user_models.Profile.objects.create(user=url_user)
        profile_update_form = ProfileUpdateForm(instance=url_user.profile)
    context = {
        'url_user': url_user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    template = 'user/profile.html'
    return render(request, template, context)
 