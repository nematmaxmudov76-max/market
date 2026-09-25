### 1 GET Requestda body qatnashmaydi yani pydantik ishlatilmayd faqat POST PUT PATCH da ishlatiladi, va body nimadir berish uchun jo'natish uchun ishlatiladi!!!       
## faqat body bilan data base ni `manage` qilish uchun ishlatiladi, yani siz get qilib olaman deb ham data base ga o'zgartirish kirita olmaysiz bir vaqtda!!!!!

### 2* Annotated -> metadatalarni biriktirish uchun ishlatiladi

### 3* 401 -> san kimsan
###    403 -> sani buni qilishga huquqing yo'q

### 4* Mana shu sozlama ORM obyektini(user.post, user.email) Json formatga o'girib beradi(user["post"], user["email"])
`model_config = ConfigDict(from_attributes=True`


# 5* select(Post) -> scalars()
#    select(Post.title, Post.slug) -> mappings()
## !! QULAYLIGI: `.mappings()` ma'lumotni to'g'ridan-to'g'ri kalit-qiymat ({"id": 1, "title": "..."}) ko'rinishida bergani uchun Pydantic modellariga (response_model) uzatish o'ta tez va kam xotira sarflaydi.
### ASOSIY MAQSADI: Faqat ma'lumot o'qish (Read-only API), ro'yxat ko'rsatish va shu sababli scalars() ga qaraganda juda tez va minimal RAM sarflaydi 
## NIMALAR BILAN ISHLATISH QULAY: aqat tekis (Flat) ma'lumot va yuqori tezlik kerak bo'lsa:



## 6* Ichma-ich (Nested) munosabatlar va struktura kerak bo'lsa:
# select(Post).options(selectinload(Post.author)) qilib, .scalars() bilan oling va Pydantic orqali serialized qiling.

## 7* joinedload/selectinload bilan `.mappings()` ishlatish texnik jihatdan xato bermaydi, lekin xotira tejamkorligi nuqtai nazaridan mantiqsiz.

```
from sqlalchemy import select

# SQL darajasida join qilib, aniq ustunlarni tanlaymiz
stmt = (
    select(
        Post.id,
        Post.title,
        User.username.label("author_name")  # Ustunga alias berish qulay
    )
    .outerjoin(User, Post.author_id == User.id)
)

result = await session.execute(stmt)
posts = result.mappings().all()

# Natija: [{'id': 1, 'title': 'First Post', 'author_name': 'Nemat'}, ...]
```


### 8* @limiter.limit("10/minute")
### asyc def get(request:Request, ...)
## limiter funksiyasini ishlatganda albatda har bir so'rovda `Request` parametr(argument) sifatida qo'shib qo'yish kerak 

### 9* get/set  vs getattr/setattr
## Lug'atdan (dict) xavfsiz o'qish	`.get(key, default)`	exp:`request.cookies.get("access_token")`
## Obyekt atributidan xavfsiz o'qish	`getattr(obj, "attr", default)`	exp:`getattr(user, "is_admin", False)`
## Obyekt atributiga dinamik yozish	`setattr(obj, "attr", value)`	exp:`setattr(request.state, "user", db_user)`
## DB'dan primary key bo'yicha tez qidirish	`session.get(Model, pk)`	exp:`db.get(User, 1)`


### 9* Bitda tableda ikki column ham PK orqali bitda columnga ulansa:
```
user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False
    )
reviewed_by: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )




user: Mapped["User"] = relationship(
    "User",
    foreign_keys=[user_id],
    back_populates="role_request_user",
    lazy="raise_on_sql",
)
reviewer: Mapped["User"] = relationship(
    "User",
    foreign_keys=[reviewed_by],
    back_populates="reviewed_by_admin",
    lazy="raise_on_sql",
)
```


### 10* OLDINDAN KELISHUVLAR!!!!
## request.state.user_login => login qilingan userlar fazasi (diapazoni)
## request.state.user => login qilinmagan!!! lekin => is_active = True bo'lgan userlar fazasi!!