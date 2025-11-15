import re

from django.contrib import admin

from .models import Artigo, Comentario, Tag


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ["autor", "preview_texto", "aprovado", "data_criacao"]
    readonly_fields = ["data_criacao", "preview_texto"]
    show_change_link = True
    can_delete = True
    verbose_name = "Comentário"
    verbose_name_plural = "Comentários"

    def preview_texto(self, obj):
        if obj.pk and obj.texto:
            # Remove tags HTML para preview
            texto_limpo = re.sub(r"<[^>]+>", "", str(obj.texto))
            return texto_limpo[:100] + "..." if len(texto_limpo) > 100 else texto_limpo
        return "-"

    preview_texto.short_description = "Texto"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-data_criacao")


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("blog/css/ckeditor-width.css",),
        }

    list_display = [
        "titulo",
        "autor",
        "mostrar_tags",
        "publicado",
        "data_criacao",
        "data_publicacao",
    ]
    list_filter = ["publicado", "data_criacao", "data_publicacao", "autor", "tags"]
    search_fields = ["titulo", "conteudo", "resumo", "tags__nome"]
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ["id", "data_criacao", "data_atualizacao"]
    date_hierarchy = "data_publicacao"
    list_editable = ["publicado"]
    inlines = [ComentarioInline]

    def mostrar_tags(self, obj):
        tags = obj.tags.all()
        if tags:
            return ", ".join([tag.nome for tag in tags])
        return "-"

    mostrar_tags.short_description = "Tags"
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "titulo",
                    "slug",
                    "autor",
                    "tags",
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
    class Media:
        css = {
            "all": ("blog/css/ckeditor-width.css",),
        }

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
        if obj.texto:
            return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
        return "-"

    preview_texto.short_description = "Prévia do Texto"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["nome", "slug"]
    search_fields = ["nome"]
    prepopulated_fields = {"slug": ("nome",)}
    readonly_fields = ["id"]
