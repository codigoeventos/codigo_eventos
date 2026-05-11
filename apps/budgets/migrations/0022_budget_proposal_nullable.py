from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0021_migrate_draft_approved_to_sent_confirmed'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='proposal',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='budgets',
                to='projects.project',
                verbose_name='Projeto',
            ),
        ),
        migrations.AlterField(
            model_name='historicalbudget',
            name='proposal',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='projects.project',
                verbose_name='Projeto',
            ),
        ),
    ]
