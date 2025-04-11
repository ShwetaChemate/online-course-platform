from rest_framework import serializers
from .models import Course, PublishedCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # Serialize all fields in Course model

class PublishedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishedCourse
        fields = '__all__'  # Serialize all fields in PublishedCourse model
