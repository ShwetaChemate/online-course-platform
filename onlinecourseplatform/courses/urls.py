from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, PublishedCourseViewSet, home, non_admin_course_view
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('published-courses', PublishedCourseViewSet, basename='publishedcourse')

urlpatterns = [
    path('', home, name='home'),  # Login/Home page
    path('non-admin/courses', non_admin_course_view, name='non_admin_course_list'),
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
]