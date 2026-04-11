from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0006_alter_art_budget'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ARTFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do Arquivo')),
                ('file', models.FileField(max_length=500, upload_to='art/artfile/temp/art_files', verbose_name='Arquivo')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Enviado em')),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='art.art', verbose_name='ART')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Enviado por')),
            ],
            options={
                'verbose_name': 'Arquivo de ART',
                'verbose_name_plural': 'Arquivos de ART',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
