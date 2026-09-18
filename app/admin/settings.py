from starlette_admin.contrib.sqla import Admin
from app.database import engine
from app.model import User, Product, Shop, Wallet, Order
from app.admin.auth import JsonAuthProvider
from app.admin.views import UserAdminView
from app.config import settings

admin = Admin(
    engine,
    title="Market-place admin",
    base_url="/admin",
    secret_key=settings.SECRET_KEY,
    auth_provider=JsonAuthProvider(login_path="/login", logout_path="/logout"),
)

admin.add_view(UserAdminView(User, icon="fa fa-user"))
