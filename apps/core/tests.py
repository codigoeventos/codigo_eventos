"""Core app tests."""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ExampleModel


class ExampleModelTestCase(TestCase):
    """Testes para o modelo ExampleModel."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.example = ExampleModel.objects.create(
            title='Teste',
            description='Descrição de teste',
            owner=self.user
        )

    def test_example_creation(self):
        """Testa a criação de um exemplo."""
        self.assertEqual(self.example.title, 'Teste')
        self.assertEqual(self.example.owner, self.user)
        self.assertTrue(self.example.is_active)

    def test_example_str(self):
        """Testa o método __str__."""
        self.assertEqual(str(self.example), 'Teste')


class ExampleModelAPITestCase(APITestCase):
    """Testes para a API de ExampleModel."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_examples(self):
        """Testa a listagem de exemplos."""
        ExampleModel.objects.create(
            title='Exemplo 1',
            owner=self.user
        )
        response = self.client.get('/api/examples/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_example(self):
        """Testa a criação de um exemplo."""
        data = {
            'title': 'Novo Exemplo',
            'description': 'Descrição do novo exemplo'
        }
        response = self.client.post('/api/examples/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExampleModel.objects.count(), 1)
