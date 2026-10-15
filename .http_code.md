### 2xx — Success (Muvaffaqiyatli)

# 200 OK: So'rov muvaffaqiyatli bajarildi.

# 201 Created: So me'moriy so'rov orqali yangi resurs muvaffaqiyatli yaratildi.

# 202 Accepted: So'rov qabul qilindi, lekin ishlov berish hali yakunlanmadi.

# 204 No Content: So'rov muvaffaqiyatli bajarildi, lekin qaytarish uchun javob tanasi (body) yo'q.

### 3xx — Redirection (Yuborish / Yo'naltirish)

# 301 Moved Permanently: So'ralgan resurs manzili butunlay boshqa URL'ga ko'chirilgan.

302 Found: Resurs vaqtincha boshqa URL'da joylashgan.

304 Not Modified: Resurs keshdan beri o'zgarmagan (mijoz keshdagi nusxadan foydalanishi mumkin).

### 4xx — Client Errors (Mijoz xatoliklari)

400 Bad Request: So me'moriy so'rov sintaksisi xato yoki noto'g'ri ma'lumot yuborilgan.

401 Unauthorized: Autentifikatsiya talab qilinadi (token yoki login/parol yo'q yoki xato).

403 Forbidden: Ruxsat yo'q (autentifikatsiya o'tilgan bo'lsa ham bu resursga kirish Taqiqlangan).

404 Not Found: So'ralgan resurs yoki endpoint topilmadi.

405 Method Not Allowed: Ishlatilgan HTTP metodi (GET, POST, PUT, DELETE va h.k.) ushbu endpoint uchun ruxsat etilmagan.

409 Conflict: So'rov baza holati bilan toqnashuv yaratdi (masalan, unikal email qayta kiritilganda).

422 Unprocessable Entity: Validation xatosi (so'rov strukturasi to'g'ri, lekin ma'lumot turi yoki qiymati noto'g'ri).

429 Too Many Requests: Belgilangan vaqt ichida juda ko'p so'rov yuborildi (Rate Limit cheklovi).

### 5xx — Server Errors (Server xatoliklari)

500 Internal Server Error: Serverda kutilmagan ichki xatolik yuz berdi (backend kodida unhandled exception).

502 Bad Gateway: Server proksi yoki shlyuz sifatida ishlayotganda yuqoridagi serverdan noto'g'ri javob oldi.

503 Service Unavailable: Server vaqtincha ishlamayapti (sozlash ishlari ketmoqda yoki yuklama juda yuqori).

504 Gateway Timeout: Server yuqoridagi backend servisdan belgilangan vaqt ichida javob ololmadi (timeout).