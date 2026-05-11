from django.db import migrations


def fix_approved_status(apps, schema_editor):
    """Migrate any remaining 'approved' status to 'confirmed'."""
    Budget = apps.get_model('budgets', 'Budget')
    Budget.objects.filter(status='approved').update(status='confirmed')


def reverse_fix(apps, schema_editor):
    """Reverse migration - not recommended."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0022_budget_proposal_nullable'),
    ]

    operations = [
        migrations.RunPython(fix_approved_status, reverse_fix),
    ]
