import uuid
from django.db import migrations, models


def fill_public_tokens(apps, schema_editor):
    ServiceOrder = apps.get_model('service_orders', 'ServiceOrder')
    for so in ServiceOrder.objects.filter(public_token__isnull=True):
        so.public_token = uuid.uuid4()
        so.save(update_fields=['public_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0002_add_physical_fields_to_serviceorderitem'),
    ]

    operations = [
        # Step 1: add as nullable (no unique yet)
        migrations.AddField(
            model_name='serviceorder',
            name='public_token',
            field=models.UUIDField(
                verbose_name='Token Público',
                null=True,
                blank=True,
                editable=False,
                help_text='Token único para link público de visualização da OS',
            ),
        ),
        # Step 2: fill existing rows
        migrations.RunPython(fill_public_tokens, migrations.RunPython.noop),
        # Step 3: make non-null + unique
        migrations.AlterField(
            model_name='serviceorder',
            name='public_token',
            field=models.UUIDField(
                verbose_name='Token Público',
                default=uuid.uuid4,
                unique=True,
                editable=False,
                help_text='Token único para link público de visualização da OS',
            ),
        ),
    ]
