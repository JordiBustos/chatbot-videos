from typing import TypedDict, Tuple, Union
from qdrant_client import QdrantClient
from enum import Enum


class QdrantError(TypedDict):
    e: Tuple[dict, int]
    ve: Tuple[dict, int]
    nre: Tuple[dict, int]


QdrantConnection = Tuple[Union[QdrantClient, tuple], bool]


Response = Tuple[dict, int]


class FaqDict(TypedDict):
    id: str
    question: str
    answer: str
    category: str
    courses_id: list


class FaqCategory(Enum):
    TECH = "tech"
    ADMIN = "admin"
