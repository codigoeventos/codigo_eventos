from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0002_contractormembernr_has_car_car_plate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorMemberNRFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='contractor_members/nr_certificates/', verbose_name='Arquivo')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('nr', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='files',
                    to='contractors.contractormembernr',
                    verbose_name='NR',
                )),
            ],
            options={
                'verbose_name': 'Arquivo NR',
                'verbose_name_plural': 'Arquivos NR',
                'ordering': ['uploaded_at'],
            },
        ),
    ]
