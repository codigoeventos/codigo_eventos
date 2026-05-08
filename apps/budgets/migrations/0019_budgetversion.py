from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0018_budgetnotification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField(verbose_name='Número da Versão')),
                ('label', models.CharField(
                    blank=True,
                    max_length=255,
                    verbose_name='Rótulo',
                    help_text='Nome curto opcional para identificar esta versão',
                )),
                ('snapshot', models.JSONField(
                    verbose_name='Snapshot',
                    help_text='Cópia completa dos dados da proposta neste momento',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('budget', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='versions',
                    to='budgets.budget',
                    verbose_name='Proposta',
                )),
                ('created_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='budget_versions_created',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Criado por',
                )),
            ],
            options={
                'verbose_name': 'Versão da Proposta',
                'verbose_name_plural': 'Versões da Proposta',
                'ordering': ['-version_number'],
                'unique_together': {('budget', 'version_number')},
            },
        ),
    ]
