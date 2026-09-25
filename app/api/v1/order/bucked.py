from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select, func
from sqlalchemy.orm import join
from app.database import db_dep
from app.model import (
    Bucket,
    Bucket_Product,
    Product,
)


