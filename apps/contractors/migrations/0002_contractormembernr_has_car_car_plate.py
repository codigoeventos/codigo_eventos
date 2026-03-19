from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0001_initial'),
    ]

    operations = [
        # 1. Remove old single-NR fields from ContractorMember
        migrations.RemoveField(
            model_name='contractormember',
            name='nr_number',
        ),
        migrations.RemoveField(
            model_name='contractormember',
            name='nr_certificate_expiry',
        ),
        migrations.RemoveField(
            model_name='contractormember',
            name='nr_certificate_file',
        ),
        # 2. Create ContractorVehicle model (linked to Contractor)
        migrations.CreateModel(
            name='ContractorVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(help_text='Ex: ABC-1234 ou ABC1D23', max_length=10, verbose_name='Placa')),
                ('brand', models.CharField(blank=True, max_length=60, null=True, verbose_name='Marca')),
                ('model', models.CharField(blank=True, max_length=60, null=True, verbose_name='Modelo')),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Ano')),
                ('color', models.CharField(blank=True, max_length=40, null=True, verbose_name='Cor')),
                ('fuel', models.CharField(
                    blank=True,
                    choices=[('gasolina', 'Gasolina'), ('etanol', 'Etanol'), ('flex', 'Flex'),
                             ('diesel', 'Diesel'), ('eletrico', 'El\xe9trico'), ('hibrid', 'H\xedbrido')],
                    max_length=10, null=True, verbose_name='Combust\xedvel')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observa\xe7\xf5es')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contractor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='vehicles',
                    to='contractors.contractor',
                    verbose_name='Empreiteira',
                )),
            ],
            options={
                'verbose_name': 'Ve\xedculo',
                'verbose_name_plural': 'Ve\xedculos',
                'ordering': ['plate'],
            },
        ),
        # 3. Create ContractorMemberNR model
        migrations.CreateModel(
            name='ContractorMemberNR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_number', models.CharField(help_text='Ex: NR-10, NR-35, NR-33', max_length=20, verbose_name='N\xfamero NR')),
                ('nr_certificate_expiry', models.DateField(blank=True, null=True, verbose_name='Validade do Certificado')),
                ('nr_certificate_file', models.FileField(blank=True, null=True, upload_to='contractor_members/nr_certificates/', verbose_name='Certificado NR (upload)')),
                ('member', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='nrs',
                    to='contractors.contractormember',
                    verbose_name='Membro',
                )),
            ],
            options={
                'verbose_name': 'Certificado NR',
                'verbose_name_plural': 'Certificados NR',
                'ordering': ['nr_number'],
            },
        ),
    ]
