from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from app_users import views
from app_users.views import *

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('validate-username', views.ajax_username, name='ajax-username'),

    path('login', LoginUser.as_view(), name='login'),
    path('validate-login', views.ajax_login, name='ajax-login'),

    path('logout', logout_view, name='logout'),
    # path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    re_path(r'^profile/(\d+)/$', UserDetailView, name='profile'),
    re_path(r'^profile/(\d+)/statistics$', profile_statistics, name='profile_statistics'),

    path('profile-update/<int:pk>', UserUpdateView.as_view(), name='profile-update'),
    path('change-pass/<int:pk>', ChangePassView.as_view(), name='change-pass'),

    path('status-update/<int:pk>', StatusUserUpdateView.as_view(), name='status-update'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    # url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    # url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
    #     'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    # url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
    #     name='password_reset_complete'),
]
