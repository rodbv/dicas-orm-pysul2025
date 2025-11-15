from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.views import View

from .dto import ArtigoDetailDTO, ArtigoListDTO, AutorDTO, ComentarioDTO, TagDTO
from .models import Artigo, Tag


class ArtigoListView(View):
    template_name = "blog/artigo_list.html"

    def get(self, request):
        artigos_qs = (
            Artigo.objects.filter(publicado=True)
            .only(
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
                    queryset=Tag.objects.only("nome"),
                )
            )
            .order_by("-data_publicacao", "-data_criacao")
        )

        artigos = [
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

        return render(request, self.template_name, context={"artigos": artigos})


class ArtigoDetailView(View):
    template_name = "blog/artigo_detail.html"

    def get(self, request, slug):
        artigo = get_object_or_404(
            Artigo.objects.filter(publicado=True)
            .only(
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
                    queryset=Tag.objects.only("nome"),
                )
            ),
            slug=slug,
        )

        comentarios_qs = (
            artigo.comentarios.filter(aprovado=True)
            .only(
                "texto",
                "data_criacao",
                "autor_id",
                "autor__username",
                "autor__first_name",
                "autor__last_name",
            )
            .select_related("autor")
            .order_by("data_criacao")
        )

        artigo_dto = ArtigoDetailDTO(
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
                for comentario in comentarios_qs
            ],
        )

        context = {"artigo": artigo_dto, "comentarios": artigo_dto.comentarios}

        return render(request, self.template_name, context)
