from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from .models import Forum, Classroom


class ForumModelTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(username="rezaasdaa1111", password="whatsupbody")
        user1.save()

        math_class = Classroom.objects.create(lesson="math", grade="twelve science",
                                              class_num=100, description="Hi")
        math_class.save()
        forum = Forum.objects.create(classroom=math_class, title="Hi", description="Alooo")
        forum.save()

    def test_classroom(self):
        obj = Classroom.objects.get(lesson="math")
        self.assertIsNotNone(obj)
        self.assertEqual(obj.class_num, 100)
        self.assertEqual(obj.description, "Hi")
        self.assertEqual(obj.grade, "twelve science")

    def test_forum(self):
        obj = Forum.objects.get(description="Alooo")
        self.assertIsNotNone(obj)
        self.assertEqual(obj.description, "Alooo")
        self.assertEqual(obj.classroom.lesson, "math")


class CreateClassTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="firstName", password="whatsupbody")
        user1.save()
        cls = Classroom.objects.create(lesson="l1", grade="20", class_num=1, description="nothing", teacher=user1)
        cls.save()

    def test_create_class_successfully(self):
        classes = Classroom.objects.all()
        self.assertEqual(len(classes), 1)


class JoinClassTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="firstName", password="whatsupbody")
        user1.save()
        user2 = User.objects.create(username="firstName2", password="whatsupbody2")
        user2.save()
        cls = Classroom.objects.create(lesson="l1", grade="20", class_num=1, description="nothing", teacher=user1)
        cls.students.add(user2)
        cls.save()

    def test_join_class_successfully(self):
        classes = Classroom.objects.all()
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].students.count(), 1)
