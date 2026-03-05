# Generated migration for teams app

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
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(help_text='Ex: Equipe de Som, Equipe de Iluminação, etc.', max_length=255, verbose_name='Nome da Equipe')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'Equipe',
                'verbose_name_plural': 'Equipes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalTeam',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Atualizado em')),
                ('name', models.CharField(help_text='Ex: Equipe de Som, Equipe de Iluminação, etc.', max_length=255, verbose_name='Nome da Equipe')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'historical Equipe',
                'verbose_name_plural': 'historical Equipes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('role', models.CharField(help_text='Ex: Técnico de Som, Iluminador, etc.', max_length=100, verbose_name='Função')),
                ('phone', models.CharField(max_length=50, verbose_name='Telefone')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='teams.team', verbose_name='Equipe')),
            ],
            options={
                'verbose_name': 'Membro da Equipe',
                'verbose_name_plural': 'Membros da Equipe',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EventTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_assignments', to='events.event', verbose_name='Evento')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_assignments', to='teams.teammember', verbose_name='Membro')),
            ],
            options={
                'verbose_name': 'Equipe do Evento',
                'verbose_name_plural': 'Equipes dos Eventos',
                'ordering': ['event', 'member'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventteam',
            unique_together={('event', 'member')},
        ),
    ]
