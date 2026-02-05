"""Core app views."""

from rest_framework import viewsets, permissions
from .models import ExampleModel
from .serializers import ExampleModelSerializer


class ExampleModelViewSet(viewsets.ModelViewSet):
    """ViewSet para ExampleModel."""
    
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Define o owner como o usuário autenticado."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Retorna apenas os exemplos do usuário autenticado."""
        if self.request.user.is_staff:
            return ExampleModel.objects.all()
        return ExampleModel.objects.filter(owner=self.request.user)
