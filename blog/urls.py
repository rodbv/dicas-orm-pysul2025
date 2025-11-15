from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.ArtigoListView.as_view(), name="artigo_list"),
    path("<slug:slug>/", views.ArtigoDetailView.as_view(), name="artigo_detail"),
]
