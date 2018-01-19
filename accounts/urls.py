from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'sign_in/$', views.sign_in, name='sign_in'),
    re_path(r'sign_up/$', views.sign_up, name='sign_up'),
    re_path(r'sign_out/$', views.sign_out, name='sign_out'),
    re_path(r'profile/$', views.profile, name='profile'),
    re_path(r'profile/edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'profile/change_avatar/$', views.edit_avatar, name='edit_avatar'),
    re_path(r'profile/change_avatar/rotate', views.rotate_image, name='rotate_image'),
    re_path(r'profile/change_avatar/crop', views.crop_image, name='crop_image'),
    re_path(r'profile/change_avatar/flip', views.flip_image, name='flip_image'),
    re_path(r'profile/change_password/$', views.edit_password, name='edit_password'),
]
