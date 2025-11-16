[![Tests](https://github.com/rodbv/dicas-orm-pysul2025/actions/workflows/tests.yml/badge.svg)](https://github.com/rodbv/dicas-orm-pysul2025/actions/workflows/tests.yml)

# ORMs em Python - PySul 2025

Projeto de exemplo para a apresentação sobre boas práticas de ORM em Python/Django.

## 📊 Slides da Apresentação

- **Google Slides**: [ORMs em Python - PySul 2025](https://docs.google.com/presentation/d/1npM5xOY82dOzDhR3r6Reh6k_ijWdZHsiP_CkejXCl5g/edit?usp=sharing)

## 🚀 Sobre o Projeto

Este projeto demonstra boas práticas de uso de ORM no Django, incluindo:

- Otimização de queries com `select_related()` e `prefetch_related()`
- Uso de `.only()` e `.defer()` para reduzir uso de memória
- Padrão View → Serviço → DTO
- Testes de performance com `assertNumQueries`
- Estratégia de testes: separação entre testes de serviço e testes de view

## 🛠️ Tecnologias

- Django 5.2+
- Python 3.13+
- pytest + pytest-django
- model-bakery
- ruff (linting e formatação)

## 📦 Instalação

```bash
# Instalar dependências
uv sync --all-groups

# Aplicar migrations
uv run python manage.py migrate

# Rodar testes
uv run pytest blog/tests/ -v
```

## 📚 Estrutura do Projeto

```
blog/
├── models.py          # Modelos Django
├── services/          # Camada de serviços (lógica de negócio)
│   └── artigo_service.py
├── dto.py            # Data Transfer Objects
├── views.py          # Views (finais, apenas HTTP)
└── tests/
    ├── test_artigo_service.py  # Testes de regras de negócio
    └── test_views.py           # Testes de comportamento HTTP
```

## 🧪 Testes

```bash
# Todos os testes
uv run pytest blog/tests/ -v

# Apenas testes de serviço
uv run pytest blog/tests/test_artigo_service.py -v

# Apenas testes de view
uv run pytest blog/tests/test_views.py -v
```

## 📖 Diretrizes

Consulte [`AGENTS.md`](./AGENTS.md) para diretrizes completas do projeto, incluindo:

- Estilo de código (PEP 8)
- TDD (Test-Driven Development)
- Padrões Django
- Boas práticas de ORM

## 🔗 Links Úteis

- [Documentação do Django ORM](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [Django QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)

