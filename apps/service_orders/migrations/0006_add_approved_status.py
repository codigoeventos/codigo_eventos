from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0005_serviceorder_event_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pendente'),
                    ('approved', 'Aprovado'),
                    ('in_progress', 'Em Andamento'),
                    ('completed', 'Concluída'),
                    ('cancelled', 'Cancelada'),
                ],
                default='pending',
                max_length=15,
                verbose_name='Status',
            ),
        ),
    ]
