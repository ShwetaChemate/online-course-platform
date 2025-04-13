from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Course, PublishedCourse
from .serializers import CourseSerializer, PublishedCourseSerializer
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from .permissions import IsAdminOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Course.objects.all()
        return Course.objects.filter(is_published=True)

class PublishedCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishedCourse.objects.all()
    serializer_class = PublishedCourseSerializer

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')  # Django admin
            else:
                return redirect('/non-admin/courses')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'home.html')  # Login form

@api_view(['GET'])
def non_admin_course_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        courses = Course.objects.all()  # Admins/staff can see all courses
    else:
        courses = Course.objects.filter(is_published=True)  # Non-admins only see published ones
    serializer = CourseSerializer(courses, many=True)
    return render(request, 'non_admin/published_course_list.html', {'courses': serializer.data})

