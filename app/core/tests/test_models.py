from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_successfull_email(self):
        """Test create a user with successfull email"""
        email = 'test@example.com'
        password = 'Password'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(
            user.check_password(password)
        )

    def test_create_user_with_case_insensitive_email(self):
        """Test create a user with case insensitive email"""
        email = "Test@EXAMPLE.com"
        password = 'Password'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, 'Test@example.com')

    def test_new_user_with_invalid_email(self):
        """Test create a user without email provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Password')

    def test_create_new_superuser(self):
        """Test create a superuser"""
        user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            'Password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
