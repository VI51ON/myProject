"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from posts.views import index, blog, post, services, serviceDetails, about, contact_us, search, thankyou, events, post_update, post_delete, post_create, error_404, donation, charge
from users import views as user_views
from marketing.views import email_list_signup


urlpatterns = [
    path('admin/', admin.site.urls),


    path('', index, name="index"),


    path('donation/', donation, name='donation'),


    path('charge/', charge, name='charge'),


    path('about/', about, name='about-us'),


    path('blog/', blog, name='post-list'),


    path('search/', search, name='search'),


    path('subscribe/', email_list_signup, name='subscribe'),


    path('contact_us/', contact_us, name='contact_us'),


    path('events/', events, name='events'),


    path('post/<id>/', post, name='post-detail'),


    path('create/', post_create, name='post-create'),


    path('post/<id>/update/', post_update, name='post-update'),


    path('post/<id>/delete', post_delete, name='post-delete'),


    path('services/', services, name='services'),


    path('register/', user_views.register, name='register'),


    path('profile/', user_views.profile, name='profile'),


    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),


    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


    path('password-reset/', 
    auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), 
    name='password_reset'),


    path('password-reset/done/', 
    auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
    name='password_reset_done'),


    path('password-reset-confirm/<uidb64>/<token>', 
    auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
    name='password_reset_confirm'),


    path('password-reset-complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
    name='password_reset_complete'),

    path('change-password/', user_views.change_password, name="change_password"),


    path('thankyou/', thankyou, name='thankyou'),


    path('serviceDetails/<id>/', serviceDetails, name='service-detail'),


    path('tinymce/', include('tinymce.urls')),


    path('oauth/', include('social_django.urls', namespace="social")),
]

handler404 = 'posts.views.error_404'
admin.site.site_header = 'Supreme Security'
admin.site.site_title = 'Supreme Security'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
