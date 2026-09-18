from fastapi import APIRouter, UploadFile, HTTPException
from app.database import db_dep
from app.model import Media
from app.config import settings
import shutil
from pathlib import Path


router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: db_dep):
    if file.size > settings.FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File size is too large. Max size is 5MB."
        )

    file_ext = Path(file.filename).suffix.lower()  # image.png
    if file_ext not in settings.FILE_TYPE:
        raise HTTPException(
            status_code=400,
            detail="File type is not supported. Only .jpg, .png, .jpeg are allowed.",
        )
    path = Path(settings.MEDIA_PATH)
    path.mkdir(exist_ok=True)
    res = path / file.filename  # chesnokuz/media/filename.jpg
    with open(res, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Media(url=f"{settings.MEDIA_PATH}/{file.filename}")
    db.add(image)
    db.commit()
    db.refresh(image)

    return {"media_id": image.id, "url": f"{settings.BASE_URL}/{image.url}"}
