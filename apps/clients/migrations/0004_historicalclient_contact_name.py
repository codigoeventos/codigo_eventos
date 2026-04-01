from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalclient',
            name='contact_name',
            field=models.CharField(
                blank=True,
                help_text='Nome da pessoa de contato responsável',
                max_length=255,
                null=True,
                verbose_name='Nome do Contato',
            ),
        ),
    ]
