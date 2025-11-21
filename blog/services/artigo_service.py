from django.db.models import Prefetch

from blog.dto import ArtigoDTO, ArtigoListDTO, AutorDTO, ComentarioDTO, TagDTO
from blog.models import Artigo, Comentario, Tag


def obter_lista_artigos_dto() -> list[ArtigoListDTO]:
    artigos_qs = (
        Artigo.objects.filter(publicado=True)
        .only(
            "id",
            "titulo",
            "slug",
            "resumo",
            "data_publicacao",
            "data_criacao",
            "autor_id",
            "autor__username",
            "autor__first_name",
            "autor__last_name",
        )
        .select_related("autor")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.only("id", "nome"),
            )
        )
        .order_by("-data_publicacao", "-data_criacao")
    )

    return [
        ArtigoListDTO(
            titulo=artigo.titulo,
            slug=artigo.slug,
            resumo=artigo.resumo,
            data_publicacao=artigo.data_publicacao,
            data_criacao=artigo.data_criacao,
            autor=AutorDTO(
                username=artigo.autor.username,
                first_name=artigo.autor.first_name,
                last_name=artigo.autor.last_name,
            ),
            tags=[TagDTO(nome=tag.nome) for tag in artigo.tags.all()],
        )
        for artigo in artigos_qs
    ]


def obter_artigo_dto_por_slug(slug: str) -> ArtigoDTO:
    artigo = (
        Artigo.objects.filter(publicado=True)
        .only(
            "id",
            "titulo",
            "conteudo",
            "data_publicacao",
            "autor_id",
            "autor__username",
            "autor__first_name",
            "autor__last_name",
        )
        .select_related("autor")
        .prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.only("id", "nome"),
            ),
            Prefetch(
                "comentarios",
                queryset=Comentario.objects.filter(aprovado=True)
                .only(
                    "id",
                    "texto",
                    "data_criacao",
                    "artigo_id",
                    "autor_id",
                    "autor__username",
                    "autor__first_name",
                    "autor__last_name",
                )
                .select_related("autor")
                .order_by("data_criacao"),
            ),
        )
        .get(slug=slug)
    )

    return _construir_artigo_dto(artigo)


def _construir_artigo_dto(artigo: Artigo) -> ArtigoDTO:
    return ArtigoDTO(
        titulo=artigo.titulo,
        conteudo=artigo.conteudo,
        data_publicacao=artigo.data_publicacao,
        autor=AutorDTO(
            username=artigo.autor.username,
            first_name=artigo.autor.first_name,
            last_name=artigo.autor.last_name,
        ),
        tags=[TagDTO(nome=tag.nome) for tag in artigo.tags.all()],
        comentarios=[
            ComentarioDTO(
                texto=comentario.texto,
                data_criacao=comentario.data_criacao,
                autor=AutorDTO(
                    username=comentario.autor.username,
                    first_name=comentario.autor.first_name,
                    last_name=comentario.autor.last_name,
                ),
            )
            for comentario in artigo.comentarios.all()
        ],
    )
