"""
Budget models for event cost estimation.
"""

import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from apps.common.models import BaseModel


class Budget(BaseModel):
    """
    Budget model representing a cost estimate for an event proposal.
    
    Contains multiple budget items with calculated totals.
    When approved, automatically generates a Service Order.
    """
    
    STATUS_CHOICES = [
        ('sent', 'Enviado'),
        ('rejected', 'Rejeitado'),
        ('confirmed', 'Confirmado'),
    ]
    
    proposal = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budgets',
        verbose_name='Projeto'
    )
    
    name = models.CharField(
        'Nome',
        max_length=255,
        help_text='Nome identificador deste orçamento'
    )
    
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='sent'
    )
    
    is_selected = models.BooleanField(
        'Selecionado',
        default=False,
        help_text='Orçamento escolhido pelo cliente'
    )
    
    approval_token = models.UUIDField(
        'Token de Aprovação',
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text='Token único para link público de aprovação'
    )
    
    approval_status = models.CharField(
        'Status de Aprovação',
        max_length=20,
        choices=[
            ('pending', 'Pendente'),
            ('approved', 'Confirmado pelo Cliente'),
            ('rejected', 'Rejeitado pelo Cliente'),
        ],
        default='pending'
    )
    
    approved_at = models.DateTimeField(
        'Data de Aprovação',
        blank=True,
        null=True
    )
    
    client_notes = models.TextField(
        'Observações do Cliente',
        blank=True,
        null=True,
        help_text='Comentários do cliente na aprovação'
    )

    payment_info = models.TextField(
        'Informações de Pagamento',
        blank=True,
        default='',
        help_text='Bloco exibido antes das observações no documento público'
    )

    # ── Logistics / Freight ──────────────────────────────────────────────
    freight_cost = models.DecimalField(
        'Custo de Frete (R$)',
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Calculado automaticamente ou informado manualmente'
    )
    freight_urgency = models.ForeignKey(
        'logistics.UrgencyMultiplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budgets',
        verbose_name='Urgência de Entrega'
    )
    freight_distance_km = models.DecimalField(
        'Distância para Entrega (km)',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Usado no cálculo por distância (opcional)'
    )

    freight_included = models.BooleanField(
        'Frete Incluído',
        null=True,
        default=None,
        help_text='Cliente optou por incluir o frete no total aprovado'
    )

    include_fiscal_charges = models.BooleanField(
        'Incluir Encargos Fiscais',
        default=False,
        help_text='Aplica 17% de encargos fiscais sobre os itens do orçamento'
    )

    extra_charges = models.JSONField(
        'Encargos Adicionais',
        default=dict,
        blank=True,
        help_text='Apoio, mão de obra extra, documentação e taxas da feira'
    )

    DISCOUNT_TYPE_CHOICES = [
        ('none', 'Sem desconto'),
        ('percent', 'Percentual (%)'),
        ('value', 'Valor (R$)'),
    ]

    discount_type = models.CharField(
        'Tipo de Desconto',
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='none',
        help_text='Define se o desconto será em percentual ou valor fixo',
    )

    discount_value = models.DecimalField(
        'Valor do Desconto',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Percentual (%) ou valor fixo (R$), conforme o tipo selecionado',
    )

    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.proposal_id:
            return f"{self.name} - {self.proposal.title}"
        return self.name
    
    def get_approval_url(self):
        """Generate public approval URL."""
        from django.urls import reverse
        return reverse('budgets:public_approval', kwargs={'token': str(self.approval_token)})
    
    @property
    def total_value(self):
        """Calculate total value from all budget items."""
        total = self.items.aggregate(total=Sum('total_price'))['total']
        return total or 0

    @property
    def extra_charges_total(self):
        """Sum all extra charge entries from the JSON field (base values, no fiscal)."""
        total = Decimal('0')
        charges = self.extra_charges or {}
        for rows in charges.values():
            if isinstance(rows, list):
                for row in rows:
                    try:
                        total += Decimal(str(row.get('value') or 0))
                    except Exception:
                        pass
        return total

    @property
    def extra_charges_fiscal_total(self):
        """17% fiscal charges from extra charge rows with fiscal=True."""
        total = Decimal('0')
        charges = self.extra_charges or {}
        for rows in charges.values():
            if isinstance(rows, list):
                for row in rows:
                    if row.get('fiscal'):
                        try:
                            total += Decimal(str(row.get('value') or 0)) * Decimal('0.17')
                        except Exception:
                            pass
        return total

    @property
    def approved_value(self):
        """Calculate total value from approved items only (+ per-item fiscal + encargos + freight)."""
        approved_qs = self.items.filter(is_approved=True)
        total = approved_qs.aggregate(total=Sum('total_price'))['total'] or Decimal('0')
        # Per-item fiscal for approved items
        fiscal_base = approved_qs.filter(include_fiscal=True).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
        total += fiscal_base * Decimal('0.17') + self.extra_charges_fiscal_total
        if self.freight_included and self.freight_cost:
            total += self.freight_cost
        total += self.extra_charges_total
        return total - self.calculate_discount(total)

    @property
    def is_editable(self):
        """Check if budget can still be edited."""
        return self.approval_status == 'pending'

    @property
    def has_item_fiscal(self):
        """True if at least one item or extra charge row has fiscal charges."""
        if self.items.filter(include_fiscal=True).exists():
            return True
        charges = self.extra_charges or {}
        for rows in charges.values():
            if isinstance(rows, list):
                for row in rows:
                    if row.get('fiscal'):
                        return True
        return False

    @property
    def fiscal_charges_value(self):
        """17% fiscal charges — summed per-item and per-extra-row."""
        item_base = self.items.filter(include_fiscal=True).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
        return item_base * Decimal('0.17') + self.extra_charges_fiscal_total

    def calculate_discount(self, base_total):
        """Calculate discount amount over a given base total."""
        base = Decimal(str(base_total or 0))
        if base <= 0:
            return Decimal('0')

        raw = Decimal(str(self.discount_value or 0))
        if raw <= 0 or self.discount_type == 'none':
            return Decimal('0')

        if self.discount_type == 'percent':
            discount = (base * raw) / Decimal('100')
        else:  # 'value'
            discount = raw

        if discount < 0:
            return Decimal('0')
        return min(discount, base)

    @property
    def discount_amount(self):
        """Discount amount over the full budget total (before discount)."""
        base_total = self.total_value + self.fiscal_charges_value + (self.freight_cost or 0) + self.extra_charges_total
        return self.calculate_discount(base_total)

    @property
    def total_with_freight(self):
        """Budget total value plus per-item/per-row fiscal charges, freight and extra charges."""
        freight = self.freight_cost or 0
        base_total = self.total_value + self.fiscal_charges_value + freight + self.extra_charges_total
        return base_total - self.calculate_discount(base_total)

    @property
    def total_weight(self):
        """Sum of (weight × quantity) across all items that have weight."""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.items.all():
            if item.weight:
                total += item.weight * item.quantity
        return total

    @property
    def total_volume(self):
        """Sum of (measurement × quantity) for items with measurement_unit == 'm3'."""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.items.all():
            if item.measurement and item.measurement_unit == 'm3':
                total += item.measurement * item.quantity
        return total


