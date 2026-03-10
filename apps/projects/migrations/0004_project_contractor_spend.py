from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_make_event_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contractor_spend',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Valor total gasto com a empreiteira neste projeto',
                max_digits=12,
                null=True,
                verbose_name='Valor Gasto com Empreiteira',
            ),
        ),
        migrations.AddField(
            model_name='historicalproject',
            name='contractor_spend',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Valor total gasto com a empreiteira neste projeto',
                max_digits=12,
                null=True,
                verbose_name='Valor Gasto com Empreiteira',
            ),
        ),
    ]
