from django.test import TestCase
# Create your tests here.
from .models import Profile


class ProfileTestCase(TestCase):
    def test_login(self):
        # user1 = Profile.objects.get(pk=1)
        self.assertEqual(3, 3)