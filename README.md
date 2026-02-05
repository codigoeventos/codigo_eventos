# Django Project Template

Template simples e funcional para projetos Django com Docker, PostgreSQL e Redis.

## 🚀 Features

- Django 5.0+ com Django REST Framework
- PostgreSQL como banco de dados
- Redis para cache e Celery
- Docker e Docker Compose
- Celery para tarefas assíncronas
- Autenticação JWT
- Documentação automática da API (Swagger)

## 📋 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (recomendado)

## 🔧 Instalação

### Opção 1: Com Docker (Recomendado)

1. Clone o repositório e configure o ambiente:
```bash
git clone <seu-repositorio>
cd django_project_template
cp .env.example .env
```

2. Edite o arquivo `.env` com suas configurações

3. Inicie os containers:
```bash
docker-compose up --build
```

4. Em outro terminal, execute as migrações e crie um superusuário:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

5. Acesse: `http://localhost:8000`

### Opção 2: Desenvolvimento Local

1. Clone e configure:
```bash
git clone <seu-repositorio>
cd django_project_template
cp .env.example .env
```

2. Crie o ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Inicie o servidor:
```bash
python manage.py runserver
```

## 📁 Estrutura do Projeto

```
django_project_template/
├── apps/               # Apps Django
│   └── core/          # App de exemplo
├── config/            # Configurações do projeto
│   ├── settings/     # Settings (base, local, production)
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── static/           # Arquivos estáticos
├── media/            # Uploads
├── requirements.txt  # Dependências
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

## 🛠️ Comandos Úteis

### Django
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Criar nova app
python manage.py startapp nome_app apps/nome_app
```

### Docker
```bash
# Iniciar
docker-compose up

# Parar
docker-compose down

# Ver logs
docker-compose logs -f web

# Executar comandos
docker-compose exec web python manage.py <comando>
```

### Celery
```bash
# Worker
celery -A config worker -l info

# Beat (agendador)
celery -A config beat -l info
```

## 🌐 Endpoints

- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`
- Swagger: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 🚀 Deploy

1. Configure as variáveis de ambiente de produção no `.env`
2. Defina `DEBUG=False`
3. Configure `ALLOWED_HOSTS`
4. Use um `SECRET_KEY` seguro
5. Configure o banco de dados de produção

## 📝 Próximos Passos

Após clonar o template:

1. Renomeie o projeto conforme necessário
2. Configure suas variáveis de ambiente
3. Crie suas próprias apps
4. Customize os models, views e serializers
5. Adicione suas funcionalidades

## 📄 Licença

MIT
