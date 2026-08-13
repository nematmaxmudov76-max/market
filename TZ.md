#### 1. USER (Foydalanuvchilar) uchun TODO vazifalar (10 ta)
##### Biznes modeli: Foydalanuvchilar xarid qiladi, sharh yozadi, manzillarini saqlaydi va kuryer bo'lib ishlashi mumkin.

# [Easy] Barcha faol (is_active = true) foydalanuvchilarning ismi, familiyasi va emailini chiqaring.

# [Easy] Ma'lum bir foydalanuvchi (masalan, id = 5) uchun uning barcha saqlangan manzillarini (user_address jadvalidan) chiqaring.

# [Medium] Oxirgi 7 kun ichida ro'yxatdan o'tgan (create_at) foydalanuvchilar sonini hisoblang.


# [High Level] "Admin" yoki "Staff" huquqiga ega (is_admin = true yoki is_staff = true) bo'lgan foydalanuvchilar ro'yxatini chiqaring.

# [High Level] Barcha kuryerlar (is_courier = true) ro'yxatini chiqaring va ularning courier_profile jadvalidagi transport vositalari (transport_type) va balanslarini (balance) qo'shib ko'rsating.

# [High Level] Foydalanuvchi (masalan, user_id = 50) jami nechta buyurtma berganini order jadvalidan hisoblang.

# [High Level] O'chirilgan (is_deleted = true) foydalanuvchilarning barcha eski xabarlarini (notification jadvalidan) o'chirib tashlash uchun SQL so'rovini yozing.

[High Level] Barcha foydalanuvchilar va ularning oxirgi tizimga kirish vaqtini (last_login) va o'rtacha buyurtma summasini hisoblaydigan statistik so'rov tayyorlang.

#### 2. SHOP (Do'konlar) uchun TODO vazifalar (15 ta)
##### Biznes modeli: Har bir do'kon o'z mahsulotlarini qo'shadi, medialarni yuklaydi, obunalar va reytingga ega.

# [Easy] Barcha faol (is_active = true) do'konlarning nomlari va ularning reytingini (rating) o'rtacha qiymat bo'yicha kamayish tartibida chiqaring.

# [Easy] Ma'lum bir do'konga tegishli (shop_id = 5) barcha mahsulotlarni (product) va ularning narxini chiqaring.

[Medium] shop jadvalidagi description maydoni bo'sh (NULL) bo'lgan do'konlarni toping va ularni yangilash uchun SQL so'rovini yozing (masalan, "Ma'lumot kiritilmagan" deb yozing).

# [Medium] Har bir do'konda qancha mahsulot borligini hisoblang (product jadvali bo'yicha shop_id guruhlab).

# [Medium] Qaysi do'kon o'z mahsulotlariga eng ko'p media (rasm/video) yuklagan? (product_media jadvalidan foydalanib statistikani chiqaring).

# [High Level] Reytingi 4.5 dan yuqori bo'lgan do'konlar ro'yxatini va ularning mahsulotlarining o'rtacha narxini chiqaring.

# [High Level] Oxirgi 1 oy ichida yangi ochilgan (create_at) do'konlar ro'yxatini chiqaring.

# [High Level] Do'kon egasini (user_id) do'kon ma'lumotlari bilan qo'shib ko'rsatadigan murakkab JOIN so'rovini yozing (shop + user).

[High Level] Do'konning banner_id bo'yicha media jadvalidan rasmni topib, keyin o'sha rasmni o'chirish (banner rasmini yangilash uchun) mantiqini yozing.

[High Level] Barcha do'konlarni ularning mahsulotlarining umumiy soni bo'yicha saralang (eng ko'p mahsulotdan eng kamiga).

# [High Level] shop va product jadvallarini birlashtirib, har bir do'kon uchun eng qimmat va eng arzon mahsulot narxini ko'rsating.

# [High Level] Do'kon o'chirilganda (is_active = false), ushbu do'konga tegishli barcha mahsulotlarni ham avtomatik o'chirish uchun SQL skript yoki Trigger yozish rejasini tuzing (biznes mantiq).

# [High Level] shop jadvalidagi ma'lumotlarni yangilashda update_at ustunini avtomatik yangilaydigan mexanizmni (Trigger) taklif qiling.

#### 3. PRODUCT & CATEGORY (Mahsulot va Kategoriyalar) uchun TODO vazifalar (10 ta)
##### Biznes modeli: Mahsulotlar kategoriyalarga bo'linadi, zaxirada bo'ladi, chegirmalar va likelar (sevimlilar) mavjud.

# [Easy] Barcha faol (is_active = true) mahsulotlarning nomi va narxini list qiling.

# [Easy] Ma'lum bir kategoriyaga (category_id = 3) tegishli barcha mahsulotlarni chiqaring.
 
# [Medium] Sotuvda mavjud bo'lgan (joriy zaxirasi current_quantity > 0) mahsulotlar sonini hisoblang.

# [Medium] Umumiy kategoriyalar (category jadvalidan) ro'yxatini va ular nechta mahsulotga ega ekanligini ko'rsating.

[High Level] Mahsulotga qo'yilgan barcha Like va Comment (sharhlar) sonini birgalikda ko'rsating (like va comment jadvallarini birlashtirib).

[High Level] "Bu mahsulotni kimlar yoqtirgan?" degan savolga javob berish uchun user va like jadvallarini birlashtirib, userlarning ismi va familiyasini chiqaring.

[High Level] Muddati o'tgan mahsulotlarni (expiration_date < CURRENT_DATE) toping va ularni muddatli (expired) deb belgilang (UPDATE so'rovi).

