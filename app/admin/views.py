from starlette_admin.contrib.sqla import ModelView
from starlette_admin import IntegerField

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
        "password_pash",
        "updated_at",
        "created_at",
        "last_login",
    ]


class NotificationAdminView(ModelView):
    fields = [
        "title",
        "type",
        "message",
    ]

