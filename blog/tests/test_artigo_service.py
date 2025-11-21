import pytest
from django.contrib.auth.models import User
from freezegun import freeze_time
from model_bakery import baker
from pytest_django.asserts import assertNumQueries

from blog.dto import ArtigoDTO, ArtigoListDTO, AutorDTO, ComentarioDTO, TagDTO
from blog.models import Artigo, Comentario, Tag
from blog.services.artigo_service import (
    obter_artigo_dto_por_slug,
    obter_lista_artigos_dto,
)


@pytest.fixture
def user_fixture():
    def _wrapper(
        username: str = "testuser",
        first_name: str = "Test",
        last_name: str = "User",
    ):
        return baker.make(
            User, username=username, first_name=first_name, last_name=last_name
        )

    return _wrapper


@pytest.fixture
def tag_fixture():
    def _wrapper(nome: str = "Python", slug: str = "python"):
        return baker.make(Tag, nome=nome, slug=slug)

    return _wrapper


@pytest.fixture
def artigo_fixture(user_fixture, tag_fixture):
    def _wrapper(
        titulo: str = "Artigo de Teste",
        slug: str = "artigo-de-teste",
        conteudo: str = "<p>Conteúdo do artigo</p>",
        resumo: str = "<p>Resumo do artigo</p>",
        publicado: bool = True,
        tags: list | None = None,
        autor_param: User | None = None,
    ):
        if autor_param is None:
            autor_param = user_fixture()

        artigo = baker.make(
            Artigo,
            titulo=titulo,
            slug=slug,
            autor=autor_param,
            conteudo=conteudo,
            resumo=resumo,
            publicado=publicado,
        )
        if tags:
            artigo.tags.add(*tags)
        else:
            artigo.tags.add(tag_fixture())
        return artigo

    return _wrapper


@pytest.fixture
def comentario_fixture(artigo_fixture, user_fixture):
    def _wrapper(
        texto: str,
        aprovado: bool = True,
        data_criacao: str | None = None,
        quantity: int | None = None,
        artigo_param: Artigo | None = None,
        autor_param: User | None = None,
    ):
        artigo_para_usar = (
            artigo_param if artigo_param is not None else artigo_fixture()
        )
        autor_para_usar = autor_param if autor_param is not None else user_fixture()

        if data_criacao:
            with freeze_time(data_criacao):
                return baker.make(
                    Comentario,
                    artigo=artigo_para_usar,
                    autor=autor_para_usar,
                    texto=texto,
                    aprovado=aprovado,
                    _quantity=quantity,
                )
        return baker.make(
            Comentario,
            artigo=artigo_para_usar,
            autor=autor_para_usar,
            texto=texto,
            aprovado=aprovado,
            _quantity=quantity,
        )

    return _wrapper


