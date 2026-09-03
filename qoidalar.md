### 1 GET Requestda body qatnashmaydi yani pydantik ishlatilmayd faqat POST PUT PATCH da ishlatiladi, va body nimadir berish uchun jo'natish uchun ishlatiladi!!!       
## faqat body bilan data base ni `manage` qilish uchun ishlatiladi, yani siz get qilib olaman deb ham data base ga o'zgartirish kirita olmaysiz bir vaqtda!!!!!

### Annotated -> metadatalarni biriktirish uchun ishlatiladi

### 401 -> san kimsan
### 403 -> sani buni qilishga huquqing yo'q

### Mana shu sozlama ORM obyektini(user.post, user.email) Json formatga o'girib beradi(user["post"], user["email"])
`model_config = ConfigDict(from_attributes=True`
