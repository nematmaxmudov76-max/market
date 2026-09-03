from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.database import db_dep
from app.model import Region, Country
from app.schemas import (
    RegionListResponse,
    RegionCreateRequest,
    CountryCreateRequest,
    CountryListResponse,
    CountryUpdateRequest,
)

router = APIRouter(prefix="/location", tags=["Location"])

# CRUD


@router.get("/get-region/{region_id}", response_model=RegionListResponse)
async def get_region(session: db_dep, region_id: int):
    stmt = (
        select(Region).where(Region.id == region_id).options(joinedload(Region.country))
    )
    res = (session.execute(stmt)).scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="region not found")

    return res


@router.post("/create-region")
async def create_region(session: db_dep, data: RegionCreateRequest):
    region = Region(name=data.name, country_id=data.country_id)
    session.add(region)
    session.commit()
    session.refresh(region)

    return region


@router.post("/create-country", response_model=CountryListResponse)
async def create_country(session: db_dep, data: CountryCreateRequest):
    res = Country(name=data.name)
    session.add(res)
    session.commit()
    session.refresh(res)

    return res


@router.patch("/update-country", response_model=CountryListResponse)
async def update_country(session: db_dep, country_id: int, data: CountryUpdateRequest):
    stmt = session.get(Country, country_id)
    if not stmt:
        raise HTTPException(status_code=404, detail="country not found")
    stmt.name = data.name
    session.commit()
    session.refresh(stmt)
    return stmt


@router.delete("/delete-country/{country_id}", status_code=204)
async def delete_country(session: db_dep, country_id: int):
    stmt = select(Country).where(Country.id == country_id)
    res = (session.execute(stmt)).scalar_one_or_none()

    if res is None:
        raise HTTPException(status_code=404, detail="country not found")
    session.delete(res)
    session.commit()
