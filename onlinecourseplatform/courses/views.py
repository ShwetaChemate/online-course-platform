from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Course, PublishedCourse
from .serializers import CourseSerializer, PublishedCourseSerializer
from .permissions import IsAdminUser
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            # Normal users see only published ones
            return Course.objects.filter(is_published=True)
        return Course.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]  # Anyone can view (but see queryset above)

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

# @login_required
# def normal_user_page(request):
#     return HttpResponse("🌟 Welcome, normal user!")

# def redirect_to_courses(request):
#     return redirect('/non-admin/courses/')

def non_admin_course_view(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'non_admin/course_list.html', {'courses': courses})