[High Level] Chegirmadagi (promo_code orqali) mahsulotlarni aniqlash va ularning chegirmadagi yangi narxini hisoblab chiqadigan murakkab so'rov yozing.

[High Level] Mahsulot tavsifi (description) da ma'lum bir kalit so'z (masalan, "iPhone") qatnashgan mahsulotlarni qidiring va ularni mashhurlik bo'yicha (like soni bo'yicha) saralang.

#### 4. ORDER & PAYMENT & WALLET (Buyurtma, To'lov va Hamyon) uchun TODO vazifalar (10 ta)
##### Biznes modeli: Foydalanuvchi buyurtma beradi, buyurtma mahsulotlari (order_item), to'lov amalga oshadi, hamyon va tranzaksiyalar qayd etiladi.

[Easy] Barcha tugallangan (status jadvalidagi status_method bo'yicha) buyurtmalarni va ularning umumiy summasini (total_amount) chiqaring.

[Easy] Bitta buyurtma (masalan, order_id = 101) ichida qancha va qanday mahsulotlar borligini order_item jadvalidan ko'rsating.

[Medium] Ma'lum bir foydalanuvchining (user_id = 25) hamyon (wallet) balansini va valyutasini (currency) chiqaring.

[Medium] Eng ko'p pul sarflagan eng yaxshi 3 ta mijozni order jadvalidagi total_amount bo'yicha saralab toping.

[Medium] To'lov jarayonida (payment_process) status qiymati "failed" (muvaffaqiyatsiz) bo'lgan barcha urinishlarni va ularning sababini (transaction_param maydonidan) chiqaring.

[High Level] Har bir buyurtma uchun to'lov jarayonini (summa, status, sana) va buyurtma holatini (order jadvalidagi status_id) birgalikda ko'rsatadigan JOIN so'rovini yozing.

[High Level] Foydalanuvchi hamyonini to'ldirish yoki sarflash vaqtida transactions_log jadvaliga yozuv kiritadigan (INSERT) mantiqni yozing.

[High Level] Kuryer tomonidan yetkazib berilgan (delivery_process jadvalidagi courier_id orqali) buyurtmalar ro'yxatini va ularning kuryer ismi bilan birga chiqaring.

[High Level] Har bir foydalanuvchining hamyon balansi va to'lanmagan buyurtmalari yig'indisini solishtirib, balansi yetarli bo'lmagan foydalanuvchilarni aniqlang.

[High Level] O'tgan oy davomida to'lovlar (payment_process) yig'indisi bo'yicha eng ko'p daromad keltirgan do'konlarni (shop jadvalidan) aniqlang.

Qo'shimcha Business Level Masalalar (Bonus)
Bu erda oddiy SQL emas, balki biznes qoidalar (Business Logic) bo'yicha vazifalar:

Chegirma mantiqi: promo_code jadvalidagi discount_amount ni order jadvalidagi total_amount ga qanday qo'llash kerak? (API logikasi yozing).

Yetkazib berish: delivery_process jadvalidagi status o'zgarganda (masalan, "delivered"), order jadvalidagi status_id ni avtomatik ravishda "Yakunlandi" ga o'zgartirish mantiqi.

Buyurtma tarkibi: Foydalanuvchi savatga (bucket) mahsulot qo'shganda bucket_product jadvaliga yozuv qo'shish. Ammo, agar mahsulot zaxirada (current_quantity) qolmagan bo'lsa, xatolik (Error) qaytarish mantiqi.

O'chirish kaskadi: Agar kategoriya (category) o'chirilsa, unga tegishli barcha mahsulotlar ham o'chirilsinmi yoki kategoriya NULL ga o'zgartirilsinmi? Bu biznes qarorini asoslab bering.