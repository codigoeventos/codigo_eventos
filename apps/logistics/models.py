"""
Logistics models for freight/shipping cost calculation.

Provides configurable weight/volume range pricing tables,
urgency multipliers, and global freight settings.
"""

from django.core.exceptions import ValidationError
from django.db import models


class FreightSettings(models.Model):
    """
    Singleton model for global freight configuration.

    Only one instance should exist (enforced via clean/save).
    Contains fixed fees, percentage rates and optional distance pricing.
    """

    # Fixed fee applied to every shipment
    fixed_delivery_fee = models.DecimalField(
        'Taxa Fixa por Entrega (R$)',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Valor fixo adicionado independentemente do peso/volume'
    )

    # Percentage applied over the budget total value
    percentage_on_total = models.DecimalField(
        'Percentual sobre o Valor Total (%)',
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Percentual aplicado sobre o valor total do orçamento (ex: 5.00 = 5%)'
    )

    # Optional distance-based pricing
    distance_rate_enabled = models.BooleanField(
        'Habilitar Frete por Distância',
        default=False
    )
    distance_rate_per_km = models.DecimalField(
        'Taxa por Km (R$)',
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text='Custo por quilômetro rodado (requer que o orçamento informe a distância)'
    )

    # Calculation rule when both weight AND volume apply
    CALC_MODE_CHOICES = [
        ('max', 'Usar o maior valor (peso ou volume)'),
        ('sum', 'Somar peso e volume'),
        ('weight', 'Usar apenas peso'),
        ('volume', 'Usar apenas volume'),
    ]
    calculation_mode = models.CharField(
        'Modo de Cálculo',
        max_length=10,
        choices=CALC_MODE_CHOICES,
        default='max',
        help_text='Como combinar as tabelas de peso e volume'
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração de Frete'
        verbose_name_plural = 'Configuração de Frete'

    def __str__(self):
        return 'Configuração Global de Frete'

    def clean(self):
        if not self.pk and FreightSettings.objects.exists():
            raise ValidationError(
                'Só pode existir uma configuração de frete. Edite a existente.'
            )

    @classmethod
    def get_settings(cls):
        """Return the singleton instance, creating with defaults if absent."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class WeightRange(models.Model):
    """
    Pricing band for shipment weight.

    When rate_type is 'per_ton', the rate is multiplied by each additional
    tonne above min_weight (used for the open-ended last band).
    """

    RATE_TYPE_CHOICES = [
        ('fixed', 'Valor fixo para a faixa'),
        ('per_ton', 'R$ por tonelada'),
    ]

    label = models.CharField(
        'Descrição',
        max_length=100,
        help_text='Ex: Até 50 kg, De 51 a 100 kg'
    )
    min_weight = models.DecimalField(
        'Peso Mínimo (kg)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    max_weight = models.DecimalField(
        'Peso Máximo (kg)',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Deixe em branco para "acima de X"'
    )
    rate = models.DecimalField(
        'Valor (R$)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    rate_type = models.CharField(
        'Tipo de Valor',
        max_length=10,
        choices=RATE_TYPE_CHOICES,
        default='fixed'
    )
    order = models.PositiveSmallIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Faixa de Peso'
        verbose_name_plural = 'Faixas de Peso'
        ordering = ['order', 'min_weight']

    def __str__(self):
        return self.label


class VolumeRange(models.Model):
    """
    Pricing band for shipment volume (m³).

    When rate_type is 'per_m3', the rate is multiplied by each additional
    m³ above min_volume (used for the open-ended last band).
    """

    RATE_TYPE_CHOICES = [
        ('fixed', 'Valor fixo para a faixa'),
        ('per_m3', 'R$ por m³ adicional'),
    ]

    label = models.CharField(
        'Descrição',
        max_length=100,
        help_text='Ex: Até 1 m³, De 1 a 5 m³'
    )
    min_volume = models.DecimalField(
        'Volume Mínimo (m³)',
        max_digits=10,
        decimal_places=3,
        default=0
    )
    max_volume = models.DecimalField(
        'Volume Máximo (m³)',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Deixe em branco para "acima de X"'
    )
    rate = models.DecimalField(
        'Valor (R$)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    rate_type = models.CharField(
        'Tipo de Valor',
        max_length=10,
        choices=RATE_TYPE_CHOICES,
        default='fixed'
    )
    order = models.PositiveSmallIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Faixa de Volume'
        verbose_name_plural = 'Faixas de Volume'
        ordering = ['order', 'min_volume']

    def __str__(self):
        return self.label


class UrgencyMultiplier(models.Model):
    """
    Delivery urgency level with a price multiplier.

    The multiplier is applied to the freight sub-total
    after weight/volume/fixed-fee calculations.
    """

    label = models.CharField('Nome', max_length=80)
    description = models.CharField(
        'Descrição',
        max_length=200,
        blank=True
    )
    multiplier = models.DecimalField(
        'Multiplicador',
        max_digits=5,
        decimal_places=2,
        default=1,
        help_text='1.00 = sem acréscimo, 1.50 = +50%, 2.00 = 100% a mais'
    )
    is_default = models.BooleanField(
        'Padrão',
        default=False,
        help_text='Urgência selecionada por padrão nos orçamentos'
    )

    class Meta:
        verbose_name = 'Urgência de Entrega'
        verbose_name_plural = 'Urgências de Entrega'
        ordering = ['multiplier']

    def __str__(self):
        return f"{self.label} (×{self.multiplier})"

    def save(self, *args, **kwargs):
        # Ensure only one default urgency at a time
        if self.is_default:
            UrgencyMultiplier.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
