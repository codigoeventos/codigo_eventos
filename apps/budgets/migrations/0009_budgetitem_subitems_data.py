from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0008_budgetitem_billing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='subitems_data',
            field=models.JSONField(
                blank=True,
                help_text='Lista de subitens com medidas individuais quando cada unidade tem dimensões diferentes',
                null=True,
                verbose_name='Subitens',
            ),
        ),
    ]
