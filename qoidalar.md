### 1 GET Requestda body qatnashmaydi yani pydantik ishlatilmayd faqat POST PUT PATCH da ishlatiladi, va body nimadir berish uchun jo'natish uchun ishlatiladi!!!       
## faqat body bilan data base ni `manage` qilish uchun ishlatiladi, yani siz get qilib olaman deb ham data base ga o'zgartirish kirita olmaysiz bir vaqtda!!!!!

### Annotated -> metadatalarni biriktirish uchun ishlatiladi

### 401 -> san kimsan
### 403 -> sani buni qilishga huquqing yo'q

### Mana shu sozlama ORM obyektini(user.post, user.email) Json formatga o'girib beradi(user["post"], user["email"])
`model_config = ConfigDict(from_attributes=True`


# select(Post) -> scalars()
# select(Post.title, Post.slug) -> mappings()
## QULAYLIGI: .mappings() ma'lumotni to'g'ridan-to'g'ri kalit-qiymat ({"id": 1, "title": "..."}) ko'rinishida bergani uchun Pydantic modellariga (response_model) uzatish o'ta tez va kam xotira sarflaydi.
### ASOSIY MAQSADI: Faqat ma'lumot o'qish (Read-only API), ro'yxat ko'rsatish va shu sababli scalars() ga qaraganda juda tez va minimal RAM sarflaydi 
## NIMALAR BILAN ISHLATISH QULAY: aqat tekis (Flat) ma'lumot va yuqori tezlik kerak bo'lsa:

# select(Post.id, User.username).outerjoin(...) qilib, .mappings() ishlating. (Eng tez usul).

## Ichma-ich (Nested) munosabatlar va struktura kerak bo'lsa:

# select(Post).options(selectinload(Post.author)) qilib, .scalars() bilan oling va Pydantic orqali serialized qiling.

## joinedload/selectinload bilan .mappings() ishlatish texnik jihatdan xato bermaydi, lekin xotira tejamkorligi nuqtai nazaridan mantiqsiz.

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