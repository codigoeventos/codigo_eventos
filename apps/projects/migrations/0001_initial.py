# Migration: create projects tables
# Uses SeparateDatabaseAndState so local dev (which renamed from proposals) stays compatible.
# Production (virgin DB): database_operations creates the tables directly.

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
            # DB: create tables directly (works on virgin DB; local dev already has them)
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        CREATE TABLE IF NOT EXISTS projects_project (
                            id bigserial PRIMARY KEY,
                            deleted timestamptz NULL,
                            deleted_by_cascade boolean NOT NULL DEFAULT false,
                            created_at timestamptz NOT NULL,
                            updated_at timestamptz NOT NULL,
                            title varchar(255) NOT NULL,
                            description text NULL,
                            status varchar(20) NOT NULL DEFAULT 'draft',
                            original_document varchar(255) NULL,
                            event_id bigint NOT NULL REFERENCES events_event(id) ON DELETE CASCADE,
                            created_by_id integer NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                            updated_by_id integer NULL REFERENCES auth_user(id) ON DELETE SET NULL
                        );
                    """,
                    reverse_sql='DROP TABLE IF EXISTS projects_project;',
                ),
                migrations.RunSQL(
                    sql="""
                        CREATE TABLE IF NOT EXISTS projects_historicalproject (
                            id bigint NOT NULL,
                            deleted timestamptz NULL,
                            deleted_by_cascade boolean NOT NULL DEFAULT false,
                            created_at timestamptz NOT NULL,
                            updated_at timestamptz NOT NULL,
                            title varchar(255) NOT NULL,
                            description text NULL,
                            status varchar(20) NOT NULL DEFAULT 'draft',
                            original_document varchar(100) NULL,
                            history_id serial PRIMARY KEY,
                            history_date timestamptz NOT NULL,
                            history_change_reason varchar(100) NULL,
                            history_type varchar(1) NOT NULL,
                            created_by_id integer NULL,
                            event_id bigint NULL,
                            history_user_id integer NULL REFERENCES auth_user(id) ON DELETE SET NULL,
                            updated_by_id integer NULL
                        );
                    """,
                    reverse_sql='DROP TABLE IF EXISTS projects_historicalproject;',
                ),
            ],
            # State: tell Django about the new models (unchanged)
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
