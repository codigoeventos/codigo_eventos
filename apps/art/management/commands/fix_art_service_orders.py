"""
Pre-migration script: garante que toda ART com budget_id tenha uma OS correspondente.

Execute ANTES de rodar `python manage.py migrate` em produção:

    python manage.py fix_art_service_orders          # dry-run (apenas mostra o que faria)
    python manage.py fix_art_service_orders --commit  # aplica as mudanças

O que faz:
  1. Usa SQL direto para encontrar ARTs com budget_id mas SEM OS correspondente
     (seguro de rodar antes da migração 0010, que ainda não adicionou service_order_id).
  2. Para cada caso, tenta vincular a uma OS já existente para aquele budget.
  3. Se não existir OS para o budget, cria uma OS corretamente preenchida.
"""

from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Cria/vincula OSes faltantes para ARTs antes da migração art.0010'

    def add_arguments(self, parser):
        parser.add_argument(
            '--commit',
            action='store_true',
            help='Persiste as alterações no banco (sem esta flag roda em dry-run)',
        )

    def handle(self, *args, **options):
        commit = options['commit']

        from apps.service_orders.models import ServiceOrder
        from apps.budgets.models import Budget

        # ── Detecta via SQL puro (colunas do schema PRÉ-migração 0010) ──────
        # art_art.budget_id existe antes da 0010; service_order_id ainda não.
        with connection.cursor() as cur:
            # Verifica se a coluna service_order_id já existe (migração já rodou?)
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'art_art'
                  AND column_name = 'service_order_id'
            """)
            already_migrated = cur.fetchone() is not None

            if already_migrated:
                self.stdout.write(self.style.SUCCESS(
                    '✔ Migração art.0010 já foi aplicada (coluna service_order_id existe). '
                    'Nada a fazer.'
                ))
                return

            # Pré-migração: busca ARTs cujo budget não tem OS correspondente
            cur.execute("""
                SELECT a.id, a.budget_id, a.created_by_id
                FROM art_art a
                WHERE a.budget_id IS NOT NULL
                  AND NOT EXISTS (
                      SELECT 1 FROM service_orders_serviceorder so
                      WHERE so.budget_id = a.budget_id
                  )
            """)
            rows = cur.fetchall()

        total = len(rows)

        if total == 0:
            self.stdout.write(self.style.SUCCESS(
                '✔ Nenhuma ART sem OS encontrada. Pode rodar migrate normalmente.'
            ))
            return

        self.stdout.write(self.style.WARNING(
            f'⚠  {total} ART(s) com budget mas sem OS vinculada:'
        ))
        self.stdout.write('')

        criadas    = 0
        vinculadas = 0
        erros      = 0

        with transaction.atomic():
            for art_id, budget_id, created_by_id in rows:
                try:
                    budget = Budget.objects.select_related('event').get(pk=budget_id)
                except Budget.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f'  [ERRO] ART #{art_id} → Budget #{budget_id} não encontrado!'
                    ))
                    erros += 1
                    continue

                event = budget.event
                label = (
                    f'ART #{art_id} → Budget #{budget_id} '
                    f'("{budget}" / evento: {event or "—"})'
                )

                os_existente = ServiceOrder._default_manager.filter(
                    budget_id=budget_id
                ).first()

                if os_existente:
                    self.stdout.write(f'  [VINCULAR] {label}  →  OS existente #{os_existente.pk}')
                    if commit:
                        with connection.cursor() as cur2:
                            cur2.execute(
                                'UPDATE art_art SET service_order_id = %s WHERE id = %s',
                                [os_existente.pk, art_id],
                            )
                    vinculadas += 1
                else:
                    self.stdout.write(f'  [CRIAR OS] {label}')
                    if commit:
                        try:
                            os_nova = ServiceOrder._default_manager.create(
                                budget=budget,
                                event=event,
                                status='pending',
                                created_by_id=created_by_id,
                                updated_by_id=created_by_id,
                            )
                            self.stdout.write(self.style.SUCCESS(
                                f'       OS #{os_nova.pk} criada.'
                            ))
                        except Exception as exc:
                            self.stdout.write(self.style.ERROR(
                                f'       ERRO ao criar OS: {exc}'
                            ))
                            erros += 1
                            transaction.set_rollback(True)
                    criadas += 1

            if not commit:
                transaction.set_rollback(True)

        self.stdout.write('')

        if commit:
            if erros:
                self.stdout.write(self.style.ERROR(
                    f'Concluído COM ERROS — vinculadas: {vinculadas}, criadas: {criadas}, '
                    f'erros: {erros}. Rollback aplicado, nada foi salvo.'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'✔ Concluído — OSes vinculadas: {vinculadas}, OSes criadas: {criadas}.'
                ))
                self.stdout.write(self.style.SUCCESS(
                    'Agora pode rodar: python manage.py migrate'
                ))
        else:
            self.stdout.write(self.style.WARNING(
                f'DRY-RUN — nada foi alterado. Para aplicar: --commit'
            ))
