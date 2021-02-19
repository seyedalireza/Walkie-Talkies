from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from .models import Classroom


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

