"""
Comando para migrar arquivos locais da pasta media/ para o AWS S3.

Uso:
    python manage.py migrate_media_to_s3
    python manage.py migrate_media_to_s3 --dry-run
    python manage.py migrate_media_to_s3 --prefix proposals
    python manage.py migrate_media_to_s3 --force   (sobrescreve existentes)
"""

import os
import mimetypes
import boto3
from botocore.exceptions import ClientError

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Migra arquivos locais da pasta media/ para o AWS S3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Lista os arquivos que seriam migrados sem fazer upload',
        )
        parser.add_argument(
            '--prefix',
            type=str,
            default='',
            help='Subpasta específica dentro de media/ para migrar (ex: proposals, art)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Sobrescreve arquivos que já existem no S3',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        prefix = options['prefix']
        force = options['force']

        # Validar configurações
        bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
        region = getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-2')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

        if not all([bucket_name, access_key, secret_key]):
            raise CommandError(
                'Configurações AWS não encontradas. '
                'Verifique AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY no .env'
            )

        media_root = str(settings.MEDIA_ROOT)
        scan_dir = os.path.join(media_root, prefix) if prefix else media_root

        if not os.path.exists(scan_dir):
            raise CommandError(f'Diretório não encontrado: {scan_dir}')

        self.stdout.write('')
        if dry_run:
            self.stdout.write(self.style.WARNING('  DRY RUN — nenhum arquivo será enviado'))

        self.stdout.write(f'  Bucket : {bucket_name} ({region})')
        self.stdout.write(f'  Source : {scan_dir}')
        if prefix:
            self.stdout.write(f'  Prefix : {prefix}')
        self.stdout.write('  ' + '─' * 56)

        # Conectar ao S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

        # Verificar conexão
        try:
            s3.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise CommandError(f'Erro ao conectar ao bucket "{bucket_name}": {e}')

        total = success = skipped = errors = 0

        for root, dirs, files in os.walk(scan_dir):
            # Ignorar pastas ocultas
            dirs[:] = sorted([d for d in dirs if not d.startswith('.')])

            for filename in sorted(files):
                if filename.startswith('.'):
                    continue

                local_path = os.path.join(root, filename)
                # Caminho relativo ao media_root → chave S3
                s3_key = os.path.relpath(local_path, media_root)
                total += 1

                if dry_run:
                    self.stdout.write(f'  → {s3_key}')
                    skipped += 1
                    continue

                # Verificar se já existe no S3
                if not force:
                    try:
                        s3.head_object(Bucket=bucket_name, Key=s3_key)
                        self.stdout.write(f'  ⏭  Já existe: {s3_key}')
                        skipped += 1
                        continue
                    except ClientError as e:
                        if e.response['Error']['Code'] != '404':
                            self.stdout.write(self.style.ERROR(f'  ✗ Erro ao verificar {s3_key}: {e}'))
                            errors += 1
                            continue

                # Upload
                try:
                    content_type, _ = mimetypes.guess_type(filename)
                    extra_args = {}
                    if content_type:
                        extra_args['ContentType'] = content_type

                    s3.upload_file(local_path, bucket_name, s3_key, ExtraArgs=extra_args)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {s3_key}'))
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ {s3_key}: {e}'))
                    errors += 1

        self.stdout.write('  ' + '─' * 56)
        self.stdout.write(f'  Total encontrados : {total}')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  Dry run — execute sem --dry-run para enviar'))
        else:
            if success:
                self.stdout.write(self.style.SUCCESS(f'  Enviados          : {success}'))
            if skipped:
                self.stdout.write(f'  Já existiam       : {skipped}')
            if errors:
                self.stdout.write(self.style.ERROR(f'  Erros             : {errors}'))
            if success == 0 and errors == 0:
                self.stdout.write('  Nada novo para enviar.')

        self.stdout.write('')
