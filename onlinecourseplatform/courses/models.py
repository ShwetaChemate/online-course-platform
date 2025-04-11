from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PublishedCourseManager(models.Manager):
    def get_queryset(self):
        return super(PublishedCourseManager, self).get_queryset().filter(is_published=True)

class PublishedCourse(Course):
    objects = PublishedCourseManager()
    class Meta:
        proxy = True
        verbose_name = 'Published Course'


