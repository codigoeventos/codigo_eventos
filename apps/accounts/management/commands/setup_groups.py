"""
Management command to create/sync user groups and their permissions.
Run in any environment: python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


GROUPS = {
    'Administrador': [
        'add_user', 'change_user', 'delete_user', 'view_user',
        'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
        'add_group', 'change_group', 'delete_group', 'view_group',
        'add_permission', 'change_permission', 'delete_permission', 'view_permission',
        'add_budget', 'change_budget', 'delete_budget', 'view_budget',
        'add_budgetitem', 'change_budgetitem', 'delete_budgetitem', 'view_budgetitem',
        'add_historicalbudget', 'change_historicalbudget', 'delete_historicalbudget', 'view_historicalbudget',
        'add_client', 'change_client', 'delete_client', 'view_client',
        'add_historicalclient', 'change_historicalclient', 'delete_historicalclient', 'view_historicalclient',
        'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
        'add_eventdocument', 'change_eventdocument', 'delete_eventdocument', 'view_eventdocument',
        'add_event', 'change_event', 'delete_event', 'view_event',
        'add_historicalevent', 'change_historicalevent', 'delete_historicalevent', 'view_historicalevent',
        'add_historicalproposal', 'change_historicalproposal', 'delete_historicalproposal', 'view_historicalproposal',
        'add_proposal', 'change_proposal', 'delete_proposal', 'view_proposal',
        'add_historicalserviceorder', 'change_historicalserviceorder', 'delete_historicalserviceorder', 'view_historicalserviceorder',
        'add_serviceorder', 'change_serviceorder', 'delete_serviceorder', 'view_serviceorder',
        'add_serviceorderitem', 'change_serviceorderitem', 'delete_serviceorderitem', 'view_serviceorderitem',
        'add_session', 'change_session', 'delete_session', 'view_session',
        'add_eventteam', 'change_eventteam', 'delete_eventteam', 'view_eventteam',
        'add_teammember', 'change_teammember', 'delete_teammember', 'view_teammember',
        'add_historicaltechnicalvisit', 'change_historicaltechnicalvisit', 'delete_historicaltechnicalvisit', 'view_historicaltechnicalvisit',
        'add_technicalvisit', 'change_technicalvisit', 'delete_technicalvisit', 'view_technicalvisit',
        'add_technicalvisitattachment', 'change_technicalvisitattachment', 'delete_technicalvisitattachment', 'view_technicalvisitattachment',
    ],
    'Comercial': [
        'add_budget', 'change_budget', 'view_budget',
        'add_budgetitem', 'change_budgetitem', 'view_budgetitem',
        'add_historicalbudget', 'change_historicalbudget', 'view_historicalbudget',
        'add_client', 'change_client', 'view_client',
        'add_historicalclient', 'change_historicalclient', 'view_historicalclient',
        'add_event', 'change_event', 'view_event',
        'add_historicalevent', 'change_historicalevent', 'view_historicalevent',
        'add_historicalproposal', 'change_historicalproposal', 'view_historicalproposal',
        'add_proposal', 'change_proposal', 'view_proposal',
    ],
    'Operacional': [
        'add_eventdocument', 'change_eventdocument', 'view_eventdocument',
        'add_event', 'change_event', 'view_event',
        'add_historicalevent', 'change_historicalevent', 'view_historicalevent',
        'add_historicalserviceorder', 'change_historicalserviceorder', 'view_historicalserviceorder',
        'add_serviceorder', 'change_serviceorder', 'view_serviceorder',
        'add_serviceorderitem', 'change_serviceorderitem', 'view_serviceorderitem',
        'add_eventteam', 'change_eventteam', 'view_eventteam',
        'add_teammember', 'change_teammember', 'view_teammember',
    ],
    'Técnico': [
        'add_event', 'change_event', 'view_event',
        'add_historicalevent', 'change_historicalevent', 'view_historicalevent',
        'add_historicaltechnicalvisit', 'change_historicaltechnicalvisit', 'view_historicaltechnicalvisit',
        'add_technicalvisit', 'change_technicalvisit', 'view_technicalvisit',
        'add_technicalvisitattachment', 'change_technicalvisitattachment', 'view_technicalvisitattachment',
    ],
    'Financeiro': [],
}


class Command(BaseCommand):
    help = 'Create or update user groups with their permissions.'

    def handle(self, *args, **options):
        # Build a lookup of codename → Permission for efficiency
        all_perms = {p.codename: p for p in Permission.objects.all()}

        for group_name, codenames in GROUPS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            action = 'Criado' if created else 'Atualizado'

            perms_to_assign = []
            missing = []
            for codename in codenames:
                if codename in all_perms:
                    perms_to_assign.append(all_perms[codename])
                else:
                    missing.append(codename)

            group.permissions.set(perms_to_assign)

            self.stdout.write(
                self.style.SUCCESS(f'{action}: {group_name} ({len(perms_to_assign)} permissões)')
            )
            if missing:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠  Permissões não encontradas: {", ".join(missing)}')
                )

        self.stdout.write(self.style.SUCCESS('\nGrupos configurados com sucesso!'))
