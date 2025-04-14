from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django main admin site
    path('', include('courses.urls')),  # home and normal user routing
]

