
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budgets", "0003_remove_budgetitem_weight_kg_budgetitem_weight_and_more"),
    ]
    operations = [
        migrations.CreateModel(
            name="BudgetSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Titulo da Secao")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Ordem")),
                ("budget", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sections", to="budgets.budget", verbose_name="Orcamento")),
            ],
            options={"verbose_name": "Secao do Orcamento", "verbose_name_plural": "Secoes do Orcamento", "ordering": ["order", "id"]},
        ),
        migrations.AddField(
            model_name="budgetitem",
            name="section",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="section_items", to="budgets.budgetsection", verbose_name="Secao"),
        ),
    ]
