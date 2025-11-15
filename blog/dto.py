from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class AutorDTO:
    username: str
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


@dataclass
class TagDTO:
    nome: str


@dataclass
class ComentarioDTO:
    texto: str
    data_criacao: datetime
    autor: AutorDTO


@dataclass
class ArtigoDetailDTO:
    titulo: str
    conteudo: str
    data_publicacao: datetime | None
    autor: AutorDTO
    tags: List[TagDTO]
    comentarios: List[ComentarioDTO]


@dataclass
class ArtigoListDTO:
    titulo: str
    slug: str
    resumo: str
    data_publicacao: datetime | None
    data_criacao: datetime
    autor: AutorDTO
    tags: List[TagDTO]

    @property
    def data_exibicao(self) -> datetime:
        return self.data_publicacao or self.data_criacao
