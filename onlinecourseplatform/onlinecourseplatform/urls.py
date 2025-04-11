from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin site
    path('', include('courses.urls')),  # home + normal user route
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

