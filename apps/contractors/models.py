"""
Contractor models for event contractor management.
"""

from django.db import models
from django.utils import timezone
from apps.common.models import BaseModel


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

    # --- Documentação Trabalhista: NR ---
    nr_number = models.CharField(
        'Número NR',
        max_length=10,
        blank=True,
        null=True,
        help_text='Ex: NR-10, NR-35, NR-33'
    )

    nr_certificate_expiry = models.DateField(
        'Data de Validade do Certificado NR',
        blank=True,
        null=True
    )

    nr_certificate_file = models.FileField(
        'Certificado NR (upload)',
        upload_to='contractor_members/nr_certificates/',
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

    @property
    def aso_is_valid(self):
        if self.aso_expiry_date:
            return self.aso_expiry_date >= timezone.now().date()
        return None

    @property
    def nr_is_valid(self):
        if self.nr_certificate_expiry:
            return self.nr_certificate_expiry >= timezone.now().date()
        return None


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
