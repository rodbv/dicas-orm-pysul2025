from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Artigo
from .services.artigo_service import obter_artigo_dto_por_slug, obter_lista_artigos_dto


class ArtigoListView(View):
    template_name = "blog/artigo_list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        artigos = obter_lista_artigos_dto()

        return render(request, self.template_name, context={"artigos": artigos})


class ArtigoDetailView(View):
    template_name = "blog/artigo_detail.html"

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        try:
            artigo_dto = obter_artigo_dto_por_slug(slug)
        except Artigo.DoesNotExist:
            raise Http404("Artigo não encontrado")

        context = {"artigo": artigo_dto, "comentarios": artigo_dto.comentarios}

        return render(request, self.template_name, context)
