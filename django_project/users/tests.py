from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from .models import Profile


class UsersTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="rezaasdaa1111", password="whatsupbody")
        user1.save()

        user2 = User.objects.create(username="mohsen1111", password="whatsupbody")
        user2.save()

        user3 = User.objects.create(username="saeid1111", password="whatsupbody2")
        user3.save()

    def test_db(self):
        profs = Profile.objects.all()
        self.assertEqual(len(profs), 3)
        self.assertNotEqual(profs[0].user.username, profs[1].user.username)
        self.assertEqual(profs[1].user.password, profs[1].user.password)

    def test_types(self):
        profs = Profile.objects.all()
        self.assertNotEqual(profs[0].type, 'teacher')
        self.assertEqual(profs[1].type, 'student')
        self.assertEqual(profs[1].type, profs[2].type)
