from typing import Any
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin import IntegerField
from app.utils import hash_password


class UserAdminView(ModelView):
    fields = [
        "id",
        "email",
        "first_name",
        "last_name",
        "age",
        "bio",
        "tell_number",
        "password_hash",
        "last_login",
        "is_active",
        "is_deleted",
        "is_manager",
        "is_admin",
        "is_merchant",
        "is_courier",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list = [
        "password_hash",
        "bio",
        "last_login",
        "is_deleted",
    ]
    exclude_fields_from_create = [
        "id",
        "created_at",
        "updated_at",
        "last_login",
    ]
    exclude_fields_from_edit = [
        "id",
        "password_hash",
        "updated_at",
        "created_at",
        "last_login",
    ]

    async def before_create(self, request: Request, data: dict[str, Any]) -> None:
        if "password_hash" in data and data["password_hash"]:
            data["password_hash"] = hash_password(data["password_hash"])

    async def before_edit(self, request: Request, data: dict[str, Any], obj: Any) -> None:
        if "password_hash" in data and data["password_hash"]:
            data["password_hash"] = hash_password(data["password_hash"])
        elif "password_hash" in data:
            del data["password_hash"]
    # faqat admin va manager lar barcha userlarni ko'rish mumink
    async def is_accessible(self, request):
        user = getattr(request.state, "user", None)
        return bool(user and getattr(user, "is_admin", False) or getattr(user, "is_manager", False))

class NotificationAdminView(ModelView):
    icon = "fa fa-bell"
    fields = [
        "title",
        "type",
        "message",
        "target_role",
    ]

    async def is_accessible(self, request):
        user = getattr(request.state, "user", None)
        return bool(user and getattr(user, "is_admin", False) or getattr(user, "is_manager", False))

class RoleRequestView(ModelView):
    key = "role_request"
    name = "Role Request"
    label = "Role Requests"
    icon = "fa fa-id-card"
    fields = [
        "user_id",
        "request_role",
        "application",
        "resume_url",
        "checking_status",
        "reviewed_by",
        "reviewed_at",
        "status_expired_at",
        "attempt_count",
        "hash_code",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list = [
        "reviewed_by",
        "status_expired_at",
        "hash_code",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_create = [
        "id",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_edit = [
        "user_id",
        "hash_code",
        "created_at",
    ]

    async def is_accessible(self, request):
        user = getattr(request.state, "user", None)
        return bool(user and getattr(user, "is_admin", False) or getattr(user, "is_manager", False))
