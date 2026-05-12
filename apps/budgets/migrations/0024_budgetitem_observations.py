from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0023_fix_remaining_approved_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='observations',
            field=models.TextField(blank=True, help_text='Observações internas sobre este item', null=True, verbose_name='Observações'),
        ),
    ]
