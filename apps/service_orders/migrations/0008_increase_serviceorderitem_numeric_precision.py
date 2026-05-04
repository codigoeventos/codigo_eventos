from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0007_alter_historicalserviceorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorderitem',
            name='dim_length',
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=12, null=True,
                verbose_name='Comprimento (m)'
            ),
        ),
        migrations.AlterField(
            model_name='serviceorderitem',
            name='dim_width',
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=12, null=True,
                verbose_name='Largura (m)'
            ),
        ),
        migrations.AlterField(
            model_name='serviceorderitem',
            name='dim_height',
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=12, null=True,
                verbose_name='Altura (m)'
            ),
        ),
        migrations.AlterField(
            model_name='serviceorderitem',
            name='measurement',
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=15, null=True,
                verbose_name='Metragem / Volume (m³)'
            ),
        ),
        migrations.AlterField(
            model_name='serviceorderitem',
            name='weight',
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=15, null=True,
                verbose_name='Peso Unitário (kg)'
            ),
        ),
    ]
