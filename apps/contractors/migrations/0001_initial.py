# Generated migration for contractors app.
# Uses SeparateDatabaseAndState to rename existing teams DB tables.

import django.db.models.deletion
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
            # --- Rename tables at the DB level ---
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE teams_team RENAME TO contractors_contractor',
                    reverse_sql='ALTER TABLE contractors_contractor RENAME TO teams_team',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE teams_teammember RENAME TO contractors_contractormember',
                    reverse_sql='ALTER TABLE contractors_contractormember RENAME TO teams_teammember',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE teams_eventteam RENAME TO contractors_eventcontractor',
                    reverse_sql='ALTER TABLE contractors_eventcontractor RENAME TO teams_eventteam',
                ),
            ],
            # --- Recreate the model state mirroring what actually exists in the DB after rename ---
            state_operations=[
                migrations.CreateModel(
                    name='Contractor',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                        ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                        # name field as it existed in Team
                        ('name', models.CharField(max_length=255, verbose_name='Nome da Empreiteira')),
                        # description was the only extra field in Team — kept temporarily
                        ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                        ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                        ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                    ],
                    options={
                        'verbose_name': 'Empreiteira',
                        'verbose_name_plural': 'Empreiteiras',
                        'ordering': ['name'],
                    },
                ),
                migrations.CreateModel(
                    name='ContractorMember',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=255, verbose_name='Nome')),
                        ('role', models.CharField(help_text='Ex: Técnico de Som, Iluminador, etc.', max_length=100, verbose_name='Função')),
                        # phone was non-null in teams_teammember
                        ('phone', models.CharField(max_length=50, verbose_name='Telefone')),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('updated_at', models.DateTimeField(auto_now=True)),
                        # FK was team_id in DB → after rename it's still team_id column; we'll rename in 0002
                        ('contractor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='contractors.contractor', verbose_name='Empreiteira')),
                    ],
                    options={
                        'verbose_name': 'Membro da Empreiteira',
                        'verbose_name_plural': 'Membros da Empreiteira',
                        'ordering': ['name'],
                    },
                ),
                migrations.CreateModel(
                    name='EventContractor',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('assigned_at', models.DateTimeField(auto_now_add=True)),
                        ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractors', to='events.event', verbose_name='Evento')),
                        # FK was member_id in DB → will rename in 0002
                        ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_assignments', to='contractors.contractor', verbose_name='Empreiteira')),
                    ],
                    options={
                        'verbose_name': 'Empreiteira do Evento',
                        'verbose_name_plural': 'Empreiteiras dos Eventos',
                        'ordering': ['event', 'contractor'],
                    },
                ),
                migrations.AlterUniqueTogether(
                    name='eventcontractor',
                    unique_together={('event', 'contractor')},
                ),
            ],
        ),
    ]