@pytest.mark.django_db
def test_retorna_dto_com_queries_otimizadas(
    artigo_fixture,
    comentario_fixture,
):
    artigo = artigo_fixture()
    comentario_fixture(
        texto="<p>Comentário</p>",
        aprovado=True,
        quantity=2,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    # 3 queries otimizadas: artigo+autor (select_related), tags (prefetch_related), comentários+autores (prefetch_related com select_related)
    # Total: 3 queries (otimizado, sem N+1)
    with assertNumQueries(3):
        artigo_dto = obter_artigo_dto_por_slug(artigo.slug)

    assert isinstance(artigo_dto, ArtigoDTO)
    assert isinstance(artigo_dto.autor, AutorDTO)
    assert isinstance(artigo_dto.tags[0], TagDTO)
    assert isinstance(artigo_dto.comentarios[0], ComentarioDTO)
    assert isinstance(artigo_dto.comentarios[0].autor, AutorDTO)

    assert artigo_dto.titulo == "Artigo de Teste"
    assert artigo_dto.autor.username == "testuser"
    assert artigo_dto.autor.full_name == "Test User"
    assert len(artigo_dto.tags) == 1
    assert artigo_dto.tags[0].nome == "Python"
    assert len(artigo_dto.comentarios) == 2


@pytest.mark.django_db
def test_retorna_dto_sem_comentarios(
    artigo_fixture,
):
    artigo = artigo_fixture()
    with assertNumQueries(3):
        artigo_dto = obter_artigo_dto_por_slug(artigo.slug)

    assert isinstance(artigo_dto, ArtigoDTO)
    assert len(artigo_dto.comentarios) == 0


@pytest.mark.django_db
def test_retorna_lista_com_queries_otimizadas(artigo_fixture):
    artigo_fixture()
    # Uma query para o artigo e uma query para as tags
    with assertNumQueries(2):
        artigos = obter_lista_artigos_dto()

    assert len(artigos) == 1
    assert isinstance(artigos[0], ArtigoListDTO)
    assert isinstance(artigos[0].autor, AutorDTO)
    assert isinstance(artigos[0].tags[0], TagDTO)
    assert artigos[0].titulo == "Artigo de Teste"
    assert artigos[0].autor.username == "testuser"
    assert len(artigos[0].tags) == 1
    assert artigos[0].tags[0].nome == "Python"


@pytest.mark.django_db
def test_retorna_lista_vazia_quando_sem_artigos():
    with assertNumQueries(1):
        artigos = obter_lista_artigos_dto()

    assert len(artigos) == 0


@pytest.mark.django_db
def test_filtra_comentarios_nao_aprovados(
    artigo_fixture,
    comentario_fixture,
):
    artigo = artigo_fixture()
    comentario_fixture(
        texto="<p>Comentário não aprovado</p>",
        aprovado=False,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    artigo_dto = obter_artigo_dto_por_slug(artigo.slug)

    assert len(artigo_dto.comentarios) == 0


@pytest.mark.django_db
def test_retorna_apenas_comentarios_aprovados(
    artigo_fixture,
    comentario_fixture,
):
    artigo = artigo_fixture()
    aprovado = comentario_fixture(
        texto="<p>Comentário aprovado</p>",
        aprovado=True,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    comentario_fixture(
        texto="<p>Comentário não aprovado</p>",
        aprovado=False,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    artigo_dto = obter_artigo_dto_por_slug(artigo.slug)

    assert len(artigo_dto.comentarios) == 1
    assert artigo_dto.comentarios[0].texto == aprovado.texto


@pytest.mark.django_db
@freeze_time("2024-01-01")
def test_ordena_por_data_publicacao(
    user_fixture,
    tag_fixture,
    artigo_fixture,
):
    user = user_fixture()
    tag = tag_fixture()
    artigo_fixture(
        titulo="Artigo Antigo",
        slug="artigo-antigo",
        autor_param=user,
        tags=[tag],
    )

    with freeze_time("2024-01-02"):
        artigo_fixture(
            titulo="Artigo Recente",
            slug="artigo-recente",
            autor_param=user,
            tags=[tag],
        )

    artigos = obter_lista_artigos_dto()

    assert len(artigos) == 2
    assert artigos[0].titulo == "Artigo Recente"
    assert artigos[1].titulo == "Artigo Antigo"


@pytest.mark.django_db
@freeze_time("2024-01-01")
def test_ordena_por_data_criacao_quando_sem_publicacao(
    user_fixture,
    tag_fixture,
    artigo_fixture,
):
    user = user_fixture()
    tag = tag_fixture()
    with freeze_time("2024-01-01 10:00:00"):
        artigo_fixture(
            titulo="Artigo Primeiro",
            slug="artigo-primeiro",
            autor_param=user,
            tags=[tag],
        )

    with freeze_time("2024-01-01 11:00:00"):
        artigo_fixture(
            titulo="Artigo Segundo",
            slug="artigo-segundo",
            autor_param=user,
            tags=[tag],
        )

    artigos = obter_lista_artigos_dto()

    assert len(artigos) == 2
    assert artigos[0].titulo == "Artigo Segundo"
    assert artigos[1].titulo == "Artigo Primeiro"


@pytest.mark.django_db
def test_ordena_comentarios_por_data_criacao(
    artigo_fixture,
    comentario_fixture,
):
    artigo = artigo_fixture()
    comentario_fixture(
        texto="<p>Primeiro comentário</p>",
        aprovado=True,
        data_criacao="2024-01-01 10:00:00",
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    comentario_fixture(
        texto="<p>Segundo comentário</p>",
        aprovado=True,
        data_criacao="2024-01-01 11:00:00",
        artigo_param=artigo,
        autor_param=artigo.autor,
    )

    artigo_dto = obter_artigo_dto_por_slug(artigo.slug)

    assert len(artigo_dto.comentarios) == 2
    assert artigo_dto.comentarios[0].texto == "<p>Primeiro comentário</p>"
    assert artigo_dto.comentarios[1].texto == "<p>Segundo comentário</p>"


@pytest.mark.django_db
def test_levanta_doesnotexist_quando_artigo_inexistente():
    with pytest.raises(Artigo.DoesNotExist):
        obter_artigo_dto_por_slug("slug-inexistente")


@pytest.mark.django_db
def test_levanta_doesnotexist_quando_artigo_nao_publicado(
    user_fixture,
    artigo_fixture,
):
    user = user_fixture()
    artigo = artigo_fixture(
        autor_param=user,
        publicado=False,
    )

    with pytest.raises(Artigo.DoesNotExist):
        obter_artigo_dto_por_slug(artigo.slug)
