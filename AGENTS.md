# Diretrizes de Projeto Django para Agentes de IA

Diretrizes concisas para projetos Django usando TDD e pytest.

## Estilo de Código (PEP 8)

- 4 espaços para indentação, linha máxima 88 caracteres
- snake_case para funções/variáveis, PascalCase para classes, UPPER_CASE para constantes
- Type hints obrigatórios: `def func(param: Type) -> ReturnType:`
- **Imports no topo do arquivo** (PEP 8): biblioteca padrão → terceiros → aplicação local, agrupados e ordenados
- Use `uv run isort .` para organizar imports

## TDD (Test-Driven Development)

1. **Vermelho**: Escreva teste que falha
2. **Verde**: Código mínimo para passar
3. **Refatorar**: Melhore mantendo testes verdes

- Testes antes da implementação
- Um teste = uma coisa
- Nomes em português, concisos, indicando o objetivo do teste
- Use `@pytest.mark.django_db` para acesso ao banco
- **Use `mocker` do pytest (pytest-mock) para mocks, nunca `unittest.mock`**

## Django - Models

**FAÇA:** `__str__`, `Meta` com `verbose_name`, `related_name` em ForeignKey/ManyToMany, índices para campos frequentes

**NÃO FAÇA:** Nomes genéricos, esquecer `on_delete` em ForeignKey, consultas desnecessárias (use `select_related`/`prefetch_related`)

## Django - Views

**FAÇA:** Class-based views, views finas (lógica em models/services), códigos HTTP apropriados

**NÃO FAÇA:** Lógica de negócio em views, consultas em loops, retornar dados sensíveis em erros

## Camada de Serviços

**PADRÃO OBRIGATÓRIO: View → Serviço → DTO**
- ✅ Sempre use o fluxo: View busca dados → Serviço processa → Retorna DTO
- ✅ Views nunca constroem DTOs diretamente
- ✅ Serviços sempre retornam DTOs hidratados

**FAÇA:**
- ✅ Crie camada de serviços (`services/`) para lógica de negócio e construção de DTOs
- ✅ Views devem apenas: buscar dados (queryset/objeto), chamar serviço, renderizar template
- ✅ Testes com `assertNumQueries` devem estar na camada de serviços, não nas views
- ✅ Serviços recebem objetos do ORM e retornam DTOs hidratados

**NÃO FAÇA:**
- ❌ Lógica de construção de DTOs em views
- ❌ Consultas complexas em views (mova para serviços)
- ❌ Testes de performance (`assertNumQueries`) em testes de view
- ❌ Views retornando objetos do ORM diretamente (sempre use DTOs)

## Django - Querysets

**FAÇA:** `select_related()` para ForeignKey, `prefetch_related()` para ManyToMany, `exists()` em vez de `count()`, `get_or_create()`/`update_or_create()`

**NÃO FAÇA:** `all()` quando pode filtrar, consultas em loops (N+1), `count()` só para verificar existência

## FAÇA ✅

- Testes primeiro (TDD)
- Funções/classes pequenas e focadas
- Nomes significativos
- Migrations para mudanças no banco
- Nomes de teste em português, concisos, indicando o objetivo
- Variáveis de ambiente para segredos
- `gettext_lazy` para strings traduzíveis
- Validação no nível do model
- Logging em vez de `print()`

## NÃO FAÇA ❌

- Commit de segredos
- URLs hardcoded (use `reverse()`)
- Consultas em templates
- `save()` em loops (use `bulk_create()`/`bulk_update()`)
- Imports no meio do arquivo
- Imports circulares
- `null=True` em CharField/TextField sem `blank=True`
- Comentários redundantes
- Docstrings desnecessárias (apenas quando agregam valor)

## Comandos Essenciais

```bash
# Testes
uv run pytest
uv run pytest --cov=. --cov-report=html

# Qualidade
uv run ruff format .
uv run ruff check --fix .
```

## Segurança

- Nunca commite `SECRET_KEY`
- `DEBUG=False` em produção
- Valide entrada do usuário
- Use CSRF protection
- Hash de senha do Django
