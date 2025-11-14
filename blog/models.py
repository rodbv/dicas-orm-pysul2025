import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Artigo(models.Model):
    """
    Modelo que representa um artigo do blog.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="artigos",
        verbose_name="Autor",
    )
    conteudo = models.TextField(verbose_name="Conteúdo")
    resumo = models.CharField(max_length=300, blank=True, verbose_name="Resumo")
    publicado = models.BooleanField(
        default=False, verbose_name="Publicado", db_index=True
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_publicacao = models.DateTimeField(
        null=True, blank=True, verbose_name="Data de Publicação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ["-data_publicacao", "-data_criacao"]

    def __str__(self):
        return self.titulo

    def publicar(self):
        """Marca o artigo como publicado e define a data de publicação."""
        self.publicado = True
        self.data_publicacao = timezone.now()
        self.save()


class Comentario(models.Model):
    """
    Modelo que representa um comentário em um artigo.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    artigo = models.ForeignKey(
        Artigo,
        on_delete=models.CASCADE,
        related_name="comentarios",
        verbose_name="Artigo",
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comentarios",
        verbose_name="Autor",
    )
    texto = models.TextField(verbose_name="Texto do Comentário")
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    aprovado = models.BooleanField(
        default=False, verbose_name="Aprovado", db_index=True
    )

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.artigo.titulo}"
