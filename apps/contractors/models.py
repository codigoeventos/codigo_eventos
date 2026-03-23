"""
Contractor models for event contractor management.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.common.models import BaseModel
from apps.common.utils import validate_cpf, format_cpf


class Contractor(BaseModel):
    """
    Contractor model representing a subcontractor company linked to events.
    """

    name = models.CharField(
        'Razão Social',
        max_length=255,
        help_text='Razão social da empreiteira'
    )

    trade_name = models.CharField(
        'Nome Fantasia',
        max_length=255,
        blank=True,
        null=True,
        help_text='Nome fantasia da empreiteira'
    )

    cnpj = models.CharField(
        'CNPJ',
        max_length=18,
        blank=True,
        null=True,
        help_text='Ex: 00.000.000/0001-00'
    )

    state_registration = models.CharField(
        'Inscrição Estadual',
        max_length=30,
        blank=True,
        null=True,
    )

    legal_representative = models.CharField(
        'Responsável Legal',
        max_length=255,
        blank=True,
        null=True,
        help_text='Nome do responsável legal pela empresa'
    )

    # Contact
    phone = models.CharField(
        'Telefone',
        max_length=50,
        blank=True,
        null=True
    )

    email = models.EmailField(
        'E-mail',
        blank=True,
        null=True
    )

    website = models.URLField(
        'Website',
        blank=True,
        null=True
    )

    # Address
    address_street = models.CharField(
        'Logradouro',
        max_length=255,
        blank=True,
        null=True
    )

    address_number = models.CharField(
        'Número',
        max_length=20,
        blank=True,
        null=True
    )

    address_complement = models.CharField(
        'Complemento',
        max_length=100,
        blank=True,
        null=True
    )

    address_neighborhood = models.CharField(
        'Bairro',
        max_length=100,
        blank=True,
        null=True
    )

    address_city = models.CharField(
        'Cidade',
        max_length=100,
        blank=True,
        null=True
    )

    address_state = models.CharField(
        'Estado',
        max_length=2,
        blank=True,
        null=True,
        help_text='Sigla do estado (ex: SP)'
    )

    address_zip = models.CharField(
        'CEP',
        max_length=10,
        blank=True,
        null=True
    )

    # Banking data
    bank_name = models.CharField(
        'Banco',
        max_length=100,
        blank=True,
        null=True
    )

    bank_agency = models.CharField(
        'Agência',
        max_length=20,
        blank=True,
        null=True
    )

    bank_account = models.CharField(
        'Conta',
        max_length=30,
        blank=True,
        null=True
    )

    bank_account_type = models.CharField(
        'Tipo de Conta',
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('corrente', 'Corrente'),
            ('poupanca', 'Poupança'),
        ]
    )

    bank_pix_key = models.CharField(
        'Chave PIX',
        max_length=150,
        blank=True,
        null=True
    )

    # Documentation
    certifications = models.TextField(
        'Certificações e Alvarás',
        blank=True,
        null=True,
        help_text='Descreva as certificações, alvarás e documentações da empresa'
    )

    notes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Empreiteira'
        verbose_name_plural = 'Empreiteiras'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        parts = list(filter(None, [
            self.address_street,
            self.address_number,
            self.address_complement,
            self.address_neighborhood,
            self.address_city,
            self.address_state,
            self.address_zip,
        ]))
        return ', '.join(parts)


class ContractorMember(models.Model):
    """
    Member / worker belonging to a contractor company.
    """

    EXAM_TYPE_CHOICES = [
        ('admissional', 'Admissional'),
        ('periodico', 'Periódico'),
        ('retorno', 'Retorno ao Trabalho'),
        ('mudanca_funcao', 'Mudança de Função'),
        ('demissional', 'Demissional'),
    ]

    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Empreiteira',
        null=True,
        blank=True
    )

    # --- Dados Pessoais ---
    name = models.CharField(
        'Nome Completo',
        max_length=255
    )

    rg = models.CharField(
        'RG',
        max_length=30,
        blank=True,
        null=True
    )

    cpf = models.CharField(
        'CPF',
        max_length=14,
        blank=True,
        null=True,
        help_text='Ex: 000.000.000-00'
    )

    birth_date = models.DateField(
        'Data de Nascimento',
        blank=True,
        null=True
    )

    photo = models.ImageField(
        'Foto do Profissional',
        upload_to='contractor_members/photos/',
        blank=True,
        null=True
    )

    # --- Dados Profissionais ---
    role = models.CharField(
        'Função/Cargo',
        max_length=100,
        blank=True,
        default='',
        help_text='Ex: Técnico de Som, Iluminador, Eletricista, etc.'
    )

    specialty = models.CharField(
        'Especialidade',
        max_length=150,
        blank=True,
        null=True
    )

    experience_years = models.PositiveSmallIntegerField(
        'Tempo de Experiência (anos)',
        blank=True,
        null=True
    )

    # --- Documentação Trabalhista: ASO ---
    aso_number = models.CharField(
        'Número ASO',
        max_length=50,
        blank=True,
        null=True,
        help_text='Número do Atestado de Saúde Ocupacional'
    )

    aso_issue_date = models.DateField(
        'Data de Emissão do ASO',
        blank=True,
        null=True
    )

    aso_expiry_date = models.DateField(
        'Data de Validade do ASO',
        blank=True,
        null=True
    )

    aso_exam_type = models.CharField(
        'Tipo de Exame ASO',
        max_length=20,
        blank=True,
        null=True,
        choices=EXAM_TYPE_CHOICES
    )

    aso_file = models.FileField(
        'ASO (upload)',
        upload_to='contractor_members/aso/',
        blank=True,
        null=True
    )

    # --- Contato ---
    phone = models.CharField(
        'Telefone Celular',
        max_length=50,
        blank=True,
        null=True
    )

    emergency_phone = models.CharField(
        'Telefone de Emergência',
        max_length=50,
        blank=True,
        null=True
    )

    email = models.EmailField(
        'E-mail',
        blank=True,
        null=True
    )

    # --- Endereço ---
    address_street = models.CharField('Logradouro', max_length=255, blank=True, null=True)
    address_number = models.CharField('Número', max_length=20, blank=True, null=True)
    address_complement = models.CharField('Complemento', max_length=100, blank=True, null=True)
    address_neighborhood = models.CharField('Bairro', max_length=100, blank=True, null=True)
    address_city = models.CharField('Cidade', max_length=100, blank=True, null=True)
    address_state = models.CharField('Estado', max_length=2, blank=True, null=True)
    address_zip = models.CharField('CEP', max_length=10, blank=True, null=True)

    # --- Observações ---
    notes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Membro da Empreiteira'
        verbose_name_plural = 'Membros da Empreiteira'
        ordering = ['name']

    def __str__(self):
        contractor_name = self.contractor.name if self.contractor else 'Sem empreiteira'
        return f"{self.name} ({contractor_name})"

    # ------------------------------------------------------------------ #
    # Validity helpers
    # ------------------------------------------------------------------ #

    @property
    def aso_is_valid(self):
        if self.aso_expiry_date:
            return self.aso_expiry_date >= timezone.now().date()
        return None

    @property
    def days_until_aso_expiry(self):
        """Days until ASO expires. Negative = already expired."""
        if self.aso_expiry_date:
            return (self.aso_expiry_date - timezone.now().date()).days
        return None

    @property
    def nr_doc_status(self):
        """Worst NR status across all linked NRs: 'expired'|'expiring_soon'|'valid'|'no_doc'"""
        nrs = list(self.nrs.all())
        if not nrs:
            return 'no_doc'
        statuses = [nr.doc_status for nr in nrs]
        if 'expired' in statuses:
            return 'expired'
        if 'expiring_soon' in statuses:
            return 'expiring_soon'
        return 'valid'

    @property
    def aso_doc_status(self):
        """Returns: 'expired' | 'expiring_soon' (<=30d) | 'valid' | 'no_doc'"""
        d = self.days_until_aso_expiry
        if d is None:
            return 'no_doc'
        if d < 0:
            return 'expired'
        if d <= 30:
            return 'expiring_soon'
        return 'valid'

    @property
    def is_blocked_from_events(self):
        """True if any tracked document has already expired."""
        return self.nr_doc_status == 'expired' or self.aso_doc_status == 'expired'

    @property
    def worst_doc_status(self):
        """Overall worst status across NR and ASO."""
        statuses = [self.nr_doc_status, self.aso_doc_status]
        if 'expired' in statuses:
            return 'expired'
        if 'expiring_soon' in statuses:
            return 'expiring_soon'
        if 'valid' in statuses:
            return 'valid'
        return 'no_doc'

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #

    def clean(self):
        super().clean()
        errors = {}

        # CPF: format + digit validation + duplicate check
        if self.cpf:
            if not validate_cpf(self.cpf):
                errors['cpf'] = 'CPF inválido. Verifique os dígitos informados.'
            else:
                self.cpf = format_cpf(self.cpf)
                qs = ContractorMember.objects.filter(cpf=self.cpf)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                if qs.exists():
                    other = qs.first()
                    contractor_name = other.contractor.name if other.contractor else 'sem empreiteira'
                    errors['cpf'] = (
                        f'CPF já cadastrado para {other.name} ({contractor_name}).'
                    )

        if errors:
            raise ValidationError(errors)


class ContractorVehicle(models.Model):
    """
    A vehicle belonging to a Contractor.
    A contractor can have multiple vehicles.
    """

    FUEL_CHOICES = [
        ('gasolina', 'Gasolina'),
        ('etanol', 'Etanol'),
        ('flex', 'Flex'),
        ('diesel', 'Diesel'),
        ('eletrico', 'Elétrico'),
        ('hibrid', 'Híbrido'),
    ]

    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Empreiteira',
    )

    plate = models.CharField(
        'Placa',
        max_length=10,
        help_text='Ex: ABC-1234 ou ABC1D23',
    )

    brand = models.CharField(
        'Marca',
        max_length=60,
        blank=True,
        null=True,
    )

    model = models.CharField(
        'Modelo',
        max_length=60,
        blank=True,
        null=True,
    )

    year = models.PositiveSmallIntegerField(
        'Ano',
        blank=True,
        null=True,
    )

    color = models.CharField(
        'Cor',
        max_length=40,
        blank=True,
        null=True,
    )

    fuel = models.CharField(
        'Combustível',
        max_length=10,
        blank=True,
        null=True,
        choices=FUEL_CHOICES,
    )

    notes = models.TextField(
        'Observações',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['plate']

    def __str__(self):
        parts = [self.plate]
        if self.brand and self.model:
            parts.append(f'{self.brand} {self.model}')
        if self.year:
            parts.append(str(self.year))
        return ' – '.join(parts)


class ContractorMemberNR(models.Model):
    """
    A single NR (Norma Regulamentadora) certification belonging to a ContractorMember.
    A member can hold multiple NRs (e.g. NR-10, NR-35, NR-33).
    """

    member = models.ForeignKey(
        ContractorMember,
        on_delete=models.CASCADE,
        related_name='nrs',
        verbose_name='Membro',
    )

    nr_number = models.CharField(
        'Número NR',
        max_length=20,
        help_text='Ex: NR-10, NR-35, NR-33',
    )

    nr_certificate_expiry = models.DateField(
        'Validade do Certificado',
        blank=True,
        null=True,
    )

    nr_certificate_file = models.FileField(
        'Certificado NR (upload)',
        upload_to='contractor_members/nr_certificates/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Certificado NR'
        verbose_name_plural = 'Certificados NR'
        ordering = ['nr_number']

    def __str__(self):
        return f"{self.nr_number} – {self.member.name}"

    # ------------------------------------------------------------------ #
    # Validity helpers
    # ------------------------------------------------------------------ #

    @property
    def days_until_expiry(self):
        if self.nr_certificate_expiry:
            return (self.nr_certificate_expiry - timezone.now().date()).days
        return None

    @property
    def doc_status(self):
        """Returns: 'expired' | 'expiring_soon' (<=30d) | 'valid' | 'no_doc'"""
        d = self.days_until_expiry
        if d is None:
            return 'no_doc'
        if d < 0:
            return 'expired'
        if d <= 30:
            return 'expiring_soon'
        return 'valid'


class ContractorMemberNRFile(models.Model):
    """
    Additional certificate files for a single NR entry.
    Allows uploading multiple documents per NR (e.g. front + back of certificate).
    """

    nr = models.ForeignKey(
        ContractorMemberNR,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='NR',
    )

    file = models.FileField(
        'Arquivo',
        upload_to='contractor_members/nr_certificates/',
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Arquivo NR'
        verbose_name_plural = 'Arquivos NR'
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Arquivo – {self.nr}"


class EventContractor(models.Model):
    """
    Association between an event and a contractor company.
    """

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='contractors',
        verbose_name='Evento'
    )

    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.CASCADE,
        related_name='event_assignments',
        verbose_name='Empreiteira'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Empreiteira do Evento'
        verbose_name_plural = 'Empreiteiras dos Eventos'
        unique_together = [['event', 'contractor']]
        ordering = ['event', 'contractor']

    def __str__(self):
        return f"{self.event} - {self.contractor}"

    def clean(self):
        """Block assignment when the contractor has members with expired docs."""
        super().clean()
        # Only enforce on new (first-time) assignments to avoid retro-locking
        if self.pk or not self.contractor_id:
            return
        blocked = [
            m for m in self.contractor.members.all()
            if m.is_blocked_from_events
        ]
        if blocked:
            names = ', '.join(m.name for m in blocked)
            raise ValidationError(
                f'Não é possível vincular {self.contractor.name} a este evento: '
                f'os seguintes profissionais possuem documentação vencida — {names}. '
                'Atualize a documentação antes de prosseguir.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class EventContractorMember(models.Model):
    """
    Selected member of a contractor for a specific event assignment.
    """

    assignment = models.ForeignKey(
        EventContractor,
        on_delete=models.CASCADE,
        related_name='selected_members',
        verbose_name='Vínculo Empreiteira-Evento'
    )

    member = models.ForeignKey(
        ContractorMember,
        on_delete=models.CASCADE,
        related_name='event_participations',
        verbose_name='Membro'
    )

    class Meta:
        verbose_name = 'Membro em Evento'
        verbose_name_plural = 'Membros em Eventos'
        unique_together = [['assignment', 'member']]
        ordering = ['member__name']

    def __str__(self):
        return f"{self.member.name} — {self.assignment}"
