# Updated: FK changed from proposals.Proposal to projects.Project

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Budget',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                        ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                        ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                        ('name', models.CharField(help_text='Nome identificador deste orcamento', max_length=255, verbose_name='Nome')),
                        ('status', models.CharField(choices=[('draft', 'Rascunho'), ('sent', 'Enviado'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado')], default='draft', max_length=10, verbose_name='Status')),
                        ('is_selected', models.BooleanField(default=False, help_text='Orcamento escolhido pelo cliente', verbose_name='Selecionado')),
                        ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                        ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='projects.project', verbose_name='Projeto')),
                        ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                    ],
                    options={
                        'verbose_name': 'Orcamento',
                        'verbose_name_plural': 'Orcamentos',
                        'ordering': ['-created_at'],
                    },
                ),
                migrations.CreateModel(
                    name='BudgetItem',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=255, verbose_name='Item')),
                        ('description', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                        ('quantity', models.IntegerField(default=1, verbose_name='Quantidade')),
                        ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preco Unitario')),
                        ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Preco Total')),
                        ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='budgets.budget', verbose_name='Orcamento')),
                    ],
                    options={
                        'verbose_name': 'Item do Orcamento',
                        'verbose_name_plural': 'Itens do Orcamento',
                        'ordering': ['budget', 'id'],
                    },
                ),
                migrations.CreateModel(
                    name='HistoricalBudget',
                    fields=[
                        ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                        ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                        ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                        ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Criado em')),
                        ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Atualizado em')),
                        ('name', models.CharField(help_text='Nome identificador deste orcamento', max_length=255, verbose_name='Nome')),
                        ('status', models.CharField(choices=[('draft', 'Rascunho'), ('sent', 'Enviado'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado')], default='draft', max_length=10, verbose_name='Status')),
                        ('is_selected', models.BooleanField(default=False, help_text='Orcamento escolhido pelo cliente', verbose_name='Selecionado')),
                        ('history_id', models.AutoField(primary_key=True, serialize=False)),
                        ('history_date', models.DateTimeField(db_index=True)),
                        ('history_change_reason', models.CharField(max_length=100, null=True)),
                        ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                        ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                        ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                        ('proposal', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='projects.project', verbose_name='Projeto')),
                        ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                    ],
                    options={
                        'verbose_name': 'historical Orcamento',
                        'verbose_name_plural': 'historical Orcamentos',
                        'ordering': ('-history_date', '-history_id'),
                        'get_latest_by': ('history_date', 'history_id'),
                    },
                    bases=(simple_history.models.HistoricalChanges, models.Model),
                ),
            ],
        ),
    ]
