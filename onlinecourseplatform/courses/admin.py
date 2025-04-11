from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_published', 'created_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:  # Only allow non-superusers to see published courses
            queryset = queryset.filter(is_published=True)
        return queryset
