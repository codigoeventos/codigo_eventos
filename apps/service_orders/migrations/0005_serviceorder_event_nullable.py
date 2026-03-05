from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('service_orders', '0004_historicalserviceorder_public_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='event',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='service_orders',
                to='events.event',
                verbose_name='Evento',
            ),
        ),
    ]
