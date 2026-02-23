# Migration: rename proposals tables to projects tables
# Uses SeparateDatabaseAndState to rename existing DB tables without losing data

import apps.projects.models
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # DB: rename the existing proposals tables
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE proposals_proposal RENAME TO projects_project;',
                    reverse_sql='ALTER TABLE projects_project RENAME TO proposals_proposal;',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE proposals_historicalproposal RENAME TO projects_historicalproject;',
                    reverse_sql='ALTER TABLE projects_historicalproject RENAME TO proposals_historicalproposal;',
                ),
            ],
            # State: tell Django about the new models
            state_operations=[
                migrations.CreateModel(
                    name='HistoricalProject',
                    fields=[
                        ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                        ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                        ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                        ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Criado em')),
                        ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Atualizado em')),
                        ('title', models.CharField(max_length=255, verbose_name='Título')),
                        ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                        ('status', models.CharField(choices=[('draft', 'Rascunho'), ('sent', 'Enviado'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado')], default='draft', max_length=10, verbose_name='Status')),
                        ('original_document', models.TextField(blank=True, help_text='PDF ou DOC do projeto original', max_length=100, null=True, verbose_name='Documento Original')),
                        ('history_id', models.AutoField(primary_key=True, serialize=False)),
                        ('history_date', models.DateTimeField(db_index=True)),
                        ('history_change_reason', models.CharField(max_length=100, null=True)),
                        ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                        ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                        ('event', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.event', verbose_name='Evento')),
                        ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                        ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                    ],
                    options={
                        'verbose_name': 'historical Projeto',
                        'verbose_name_plural': 'historical Projetos',
                        'ordering': ('-history_date', '-history_id'),
                        'get_latest_by': ('history_date', 'history_id'),
                    },
                    bases=(simple_history.models.HistoricalChanges, models.Model),
                ),
                migrations.CreateModel(
                    name='Project',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                        ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                        ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                        ('title', models.CharField(max_length=255, verbose_name='Título')),
                        ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                        ('status', models.CharField(choices=[('draft', 'Rascunho'), ('sent', 'Enviado'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado')], default='draft', max_length=10, verbose_name='Status')),
                        ('original_document', models.FileField(blank=True, help_text='PDF ou DOC do projeto original', null=True, upload_to=apps.projects.models.project_upload_path, verbose_name='Documento Original')),
                        ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                        ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='events.event', verbose_name='Evento')),
                        ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                    ],
                    options={
                        'verbose_name': 'Projeto',
                        'verbose_name_plural': 'Projetos',
                        'ordering': ['-created_at'],
                    },
                ),
            ],
        ),
    ]
