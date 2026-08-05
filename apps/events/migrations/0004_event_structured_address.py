from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_event_date_end_event_setup_date_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Local'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Local'),
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Endereço'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Nº'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_complement',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Complemento'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_state',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='UF'),
        ),
        migrations.AddField(
            model_name='event',
            name='address_zip',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Endereço'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Nº'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_complement',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Complemento'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_state',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='UF'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='address_zip',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CEP'),
        ),
    ]
