"""
Management command to create default user groups for RBAC.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create default user groups with appropriate permissions'

    def handle(self, *args, **kwargs):
        # Define groups and their permissions
        groups_config = {
            'Administrador': {
                'description': 'Acesso total exceto gestão de usuários',
                'apps': ['clients', 'events', 'projects', 'budgets', 'service_orders', 'technical_visits', 'contractors', 'logistics', 'documents'],
                'permissions': ['view', 'add', 'change', 'delete']
            },
            'Comercial': {
                'description': 'Acesso a orçamentos, OS, eventos, projetos e clientes',
                'apps': ['clients', 'events', 'projects', 'budgets', 'service_orders'],
                'permissions': ['view', 'add', 'change']
            },
            'Financeiro': {
                'description': 'Acesso de visualização a tudo, dashboard financeiro',
                'apps': ['clients', 'events', 'projects', 'budgets', 'service_orders', 'technical_visits', 'contractors', 'logistics', 'documents'],
                'permissions': ['view']
            },
        }

        for group_name, config in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if config.get('permissions') == 'all':
                # Administrador gets all permissions
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Grupo "{group_name}" criado/atualizado com todas as permissões')
                )
            else:
                # Clear existing permissions
                group.permissions.clear()
                
                # Add permissions for specified apps
                for app_label in config.get('apps', []):
                    content_types = ContentType.objects.filter(app_label=app_label)
                    
                    for perm_type in config.get('permissions', []):
                        permissions = Permission.objects.filter(
                            content_type__in=content_types,
                            codename__startswith=perm_type
                        )
                        group.permissions.add(*permissions)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Grupo "{group_name}" criado/atualizado ({config["description"]})'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Todos os grupos foram criados com sucesso!'))
