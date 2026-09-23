from typing import Any
from starlette.requests import Request
from app.model import User, Notification
from app.database import db_dep
from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView
from app.database import SessionLocal

class ManageNotificationAdmin(ModelView):

    async def send_message(self, request:Request, )
