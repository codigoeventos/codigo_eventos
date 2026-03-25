import uuid
from django.db import migrations, models


def populate_public_token(apps, schema_editor):
    EventContractor = apps.get_model('contractors', 'EventContractor')
    for obj in EventContractor.objects.filter(public_token__isnull=True):
        obj.public_token = uuid.uuid4()
        obj.save(update_fields=['public_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0004_eventcontractormember'),
    ]

    operations = [
        # Step 1: add nullable (no unique yet)
        migrations.AddField(
            model_name='eventcontractor',
            name='public_token',
            field=models.UUIDField(
                verbose_name='Token Público',
                null=True,
                blank=True,
                editable=False,
                help_text='Token único para link público de visualização da empreiteira no evento',
            ),
        ),
        # Step 2: fill existing rows
        migrations.RunPython(populate_public_token, migrations.RunPython.noop),
        # Step 3: make non-nullable and unique
        migrations.AlterField(
            model_name='eventcontractor',
            name='public_token',
            field=models.UUIDField(
                verbose_name='Token Público',
                default=uuid.uuid4,
                unique=True,
                editable=False,
                help_text='Token único para link público de visualização da empreiteira no evento',
            ),
        ),
    ]
