from __future__ import annotations
from .base import Base


class RegionListResponse(Base):
    id: int
    name: str
    country: CountryListResponse


class RegionCreateRequest(Base):
    name: str
    country_id: int


# COUNTRY __________________________
class CountryCreateRequest(Base):
    name: str


class CountryListResponse(Base):
    id: int
    name: str


class CountryUpdateRequest(Base):
    name: str
