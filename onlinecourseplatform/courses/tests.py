from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from courses.serializers import CourseSerializer, PublishedCourseSerializer
from .models import Course,PublishedCourse
from .admin import CourseAdmin

class CourseViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin-password')
        self.non_admin_user = User.objects.create_user(username='nonadmin', password='non-adminpassword')

        self.published_course = Course.objects.create(title='Anne Frank', description='Biopic', is_published=True)
        self.unpublished_course = Course.objects.create(title='Chacha Nehru', description='Former Prime Minister', is_published=False)

    def test_non_admin_can_see_only_published_courses(self):
        self.client.login(username='nonadmin', password='non-adminpassword')
        response = self.client.get(reverse('non_admin_course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anne Frank')
        self.assertNotContains(response, 'Chacha Nehru')

    def test_admin_can_see_all_courses(self):
        self.client.login(username='admin', password='admin-password')
        response = self.client.get(reverse('non_admin_course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anne Frank')
        self.assertContains(response, 'Chacha Nehru')

class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test-password')

    def test_logout_action_redirects_to_home_page(self):
        self.client.login(username='testuser', password='test-password')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'testuser')

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(title='Alice in Wonderland', description='Test Description', is_published=True)
        self.assertEqual(course.title, 'Alice in Wonderland')
        self.assertEqual(course.description, 'Test Description')
        self.assertTrue(course.is_published)

    def test_unpublished_course(self):
        course = Course.objects.create(title='King Charles', description='King of England', is_published=False)
        self.assertEqual(course.is_published, False)

class CourseAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

        Course.objects.create(title='Anne Frank', description='Biopic', is_published=True)
        Course.objects.create(title='King Charles', description='King of England', is_published=False)

        self.superUser = User.objects.create_superuser(username='adminUser', email='admin@test.com', password='admin@123')
        self.staffUser = User.objects.create_user(username='staffUser', email='staff@test.com', password='staff@123', is_staff=True)
        self.normalUser = User.objects.create_user(username='user', email='user@test.com', password='user@123')

    def test_superuser_can_view_all_courses(self):
        request = self.factory.get('/admin/courses/course/')
        request.user = self.superUser
        admin_instance = CourseAdmin(Course, self.site)
        queryset = admin_instance.get_queryset(request)
        self.assertEqual(queryset.count(), 2)

    def test_staff_sees_all_courses(self):
        request = self.factory.get('/admin/courses/course/')
        request.user = self.staffUser
        admin_instance = CourseAdmin(Course, self.site)
        queryset = admin_instance.get_queryset(request)
        self.assertEqual(queryset.count(), 2)

    def test_normal_user_sees_only_published_courses(self):
        request = self.factory.get('/admin/courses/course/')
        request.user = self.normalUser
        admin_instance = CourseAdmin(Course, self.site)
        queryset = admin_instance.get_queryset(request)
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(queryset.first().is_published)

class PublishedCourseModelTest(TestCase):
    def setUp(self):
        Course.objects.create(title='Published course 1', description='desc1', is_published=True)
        Course.objects.create(title='Published course 2', description='desc2', is_published=True)
        Course.objects.create(title='Unpublished course', description='desc3', is_published=False)

    def test_only_published_courses_are_returned(self):
        published_courses = PublishedCourse.objects.all()
        self.assertEqual(published_courses.count(), 2)
        for course in published_courses:
            self.assertTrue(course.is_published)

    def test_str_method_returns_title(self):
        course = PublishedCourse.objects.first()
        self.assertEqual(str(course), course.title)

    def test_proxy_model_inherits_from_course(self):
        course = PublishedCourse.objects.first()
        self.assertIsInstance(course, Course)
        self.assertIsInstance(course, PublishedCourse)

class CourseSerializerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            description="Test description",
            is_published=True
        )

    def test_course_serialization(self):
        serializer = CourseSerializer(self.course)
        data = serializer.data
        self.assertEqual(data['title'], self.course.title)
        self.assertEqual(data['description'], self.course.description)
        self.assertEqual(data['is_published'], self.course.is_published)

    def test_course_deserialization_valid(self):
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'is_published': False
        }
        serializer = CourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        course = serializer.save()
        self.assertEqual(course.title, data['title'])

    def test_course_deserialization_invalid(self):
        data = {
            'title': '',
            'description': 'description',
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors) # as title is required it will throw error


class PublishedCourseSerializerTest(TestCase):
    def setUp(self):
        self.published_course = PublishedCourse.objects.create(
            title="Published Course",
            description="Published course description",
            is_published=True
        )

    def test_published_course_serialization(self):
        serializer = PublishedCourseSerializer(self.published_course)
        data = serializer.data
        self.assertEqual(data['title'], self.published_course.title)
        self.assertTrue(data['is_published'])

    def test_only_serializes_published_courses(self):
        unpublished = Course.objects.create(
            title="Unpublished course",
            description="description",
            is_published=False
        )
        published_courses = PublishedCourse.objects.all()
        self.assertNotIn(unpublished, published_courses)

class URLRoutingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='normaluser', password='pass1234')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')

        Course.objects.create(title="Published 1", description="Desc", is_published=True)
        Course.objects.create(title="Unpublished", description="Desc", is_published=False)

    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_home(self):
        self.client.login(username='normaluser', password='pass1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_course_viewset_json_response(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_published_courses_viewset_json(self):
        response = self.client.get('/published-courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')





