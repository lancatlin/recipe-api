from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test the publicly available recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to use this api"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test ingredients can be retrived by authenticated user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retriving the list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Egg')
        Ingredient.objects.create(user=self.user, name='Apple')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@example.com', 'testpass')
        Ingredient.objects.create(user=user2, name='Beef')
        ingredient = Ingredient.objects.create(user=self.user, name='Pork')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating ingredient"""
        payload = {'name': 'Egg'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)