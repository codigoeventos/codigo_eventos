from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_make_document_fields_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
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
