from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, PublishedCourseViewSet
from . import views

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('published-courses', PublishedCourseViewSet)

urlpatterns = [
    path('', views.home, name='home'),  # Login page
    # path('non-admin/', views.redirect_to_courses, name='redirect_to_courses'),
    path('non-admin/courses/', views.non_admin_course_view, name='non_admin_course_list'),
    #path('non-admin/', views.CourseViewSet.get_queryset),
    path('non-admin/courses/', include(router.urls)),
]

