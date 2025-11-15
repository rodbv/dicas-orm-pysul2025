import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    nome = models.CharField(
        max_length=50, unique=True, blank=False, verbose_name="Nome"
    )
    slug = models.SlugField(
        max_length=50, unique=True, blank=False, verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Artigo(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(
        max_length=200, unique=True, blank=False, verbose_name="Slug"
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="artigos",
        verbose_name="Autor",
    )
    conteudo = RichTextField(verbose_name="Conteúdo")
    resumo = RichTextField(blank=True, verbose_name="Resumo", config_name="resumo")
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
    tags = models.ManyToManyField(
        Tag, related_name="artigos", blank=True, verbose_name="Tags"
    )

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"

    def __str__(self):
        return self.titulo

    def publicar(self):
        self.publicado = True
        self.data_publicacao = timezone.now()
        self.save()


class Comentario(models.Model):
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
    texto = RichTextField(verbose_name="Texto do Comentário")
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
