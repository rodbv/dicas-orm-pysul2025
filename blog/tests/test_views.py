import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from blog.dto import ArtigoDTO, AutorDTO
from blog.models import Artigo, Comentario, Tag


@pytest.fixture
def client():
    return Client()


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
            from freezegun import freeze_time

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
def test_obter_detalhe_artigo_quando_artigo_existe_deve_retornar_200(
    client, artigo_fixture, comentario_fixture
):
    artigo = artigo_fixture()
    comentario_fixture(
        texto="<p>Comentário</p>",
        aprovado=True,
        quantity=2,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_obter_detalhe_artigo_quando_artigo_tem_comentarios_deve_retornar_200(
    client, artigo_fixture, comentario_fixture
):
    artigo = artigo_fixture()
    comentario_fixture(
        texto="<p>Comentário</p>",
        aprovado=True,
        quantity=2,
        artigo_param=artigo,
        autor_param=artigo.autor,
    )
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_obter_detalhe_artigo_quando_artigo_nao_tem_comentarios_deve_retornar_200(
    client, artigo_fixture
):
    artigo = artigo_fixture()
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_obter_detalhe_artigo_quando_artigo_nao_publicado_deve_retornar_404(
    client, user_fixture, artigo_fixture
):
    user = user_fixture()
    artigo = artigo_fixture(
        autor_param=user, publicado=False, conteudo="<p>Conteúdo</p>"
    )

    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_obter_detalhe_artigo_quando_slug_nao_existe_deve_retornar_404(client):
    url = reverse("blog:artigo_detail", kwargs={"slug": "slug-inexistente"})

    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_obter_lista_artigos_quando_artigos_existem_deve_retornar_200(
    client, artigo_fixture
):
    artigo_fixture()
    url = reverse("blog:artigo_list")

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_obter_lista_artigos_quando_nao_ha_artigos_deve_retornar_200(client):
    url = reverse("blog:artigo_list")

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_artigo_detail_view_chama_servico_correto(client, artigo_fixture, mocker):
    artigo = artigo_fixture()
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    mock_service = mocker.patch("blog.views.obter_artigo_dto_por_slug")
    mock_service.return_value = ArtigoDTO(
        titulo=artigo.titulo,
        conteudo=artigo.conteudo,
        data_publicacao=artigo.data_publicacao,
        autor=AutorDTO(
            username=artigo.autor.username,
            first_name=artigo.autor.first_name,
            last_name=artigo.autor.last_name,
        ),
        tags=[],
        comentarios=[],
    )

    response = client.get(url)

    assert response.status_code == 200
    mock_service.assert_called_once_with(artigo.slug)


@pytest.mark.django_db
def test_artigo_list_view_chama_servico_correto(client, mocker):
    url = reverse("blog:artigo_list")

    mock_service = mocker.patch("blog.views.obter_lista_artigos_dto")
    mock_service.return_value = []

    response = client.get(url)

    assert response.status_code == 200
    mock_service.assert_called_once()
