from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0005_eventcontractor_public_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventContractorVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='selected_vehicles', to='contractors.eventcontractor', verbose_name='Vínculo Empreiteira-Evento')),
                ('vehicle', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='event_participations', to='contractors.contractorvehicle', verbose_name='Veículo')),
            ],
            options={
                'verbose_name': 'Veículo em Evento',
                'verbose_name_plural': 'Veículos em Eventos',
                'ordering': ['vehicle__plate'],
                'unique_together': {('assignment', 'vehicle')},
            },
        ),
    ]
