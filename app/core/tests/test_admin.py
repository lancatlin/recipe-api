from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setup(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='Password'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='Password',
            name='user'
        )

    def test_users_listed(self):
        """Test if users are listed on the admin site"""
        url = reverse('admin:core_user_changellist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
