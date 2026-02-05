"""Core app serializers."""

from rest_framework import serializers
from .models import ExampleModel


class ExampleModelSerializer(serializers.ModelSerializer):
    """Serializer para ExampleModel."""
    
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = ExampleModel
        fields = ['id', 'title', 'description', 'is_active', 'owner', 'owner_username', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
