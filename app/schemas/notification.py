from .base import Base


class NotifListResponse(Base):
    title: str
    type: str
    message: str


class NotifCreateResponse(Base):
    title: str
    type: str
    message: str


class NotifUpdateRequest(Base):
    title: str
    type: str
    message: str
