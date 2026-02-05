# Sistema de Gestão de Eventos

Sistema web interno para gerenciamento completo de eventos, contemplando fluxo comercial, operacional e técnico.

## 🎯 Características

- **Autenticação por E-mail**: Login usando endereço de e-mail
- **RBAC (Controle de Acesso Baseado em Funções)**: 4 grupos de usuários
- **Auditoria Completa**: Rastreamento de criação/atualização com histórico
- **Soft Delete**: Exclusão lógica de registros
- **Design Minimalista**: Interface em preto/branco/cinza com Tailwind CSS

## 📋 Módulos do Sistema

### Núcleo
- **Clientes**: Cadastro de clientes (CPF/CNPJ) com validação
- **Eventos**: Evento como raiz agregada do sistema
- **Equipes**: Membros da equipe e alocação por evento

### Comercial
- **Propostas**: Propostas comerciais para eventos
- **Orçamentos**: Orçamentos detalhados com itens e totais automáticos

### Operacional
- **Ordens de Serviço**: Criadas automaticamente ao aprovar orçamento
- **Visitas Técnicas**: Agendamento e documentação de visitas
- **Documentos**: ARTs, seguros, certificados, etc.

## 🚀 Início Rápido com Docker

### 1. Clonar e Configurar

```bash
cd /home/rafael-pinheiro/Documentos/CODE/CODIGO\ DE\ EVENTOS/codigo_eventos
```

### 2. Subir os Containers

```bash
docker-compose up -d
```

### 3. Criar Superusuário

```bash
docker-compose exec web python manage.py createsuperuser
```

Forneça:
- **E-mail**: seu@email.com
- **Nome**: Seu Nome
- **Sobrenome**: Sobrenome
- **Senha**: (mínimo 8 caracteres)

### 4. Acessar o Sistema

- **Sistema**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## 👥 Grupos de Usuários (RBAC)

Os grupos foram criados automaticamente:

- **Administrador**: Acesso total ao sistema
- **Comercial**: Propostas, orçamentos, clientes, eventos (visualização)
- **Operacional**: Ordens de serviço, equipes, documentos
- **Técnico**: Visitas técnicas, eventos (visualização)

Para atribuir um grupo a um usuário, acesse o admin Django.

## 🛠️ Comandos Úteis

### Gerenciar Containers

```bash
# Ver logs
docker-compose logs -f web

# Parar containers
docker-compose down

# Reiniciar
docker-compose restart

# Rebuild após mudanças no código
docker-compose up -d --build
```

### Django Management

```bash
# Criar migrações
docker-compose exec web python manage.py makemigrations

# Aplicar migrações
docker-compose exec web python manage.py migrate

# Criar grupos RBAC
docker-compose exec web python manage.py create_groups

# Shell Django
docker-compose exec web python manage.py shell

# Acessar PostgreSQL
docker-compose exec db psql -U eventos_user -d eventos_db
```

## 📁 Estrutura do Projeto

```
codigo_eventos/
├── apps/
│   ├── accounts/          # Autenticação e usuários
│   ├── clients/           # Clientes
│   ├── events/            # Eventos (raiz agregada)
│   ├── proposals/         # Propostas comerciais
│   ├── budgets/           # Orçamentos
│   ├── service_orders/    # Ordens de serviço
│   ├── technical_visits/  # Visitas técnicas
│   ├── teams/             # Equipes
│   ├── documents/         # Documentos
│   ├── dashboard/         # Dashboard principal
│   └── common/            # Modelos e utilitários comuns
├── config/                # Configurações do Django
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos
├── media/                 # Uploads de arquivos
└── docker-compose.yml     # Configuração Docker
```

## 🎨 Stack Tecnológico

- **Backend**: Django 5.0, Python 3.12+
- **Banco de Dados**: PostgreSQL 16
- **Frontend**: Django Templates, Tailwind CSS (CDN)
- **Containerização**: Docker & Docker Compose
- **Auditoria**: django-simple-history
- **Soft Delete**: django-safedelete
- **Forms**: django-crispy-forms com crispy-tailwind

## 🔧 Desenvolvimento Local (Sem Docker)

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edite .env com suas configurações de banco

# Rodar migrações
python manage.py migrate

# Criar grupos
python manage.py create_groups

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

## 📝 Fluxo de Trabalho Principal

1. **Cadastrar Cliente** → Clientes
2. **Criar Evento** → Eventos (vinculado ao cliente)
3. **Agendar Visita Técnica** → Visitas Técnicas
4. **Criar Proposta** → Propostas (para o evento)
5. **Adicionar Orçamento** → Orçamentos (dentro da proposta)
6. **Aprovar Orçamento** → Status = "approved"
7. **Ordem de Serviço Criada Automaticamente** ✨
8. **Executar OS** → Atualizar status dos itens
9. **Anexar Documentos** → ARTs, seguros, etc.

## 🔐 Segurança

- Autenticação obrigatória para todas as páginas (exceto login)
- Controle de permissões por grupo
- CSRF protection ativo
- Senhas hasheadas com PBKDF2
- Histórico completo de alterações
- Soft delete (nenhum dado é perdido)

## 📊 Próximas Funcionalidades

- [ ] Integração WhatsApp
- [ ] Módulo Financeiro
- [ ] Sistema de Notificações
- [ ] Checklist de Eventos
- [ ] Link Público para Aprovação de Orçamento
- [ ] Relatórios e Dashboard Avançado

## 📄 Licença

MIT

---

**Desenvolvido para gestão interna de eventos** | 2026
