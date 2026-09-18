### HOME PAGE
## 1* barcha like bosilgan productlar
## 2* product nomi bo'yicha search qilish
## 3* mavsumiy chegirmalar, yani muddat tugamagan chegirmalarga ega mahsulotlarni tortib kelish
## 4* oxirgi hafta/oy ichida chegirmaga ega productlar
## 5* oxirgi hafta ichida eng ko'p qidiruvdagi va ratingi baland productlar
## 6* user oxirgi hafta ichida eng ko'p qidirgan va ratingi baland productlar
- 7* 


### notification page
## 1* bitda notification_id qayssi userlarga send qilingan
## 2* bitda user ga kelgan barcha notificationlar

### one product details
## 1* name, descriptions, price, current_quantity, size, 
# 2* shu categoryadagi productlar
# 3* agarda product uchun discount mavjud bo'lsa uni ham hisoblab current price ni hisobla
# 4* shu mahulotni o'rtacha rating va user tomonidan rating belgulash
# 5 store da shu productdan qancha borligini bilish
# 6* bucket ga qancha miqdordagi va qanday size dagi productlarni solib qo'yish


one product data => detail + avg rating + discount + in store 
this type products in category

#### Report
### register.py:
## "/register" API ni vazifasi
``` 
 1* Userni bazadan teshkiradi yo'q bo'lsa True ✔  oldin register qilingan bo'lsa Error(user alredy exist)
 2* Redisga %secred_kod, %user haqidagi data(json holatda), %is_active=fasle(chunki hali tasdiqlanmadi)
 3* 'send_email_message' funksiya-> regischi bo'lgan userga secred_kod yuboradi 
```
## "/verify/{secred_code}" API emailni tasdiqlaydi
```
 1* 'redis_url' dan redisga saqlangan datani get qilib oladi va decode qiladi
 2* user ni yana bir bor email orqali bazadan teshkiradi va dublikatlikga yo'l qo'ymaydi
 3* redisdan olingan datalar yordamida new_user yaratiladi va 'is_active=true' qilib qo'yiladi
 4* agar bazada hali user not exist bo'lsa first user is-> 'is_admin=true'
 ```







#### DONE
## 1* register/verify(email) + auth ✔ 
## 2* custom middleware (for check over) ✔
## 3*

### NEED
# 1* update_access_token for 