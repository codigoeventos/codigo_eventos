from django.db import migrations, models
import django.db.models.deletion


def forward_copy_project_to_budget(apps, schema_editor):
    ART = apps.get_model('art', 'ART')
    HistoricalART = apps.get_model('art', 'HistoricalART')
    Budget = apps.get_model('budgets', 'Budget')

    budget_by_project = {}

    def get_budget_for_project(project_id):
        if not project_id:
            return None
        if project_id in budget_by_project:
            return budget_by_project[project_id]

        budget = (
            Budget.objects
            .filter(proposal_id=project_id)
            .order_by('-is_selected', '-created_at', 'id')
            .first()
        )
        budget_by_project[project_id] = budget.id if budget else None
        return budget_by_project[project_id]

    for art in ART.objects.filter(budget__isnull=True).exclude(project__isnull=True):
        budget_id = get_budget_for_project(art.project_id)
        if budget_id:
            art.budget_id = budget_id
            art.save(update_fields=['budget'])

    for hart in HistoricalART.objects.filter(budget__isnull=True).exclude(project__isnull=True):
        budget_id = get_budget_for_project(hart.project_id)
        if budget_id:
            hart.budget_id = budget_id
            hart.save(update_fields=['budget'])


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '__first__'),
        ('art', '0004_fields_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='budget',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='art',
                to='budgets.budget',
                verbose_name='Orçamento',
            ),
        ),
        migrations.AddField(
            model_name='historicalart',
            name='budget',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='budgets.budget',
                verbose_name='Orçamento',
            ),
        ),
        migrations.RunPython(forward_copy_project_to_budget, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='art',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicalart',
            name='project',
        ),
    ]
