from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0007_add_include_fiscal_charges'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='billing_type',
            field=models.CharField(
                verbose_name='Tipo de Cobrança',
                max_length=10,
                choices=[('qty', 'Por Quantidade'), ('meter', 'Por Metro')],
                default='qty',
                help_text='Define se o total é calculado por quantidade ou por metragem',
            ),
        ),
    ]
