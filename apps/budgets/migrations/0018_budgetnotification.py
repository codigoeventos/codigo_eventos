from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0017_increase_numeric_precision'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('is_read', models.BooleanField(default=False, verbose_name='Lida')),
                ('action', models.CharField(
                    choices=[('approved', 'Aprovado'), ('rejected', 'Rejeitado')],
                    max_length=20,
                    verbose_name='Ação',
                )),
                ('budget', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notifications',
                    to='budgets.budget',
                    verbose_name='Proposta',
                )),
            ],
            options={
                'verbose_name': 'Notificação de Proposta',
                'verbose_name_plural': 'Notificações de Propostas',
                'ordering': ['-created_at'],
            },
        ),
    ]
