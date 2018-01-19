from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

from PIL import Image
from . models import Profile
from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "Success! Account created. You are signed in."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    """User profile view to display user details"""
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile(request):
    """Edit view for both User & Profile forms of user details"""

    if request.method == 'POST':
        user_form = forms.EditUserForm(request.POST, instance=request.user)
        profile_form = forms.EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            print(settings.MEDIA_ROOT)
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile successfully updated!')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.error(request, 'Please correct the error below')
    else:
        user_form = forms.EditUserForm(instance=request.user)
        profile_form = forms.EditProfileForm(instance=request.user.profile)
    return render(request, 'accounts/change_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def edit_password(request):
    """Edit view for password"""
    user = request.user
    form = forms.EditPasswordForm(user)
    if request.method == 'POST':
        form = forms.EditPasswordForm(data=request.POST, user=user)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully changed!')
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def edit_avatar(request):
    """Edit profile avatar"""

    form = forms.EditAvatarForm(instance=request.user.profile)
    if request.method == 'POST':
        form = forms.EditAvatarForm(request.POST,
                                    instance=request.user.profile,
                                    files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Avatar changes saved!")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/change_avatar.html', {'form': form})


@login_required
def rotate_image(request):
    with Image.open(request.user.profile.avatar.path) as image:
        image = image.transpose(Image.ROTATE_270)
        image.save(request.user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def flip_image(request):
    with Image.open(request.user.profile.avatar.path) as image:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        image.save(request.user.profile.avatar.path)
    return HttpResponseRedirect(reverse('accounts:edit_avatar'))


@login_required
def crop_image(request):
    form = forms.EditCropForm(user=request.user)
    with Image.open(request.user.profile.avatar.path) as image:
        width, heigth = image.size
        size = str(width) + 'x' + str(heigth)
        if request.method == 'POST':
            form = forms.EditCropForm(user=request.user, data=request.POST)
            if form.is_valid():
                box = (int(form.cleaned_data['left']),
                       int(form.cleaned_data['top']),
                       int(form.cleaned_data['right']),
                       int(form.cleaned_data['bottom']),
                       )
                image = image.crop(box)
                image.save(request.user.profile.avatar.path)
                return HttpResponseRedirect(reverse('accounts:edit_avatar'))
        return render(request, 'accounts/change_avatar.html', {'form': form, 'size': size})
