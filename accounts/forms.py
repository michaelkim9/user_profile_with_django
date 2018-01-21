from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       PasswordChangeForm)
from django.core import validators
from django.utils.safestring import mark_safe
from django_countries.widgets import CountrySelectWidget

from PIL import Image
from tinymce.widgets import TinyMCE
from django.core.files import File
import re


from . import models


class SignUpForm(UserCreationForm):
    """Using django's built-in template for user sign up"""
    verify_email = forms.EmailField(label='Verify email', required=True)

    class Meta:
        model = models.User
        fields = [
            'username',
            'email',
            'verify_email',
            'password1',
            'password2'
        ]

    def cleaned(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                    'Try again. Make sure your emails match'
                )


class EditUserForm(forms.ModelForm):
    """Edit profile form, includes email verification, excludes password"""

    # Add fields not in Profile Model here
    verify_email = forms.EmailField(label='Please verify your email',
                                    required=True)

    class Meta:
        model = models.User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'verify_email',
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                'Try again. Make sure your emails match'
            )


class EditProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
                            input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
                            required=False,
                            widget=forms.DateInput(attrs={'id': 'birth_date'})
                            )

    bio = forms.CharField(widget=TinyMCE(attrs={'rows': 80}),
                          required=False,
                          min_length=10)

    widgets = {'country': CountrySelectWidget()}

    class Meta:
        model = models.Profile
        fields = [
            'birth_date',
            'avatar',
            'country',
            'city',
            'hobby',
            'bio',
        ]


class EditPasswordForm(forms.Form):
    """Edit Password Form"""
    min_length = 14

    # create the fields required for password reset
    old_password = forms.CharField(widget=forms.PasswordInput(),
                                   label='Old Password')

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'data-indicator': 'pwindicator',
               'id': 'new_password',
               'id_for_label': 'new_password'}),
        label='New Password')

    new_password2 = forms.CharField(widget=forms.PasswordInput(),
                                    label='Confirm New Password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = mark_safe(
            '<ul>'
            '<li>Must not be the same as current password</li>\n'
            '<li>Minimum length 14 characters</li>\n'
            '<li>Must contain uppercase and lowercase letters</li>\n'
            '<li>Must include one or more numerical digits</li>\n'
            '<li>Must include one or more of special characters @ # $</li>\n'
            '<li>Cannot contain the username, first or last name</li>\n'
            '</ul>'
        )

    # Check for password additional validations in clean method
    def clean(self):
        cleaned_data = super(EditPasswordForm, self).clean()

        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        # check if old password is correct
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Current Password Incorrect!')

        # Check new password not equal to current password
        if new_password1 == old_password:
            raise forms.ValidationError("New Password cannot"
                                        "be same as Old Password")

        # Check for minimum length
        if len(new_password1) < self.min_length:
            raise forms.ValidationError("Password must be at least"
                                        "{} characters".format(self.min_length)
                                        )

        # check for upper and lower case letters
        if (not re.search(r'([a-z])+', new_password1) or
                not re.search(r'[A-Z]+', new_password1)):
            raise forms.ValidationError("New password must contain "
                                        "Uppercase and Lowercase letters.")

        # check new password contains special characters
        if not re.search(r'\d+', new_password1):
            raise forms.ValidationError("The new password must include at "
                                        "least one number.")

        # check for special characters
        if not re.search(r'([@#$])+', new_password1):
            raise forms.ValidationError(
                "Password must contain one of the following @, #, $.")

        # check that password is not part of username or full name
        user_first = self.user.first_name.lower()
        user_last = self.user.last_name.lower()
        user_username = self.user.username.lower()

        # if user provided first and last name then run this validation
        # first_name and last_name are not required inputs
        if user_first or user_last:
            if (user_first in new_password1.lower() or
                    user_last in new_password1.lower() or
                    user_username in new_password1.lower()):
                raise forms.ValidationError(
                    "New password cannot contain "
                    "parts of your username or full name."
                                            )
        else:
            pass

        # check that password confirmation matches
        if new_password1 != new_password2:
            raise forms.ValidationError(
                "Passwords must match"
            )

        return cleaned_data


class EditAvatarForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('avatar',)


class EditCropForm(forms.Form):
    left = forms.CharField()
    top = forms.CharField()
    right = forms.CharField()
    bottom = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditCropForm, self).__init__(*args, **kwargs)

    def clean(self):
        with Image.open(self.user.profile.avatar.path) as image:
            width, height = image.size

            left = int(self.cleaned_data['left'])
            top = int(self.cleaned_data['top'])
            right = int(self.cleaned_data['right'])
            bottom = int(self.cleaned_data['bottom'])

            max_left = width - right
            max_top = height - bottom

            if (left >= max_left
                    or top >= max_top
                    or left >= width
                    or top >= height
                    or right > width
                    or bottom > height
                    or left < 0
                    or top < 0
                    or right <= 0
                    or bottom <= 0):
                raise forms.ValidationError("Cropping box is not valid.")
