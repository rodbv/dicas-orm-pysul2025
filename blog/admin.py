from django.contrib import admin

from .models import Artigo, Comentario


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Artigo."""

    list_display = [
        "titulo",
        "autor",
        "publicado",
        "data_criacao",
        "data_publicacao",
    ]
    list_filter = ["publicado", "data_criacao", "data_publicacao", "autor"]
    search_fields = ["titulo", "conteudo", "resumo"]
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ["id", "data_criacao", "data_atualizacao"]
    date_hierarchy = "data_publicacao"
    list_editable = ["publicado"]
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "titulo",
                    "slug",
                    "autor",
                    "publicado",
                ),
            },
        ),
        (
            "Conteúdo",
            {
                "fields": (
                    "resumo",
                    "conteudo",
                ),
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "data_criacao",
                    "data_publicacao",
                    "data_atualizacao",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Informações Técnicas",
            {
                "fields": ("id",),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Comentario."""

    list_display = [
        "artigo",
        "autor",
        "aprovado",
        "data_criacao",
        "preview_texto",
    ]
    list_filter = ["aprovado", "data_criacao", "artigo"]
    search_fields = ["texto", "autor__username", "artigo__titulo"]
    readonly_fields = ["id", "data_criacao"]
    date_hierarchy = "data_criacao"
    list_editable = ["aprovado"]
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "artigo",
                    "autor",
                    "aprovado",
                ),
            },
        ),
        (
            "Conteúdo",
            {
                "fields": ("texto",),
            },
        ),
        (
            "Datas",
            {
                "fields": ("data_criacao",),
                "classes": ("collapse",),
            },
        ),
        (
            "Informações Técnicas",
            {
                "fields": ("id",),
                "classes": ("collapse",),
            },
        ),
    )

    def preview_texto(self, obj):
        """Retorna uma prévia do texto do comentário."""
        if obj.texto:
            return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
        return "-"

    preview_texto.short_description = "Prévia do Texto"
