# Migration to add new columns to contractors tables.
# Column renames (member_id→contractor_id, team_id→contractor_id, description→notes)
# are skipped at DB level for production (virgin DB already has correct column names).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0001_initial'),
    ]

    operations = [
        # --- Rename FK columns (local dev only — production tables already have correct names) ---
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$
                        BEGIN
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='contractors_eventcontractor' AND column_name='member_id'
                            ) THEN
                                ALTER TABLE contractors_eventcontractor RENAME COLUMN member_id TO contractor_id;
                            END IF;
                        END$$;
                    """,
                    reverse_sql='ALTER TABLE contractors_eventcontractor RENAME COLUMN contractor_id TO member_id',
                ),
                migrations.RunSQL(
                    sql="""
                        DO $$
                        BEGIN
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='contractors_contractormember' AND column_name='team_id'
                            ) THEN
                                ALTER TABLE contractors_contractormember RENAME COLUMN team_id TO contractor_id;
                            END IF;
                        END$$;
                    """,
                    reverse_sql='ALTER TABLE contractors_contractormember RENAME COLUMN contractor_id TO team_id',
                ),
            ],
            state_operations=[],
        ),
        # --- Rename description → notes (local dev only) ---
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$
                        BEGIN
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='contractors_contractor' AND column_name='description'
                            ) THEN
                                ALTER TABLE contractors_contractor RENAME COLUMN description TO notes;
                            END IF;
                        END$$;
                    """,
                    reverse_sql='ALTER TABLE contractors_contractor RENAME COLUMN notes TO description',
                ),
            ],
            state_operations=[
                migrations.RenameField(
                    model_name='contractor',
                    old_name='description',
                    new_name='notes',
                ),
            ],
        ),

        # --- Add new columns to contractors_contractor ---
        migrations.AddField(
            model_name='contractor',
            name='cnpj',
            field=models.CharField(blank=True, help_text='Ex: 00.000.000/0001-00', max_length=18, null=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='legal_representative',
            field=models.CharField(blank=True, help_text='Nome do responsável legal pela empresa', max_length=255, null=True, verbose_name='Responsável Legal'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefone'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_street',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Logradouro'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Número'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_complement',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_state',
            field=models.CharField(blank=True, help_text='Sigla do estado (ex: SP)', max_length=2, null=True, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='address_zip',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Banco'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_agency',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Agência'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_account',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Conta'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_account_type',
            field=models.CharField(blank=True, choices=[('corrente', 'Corrente'), ('poupanca', 'Poupança')], max_length=20, null=True, verbose_name='Tipo de Conta'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_pix_key',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Chave PIX'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='certifications',
            field=models.TextField(blank=True, help_text='Descreva as certificações, alvarás e documentações da empresa', null=True, verbose_name='Certificações e Alvarás'),
        ),
        # Make phone nullable on contractor_member
        migrations.AlterField(
            model_name='contractormember',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefone'),
        ),
        # Add email to ContractorMember
        migrations.AddField(
            model_name='contractormember',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail'),
        ),
        # Add notes to EventContractor
        migrations.AddField(
            model_name='eventcontractor',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        # Update name field verbose name
        migrations.AlterField(
            model_name='contractor',
            name='name',
            field=models.CharField(help_text='Razão social ou nome fantasia da empreiteira', max_length=255, verbose_name='Nome da Empreiteira'),
        ),
    ]
