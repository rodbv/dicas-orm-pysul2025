import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertNumQueries

from blog.models import Artigo, Comentario, Tag


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def tag(db):
    return Tag.objects.create(nome="Python", slug="python")


@pytest.fixture
def artigo(db, user, tag):
    artigo = Artigo.objects.create(
        titulo="Artigo de Teste",
        slug="artigo-de-teste",
        autor=user,
        conteudo="<p>Conteúdo do artigo</p>",
        resumo="<p>Resumo do artigo</p>",
        publicado=True,
    )
    artigo.tags.add(tag)
    return artigo


@pytest.fixture
def comentarios(db, artigo, user):
    comentario1 = Comentario.objects.create(
        artigo=artigo,
        autor=user,
        texto="<p>Primeiro comentário</p>",
        aprovado=True,
    )
    comentario2 = Comentario.objects.create(
        artigo=artigo,
        autor=user,
        texto="<p>Segundo comentário</p>",
        aprovado=True,
    )
    return [comentario1, comentario2]


@pytest.mark.django_db
def test_artigo_detail_view_num_queries(client, artigo, comentarios):
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    # assertNumQueries conta todas as queries, incluindo as do Django
    # Mas podemos usar um range para ser mais flexível
    # O importante é que não haja N+1 (muitas queries extras)
    with assertNumQueries(5):  # 3 principais + 2 extras do Django (refresh_from_db)
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_artigo_detail_view_dto_structure(client, artigo, comentarios):
    from blog.dto import ArtigoDetailDTO, AutorDTO, ComentarioDTO, TagDTO

    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})
    response = client.get(url)

    assert response.status_code == 200

    artigo_dto = response.context["artigo"]
    comentarios_dto = response.context["comentarios"]

    assert isinstance(artigo_dto, ArtigoDetailDTO)
    assert isinstance(artigo_dto.autor, AutorDTO)
    assert isinstance(artigo_dto.tags[0], TagDTO)
    assert isinstance(comentarios_dto[0], ComentarioDTO)
    assert isinstance(comentarios_dto[0].autor, AutorDTO)

    assert artigo_dto.titulo == "Artigo de Teste"
    assert artigo_dto.autor.username == "testuser"
    assert artigo_dto.autor.full_name == "Test User"
    assert len(artigo_dto.tags) == 1
    assert artigo_dto.tags[0].nome == "Python"
    assert len(comentarios_dto) == 2


@pytest.mark.django_db
def test_artigo_detail_view_sem_comentarios(client, artigo):
    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    with assertNumQueries(3):
        response = client.get(url)
        assert response.status_code == 200

    comentarios_dto = response.context["comentarios"]
    assert len(comentarios_dto) == 0


@pytest.mark.django_db
def test_artigo_detail_view_artigo_nao_publicado(client, user, tag):
    artigo = Artigo.objects.create(
        titulo="Artigo Privado",
        slug="artigo-privado",
        autor=user,
        conteudo="<p>Conteúdo</p>",
        publicado=False,
    )

    url = reverse("blog:artigo_detail", kwargs={"slug": artigo.slug})

    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_artigo_list_view_num_queries(client, artigo):
    url = reverse("blog:artigo_list")

    with assertNumQueries(2):
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_artigo_list_view_dto_structure(client, artigo):
    from blog.dto import ArtigoListDTO, AutorDTO, TagDTO

    url = reverse("blog:artigo_list")
    response = client.get(url)

    assert response.status_code == 200

    artigos = response.context["artigos"]

    assert len(artigos) == 1
    assert isinstance(artigos[0], ArtigoListDTO)
    assert isinstance(artigos[0].autor, AutorDTO)
    assert isinstance(artigos[0].tags[0], TagDTO)

    assert artigos[0].titulo == "Artigo de Teste"
    assert artigos[0].autor.username == "testuser"
    assert artigos[0].autor.full_name == "Test User"
    assert len(artigos[0].tags) == 1
    assert artigos[0].tags[0].nome == "Python"
    assert artigos[0].data_exibicao is not None


@pytest.mark.django_db
def test_artigo_list_view_sem_artigos(client):
    url = reverse("blog:artigo_list")

    with assertNumQueries(1):
        response = client.get(url)
        assert response.status_code == 200

    artigos = response.context["artigos"]
    assert len(artigos) == 0
