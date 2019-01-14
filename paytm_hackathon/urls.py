"""paytm_hackathon URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from home import views
from home.views import Home, SignUp, activity, Profile, Book, BookNow, Doctor
from paytm_hackathon import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('logout/', views.user_logout, name='logout'),
    path('activity/', activity.as_view(), name='activity'),
    path('profile/', Profile.as_view(), name='profile'),
    path('book/', Book.as_view(), name='book'),
    path('booknow/', BookNow.as_view(), name='booknow'),
    url(r'^send/', views.sms),
    path('doctor-dashboard/', Doctor.as_view(), name='doctor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)