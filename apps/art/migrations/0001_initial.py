import uuid
import django.db.models.deletion
import safedelete.models
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ART',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('public_token', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Token único para link público de visualização da ART', unique=True, verbose_name='Token Público')),
                ('engineer_name', models.CharField(max_length=255, verbose_name='Nome do Engenheiro')),
                ('engineer_crea', models.CharField(help_text='Número de registro no CREA', max_length=50, verbose_name='CREA do Engenheiro')),
                ('activity_description', models.TextField(help_text='Objeto técnico da contratação', verbose_name='Descrição da Atividade / Serviço')),
                ('location', models.CharField(max_length=500, verbose_name='Local da Obra / Endereço')),
                ('quantity', models.DecimalField(decimal_places=3, help_text='Soma da metragem dos itens do orçamento', max_digits=12, verbose_name='Quantidade Total')),
                ('measurement_unit', models.CharField(choices=[('m', 'metros (m)'), ('m2', 'metros² (m²)'), ('m3', 'metros³ (m³)'), ('un', 'unidades (un)')], default='m3', max_length=10, verbose_name='Unidade de Medida')),
                ('contract_value', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor do Contrato (R$)')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Data de Início')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Data de Conclusão')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_created', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_updated', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='art', to='projects.project', verbose_name='Projeto')),
            ],
            options={
                'verbose_name': 'ART',
                'verbose_name_plural': 'ARTs',
                'ordering': ['-created_at'],
            },
            bases=(safedelete.models.SafeDeleteModel,),
            managers=[
                ('objects', safedelete.models.SafeDeleteManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalART',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Atualizado em')),
                ('public_token', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Token único para link público de visualização da ART', verbose_name='Token Público')),
                ('engineer_name', models.CharField(max_length=255, verbose_name='Nome do Engenheiro')),
                ('engineer_crea', models.CharField(help_text='Número de registro no CREA', max_length=50, verbose_name='CREA do Engenheiro')),
                ('activity_description', models.TextField(help_text='Objeto técnico da contratação', verbose_name='Descrição da Atividade / Serviço')),
                ('location', models.CharField(max_length=500, verbose_name='Local da Obra / Endereço')),
                ('quantity', models.DecimalField(decimal_places=3, help_text='Soma da metragem dos itens do orçamento', max_digits=12, verbose_name='Quantidade Total')),
                ('measurement_unit', models.CharField(choices=[('m', 'metros (m)'), ('m2', 'metros² (m²)'), ('m3', 'metros³ (m³)'), ('un', 'unidades (un)')], default='m3', max_length=10, verbose_name='Unidade de Medida')),
                ('contract_value', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor do Contrato (R$)')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Data de Início')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Data de Conclusão')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='projects.project', verbose_name='Projeto')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'historical ART',
                'verbose_name_plural': 'historical ARTs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
