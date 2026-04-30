# Generated manually to fix numeric field overflow on budget items

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0016_budget_payment_info_and_paymentinfotemplate'),
    ]

    operations = [
        # Budget model fields
        migrations.AlterField(
            model_name='budget',
            name='freight_cost',
            field=models.DecimalField(
                blank=True, decimal_places=2,
                help_text='Calculado automaticamente ou informado manualmente',
                max_digits=15, null=True, verbose_name='Custo de Frete (R$)'
            ),
        ),
        migrations.AlterField(
            model_name='budget',
            name='freight_distance_km',
            field=models.DecimalField(
                blank=True, decimal_places=2,
                help_text='Usado no cálculo por distância (opcional)',
                max_digits=12, null=True, verbose_name='Distância para Entrega (km)'
            ),
        ),
        migrations.AlterField(
            model_name='budget',
            name='discount_value',
            field=models.DecimalField(
                decimal_places=2, default=0,
                help_text='Percentual (%) ou valor fixo (R$), conforme o tipo selecionado',
                max_digits=15, verbose_name='Valor do Desconto'
            ),
        ),
        # BudgetItem model fields
        migrations.AlterField(
            model_name='budgetitem',
            name='measurement',
            field=models.DecimalField(
                blank=True, decimal_places=3,
                help_text='Preenchido automaticamente a partir das dimensões, ou manualmente',
                max_digits=15, null=True, verbose_name='Metragem / Volume (m³)'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='dim_length',
            field=models.DecimalField(
                blank=True, decimal_places=3,
                help_text='Comprimento unitário em metros',
                max_digits=12, null=True, verbose_name='Comprimento (m)'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='dim_width',
            field=models.DecimalField(
                blank=True, decimal_places=3,
                help_text='Largura unitária em metros',
                max_digits=12, null=True, verbose_name='Largura (m)'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='dim_height',
            field=models.DecimalField(
                blank=True, decimal_places=3,
                help_text='Altura unitária em metros',
                max_digits=12, null=True, verbose_name='Altura (m)'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='weight',
            field=models.DecimalField(
                blank=True, decimal_places=3,
                help_text='Peso por unidade em quilogramas',
                max_digits=15, null=True, verbose_name='Peso Unitário (kg)'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='unit_price',
            field=models.DecimalField(
                decimal_places=2, max_digits=15,
                verbose_name='Preço Unitário'
            ),
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='total_price',
            field=models.DecimalField(
                decimal_places=2, editable=False, max_digits=15,
                verbose_name='Preço Total'
            ),
        ),
        # HistoricalBudget model fields (django-simple-history)
        migrations.AlterField(
            model_name='historicalbudget',
            name='freight_cost',
            field=models.DecimalField(
                blank=True, decimal_places=2,
                help_text='Calculado automaticamente ou informado manualmente',
                max_digits=15, null=True, verbose_name='Custo de Frete (R$)'
            ),
        ),
        migrations.AlterField(
            model_name='historicalbudget',
            name='freight_distance_km',
            field=models.DecimalField(
                blank=True, decimal_places=2,
                help_text='Usado no cálculo por distância (opcional)',
                max_digits=12, null=True, verbose_name='Distância para Entrega (km)'
            ),
        ),
        migrations.AlterField(
            model_name='historicalbudget',
            name='discount_value',
            field=models.DecimalField(
                decimal_places=2, default=0,
                help_text='Percentual (%) ou valor fixo (R$), conforme o tipo selecionado',
                max_digits=15, verbose_name='Valor do Desconto'
            ),
        ),
    ]