class BudgetSection(models.Model):
    """
    Section grouping for budget items.

    A budget can have multiple sections (e.g. "Estrutura", "AV", "Decoração").
    Each section contains one or more BudgetItems.
    """

    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Orçamento'
    )

    title = models.CharField(
        'Título da Seção',
        max_length=255,
        help_text='Nome da seção do orçamento'
    )

    order = models.PositiveIntegerField(
        'Ordem',
        default=0,
        help_text='Posição da seção dentro do orçamento'
    )

    class Meta:
        verbose_name = 'Seção do Orçamento'
        verbose_name_plural = 'Seções do Orçamento'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title} ({self.budget.name})"

    @property
    def subtotal(self):
        """Sum of total_price for all items in this section."""
        total = self.section_items.aggregate(total=Sum('total_price'))['total']
        return total or 0


class BudgetItem(models.Model):
    """
    Individual line item in a budget.
    
    Auto-calculates total_price from quantity * unit_price.
    """
    
    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Orçamento'
    )

    section = models.ForeignKey(
        'BudgetSection',
        on_delete=models.CASCADE,
        related_name='section_items',
        verbose_name='Seção',
        null=True,
        blank=True,
        help_text='Seção a qual este item pertence'
    )
    
    name = models.CharField(
        'Item',
        max_length=255
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        null=True
    )
    
    quantity = models.IntegerField(
        'Quantidade',
        default=1,
        help_text='Quantidade de unidades'
    )
    
    measurement = models.DecimalField(
        'Metragem / Volume (m³)',
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Preenchido automaticamente a partir das dimensões, ou manualmente'
    )

    measurement_unit = models.CharField(
        'Unidade de Medida',
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ('m', 'metros (m)'),
            ('m2', 'metros² (m²)'),
            ('m3', 'metros³ (m³)'),
        ],
        help_text='Tipo de unidade de medida'
    )

    # Dimensions for automatic volume calculation
    dim_length = models.DecimalField(
        'Comprimento (m)',
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Comprimento unitário em metros'
    )
    dim_width = models.DecimalField(
        'Largura (m)',
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Largura unitária em metros'
    )
    dim_height = models.DecimalField(
        'Altura (m)',
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Altura unitária em metros'
    )

    weight = models.DecimalField(
        'Peso Unitário (kg)',
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Peso por unidade em quilogramas'
    )
    
    unit_price = models.DecimalField(
        'Preço Unitário',
        max_digits=15,
        decimal_places=2
    )
    
    total_price = models.DecimalField(
        'Preço Total',
        max_digits=15,
        decimal_places=2,
        editable=False
    )
    
    is_approved = models.BooleanField(
        'Confirmado pelo Cliente',
        default=True,
        help_text='Item selecionado para confirmação pelo cliente'
    )

    BILLING_CHOICES = [
        ('qty',   'Por Quantidade'),
        ('meter', 'Por Metro'),
    ]
    billing_type = models.CharField(
        'Tipo de Cobrança',
        max_length=10,
        choices=BILLING_CHOICES,
        default='qty',
        help_text='Define se o total é calculado por quantidade ou por metragem'
    )

    subitems_data = models.JSONField(
        'Subitens',
        null=True,
        blank=True,
        help_text='Lista de subitens com medidas individuais quando cada unidade tem dimensões diferentes'
    )

    include_fiscal = models.BooleanField(
        'Encargos Fiscais (17%)',
        default=False,
        help_text='Aplica 17% de encargos fiscais sobre o total deste item'
    )

    observations = models.TextField(
        'Observações',
        blank=True,
        null=True,
        help_text='Observações internas sobre este item'
    )

    description_ref = models.ForeignKey(
        'ItemDescription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_items',
        verbose_name='Descrição da biblioteca',
        help_text='Referência à descrição padrão usada (se aplicável)'
    )

    class Meta:
        verbose_name = 'Item do Orçamento'
        verbose_name_plural = 'Itens do Orçamento'
        ordering = ['budget', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.budget.name}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total_price and volume before saving.
        
        However, if total_price was explicitly provided (from form edit),
        respect it and don't recalculate to avoid rounding errors.
        """
        # If all three dimensions are provided, compute volume (m³) automatically
        if self.dim_length and self.dim_width and self.dim_height:
            self.measurement = self.dim_length * self.dim_width * self.dim_height
            self.measurement_unit = 'm3'
        
        # Check if this is an explicit total from form submission (not auto-calculated)
        # If _skip_total_recalc flag is set, respect the provided total
        should_recalc = not getattr(self, '_skip_total_recalc', False)
        
        # Only recalculate if:
        # 1. Should recalc flag is not set, AND
        # 2. Total is zero or item is new
        if should_recalc and (self.total_price == 0 or self.pk is None):
            # Total based on billing type
            if self.billing_type == 'meter':
                self.total_price = (self.measurement or 0) * self.quantity * self.unit_price
            else:
                self.total_price = self.quantity * self.unit_price
        
        # Clean up the flag
        if hasattr(self, '_skip_total_recalc'):
            delattr(self, '_skip_total_recalc')
        
        super().save(*args, **kwargs)


class ItemDescription(models.Model):
    """
    Reusable item description library.

    Pre-defined descriptions that can be selected when building budget items.
    The selected body text is copied into the BudgetItem.description field.
    """

    title = models.CharField(
        'Título',
        max_length=255,
        help_text='Nome curto exibido no seletor (ex.: "Painel modulado 3×3")'
    )

    body = models.TextField(
        'Descrição',
        blank=True,
        help_text='Texto completo que será copiado para o item do orçamento'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Descrição de Item'
        verbose_name_plural = 'Descrições de Itens'
        ordering = ['title']

    def __str__(self):
        return self.title


class PaymentInfoTemplate(models.Model):
    """
    Reusable payment information library.

    Pre-defined payment blocks that can be selected in the budget form
    and copied to Budget.payment_info.
    """

    title = models.CharField(
        'Título',
        max_length=255,
        help_text='Nome curto exibido no seletor (ex.: "Dados bancários padrão")'
    )

    body = models.TextField(
        'Informações de Pagamento',
        blank=True,
        help_text='Texto completo que será copiado para o orçamento'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Informação de Pagamento'
        verbose_name_plural = 'Informações de Pagamento'
        ordering = ['title']

    def __str__(self):
        return self.title


class BudgetNotification(models.Model):
    """
    Notification created when a client approves or rejects a budget via the public link.
    Displayed as a bell icon badge in the internal dashboard header.
    """

    ACTION_CHOICES = [
        ('approved', 'Confirmado'),
        ('rejected', 'Rejeitado'),
    ]

    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Proposta',
    )

    action = models.CharField(
        'Ação',
        max_length=20,
        choices=ACTION_CHOICES,
    )

    is_read = models.BooleanField('Lida', default=False)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação de Proposta'
        verbose_name_plural = 'Notificações de Propostas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.budget.name} – {self.get_action_display()}"


class BudgetVersion(models.Model):
    """
    Snapshot of a budget at a specific point in time.

    Created automatically every time a budget is saved via the edit form.
    Stores a full JSON snapshot of the budget data (fields + sections + items)
    so editors can browse the history and restore a previous version.
    """

    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='Proposta',
    )

    version_number = models.PositiveIntegerField('Número da Versão')

    label = models.CharField(
        'Rótulo',
        max_length=255,
        blank=True,
        help_text='Nome curto opcional para identificar esta versão',
    )

    snapshot = models.JSONField(
        'Snapshot',
        help_text='Cópia completa dos dados da proposta neste momento',
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_versions_created',
        verbose_name='Criado por',
    )

    class Meta:
        verbose_name = 'Versão da Proposta'
        verbose_name_plural = 'Versões da Proposta'
        ordering = ['-version_number']
        unique_together = [('budget', 'version_number')]

    def __str__(self):
        label = f' — {self.label}' if self.label else ''
        return f"{self.budget.name} v{self.version_number}{label}"
