from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Artigo


class ArtigoListView(View):
    template_name = "blog/artigo_list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        artigos = Artigo.objects.filter(publicado=True).order_by(
            "-data_publicacao", "-data_criacao"
        )

        return render(request, self.template_name, context={"artigos": artigos})


class ArtigoDetailView(View):
    template_name = "blog/artigo_detail.html"

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        try:
            artigo = Artigo.objects.filter(publicado=True).get(slug=slug)
            comentarios = artigo.comentarios.filter(aprovado=True).order_by(
                "data_criacao"
            )
        except Artigo.DoesNotExist:
            raise Http404("Artigo não encontrado")

        context = {"artigo": artigo, "comentarios": comentarios}

        return render(request, self.template_name, context)
