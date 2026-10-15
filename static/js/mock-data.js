/**
 * Market Frontend Mock Data & Backend Schemas
 * 
 * Ushbu fayldagi barcha ma'lumotlar kelajakda backend API dan keladigan
 * ma'lumotlar strukturasiga to'liq moslashtirilgan.
 * Har bir ma'lumot bloki qaysi backend endpointidan kelishi ko'rsatilgan.
 */

const MOCK_DATA = {
  // BACKEND: GET /api/v1/auth/me yoki /api/v1/user/profile
  currentUser: {
    id: 5,
    firstName: "Olimjon",
    lastName: "Karimov",
    phone: "+998 90 123 45 67",
    email: "olimjon.karimov@example.uz",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80",
    balance: 1450000, // so'm
    currency: "UZS",
    role: "buyer", // "buyer" | "courier" | "merchant" | "admin"
    isCourier: true, // Kuryer bo'limi bilan integratsiya uchun
    addresses: [
      { id: 1, title: "Uyim", fullAddress: "Toshkent sh., Chilonzor tumani, 9-mavze, 14-uy, 28-xonadon", isDefault: true },
      { id: 2, title: "Ishxona", fullAddress: "Toshkent sh., Yakkasaroy tumani, Shota Rustaveli ko'chasi, 45-uy", isDefault: false }
    ],
    courierProfile: {
      id: 102,
      fullName: "Olimjon Karimov",
      vehicleType: "Skuter (Elektromoped)", // Piyoda | Velosiped | Skuter | Avtomobil
      status: "online", // "online" | "busy" | "offline"
      currentBalance: 820000,
      todayEarnings: 240000,
      completedToday: 8,
      rating: 4.95
    }
  },

  // BACKEND: GET /api/v1/product/categories
  categories: [
    { id: 1, name: "Elektronika", slug: "elektronika", icon: "laptop", count: 1240 },
    { id: 2, name: "Maishiy texnika", slug: "maishiy-texnika", icon: "plug", count: 860 },
    { id: 3, name: "Kiyim-kechak", slug: "kiyim-kechak", icon: "shirt", count: 2150 },
    { id: 4, name: "Poyabzallar", slug: "poyabzallar", icon: "shoe-prints", count: 940 },
    { id: 5, name: "Go'zallik va parvarish", slug: "gozallik", icon: "sparkles", count: 1100 },
    { id: 6, name: "Smartfonlar va gadjetlar", slug: "smartfonlar", icon: "mobile-screen-button", count: 720 },
    { id: 7, name: "Sport va hordiq", slug: "sport", icon: "volleyball", count: 530 },
    { id: 8, name: "Avtotovarlar", slug: "avtotovarlar", icon: "car", count: 680 }
  ],

  // BACKEND: GET /api/v1/product/seasonal/ (Mavsumiy chegirmalar)
  seasonalProducts: [
    {
      id: 101,
      title: "Xiaomi Redmi Note 13 Pro 8/256GB Midnight Black",
      category: "smartfonlar",
      categoryName: "Smartfonlar va gadjetlar",
      currentPrice: 3299000,
      oldPrice: 4100000,
      discountPercent: 20,
      installmentPrice: "349 000 so'm/oy",
      rating: 4.9,
      reviewsCount: 142,
      stockCount: 18,
      inOtherBaskets: 47,
      shopName: "Xiaomi Official Store",
      images: [
        "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Super AMOLED 120Hz ekran, 200MP kamera va 67W tezkor quvvatlash. 1 yil rasmiy kafolat bilan taqdim etiladi."
    },
    {
      id: 102,
      title: "Apple AirPods Pro 2 MagSafe Case (USB-C)",
      category: "elektronika",
      categoryName: "Elektronika",
      currentPrice: 2850000,
      oldPrice: 3400000,
      discountPercent: 16,
      installmentPrice: "299 000 so'm/oy",
      rating: 4.95,
      reviewsCount: 320,
      stockCount: 8,
      inOtherBaskets: 85,
      shopName: "iStore Tashkent",
      images: [
        "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1572536147248-ac59a8abfa4b?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: true,
      quantityInCart: 1,
      description: "Faol shovqinni bekor qilish (ANC), shaffoflik rejimi va moslashuvchan fazoviy audio texnologiyasi."
    },
    {
      id: 103,
      title: "Erkaklar issiq kurtkasi, suv o'tkazmaydigan qishki",
      category: "kiyim-kechak",
      categoryName: "Kiyim-kechak",
      currentPrice: 580000,
      oldPrice: 890000,
      discountPercent: 35,
      installmentPrice: "62 000 so'm/oy",
      rating: 4.7,
      reviewsCount: 89,
      stockCount: 12,
      inOtherBaskets: 23,
      shopName: "Nordic Wear",
      images: [
        "https://images.unsplash.com/photo-1544923246-77307dd654cb?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Mavsumiy sovuq va yomg'irli ob-havo uchun mukammal himoya, yuqori sifatli eko-paxta va termo astar."
    },
    {
      id: 104,
      title: "Aqlli havo namlagich va tozalagich Smart Mist 4L",
      category: "maishiy-texnika",
      categoryName: "Maishiy texnika",
      currentPrice: 340000,
      oldPrice: 480000,
      discountPercent: 29,
      installmentPrice: "37 000 so'm/oy",
      rating: 4.8,
      reviewsCount: 64,
      stockCount: 5,
      inOtherBaskets: 19,
      shopName: "EcoHome Tech",
      images: [
        "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "4 litrli hajm, tungi rejim, past shovqin va xona namligini avtomatik ushlab turish sensori."
    }
  ],

  // BACKEND: GET /api/v1/product/weekly/ (Haftalik chegirmalar)
  weeklyProducts: [
    {
      id: 201,
      title: "Samsung 55' UHD 4K Smart TV Crystal Processor",
      category: "elektronika",
      categoryName: "Elektronika",
      currentPrice: 5990000,
      oldPrice: 7200000,
      discountPercent: 17,
      installmentPrice: "630 000 so'm/oy",
      rating: 4.88,
      reviewsCount: 110,
      stockCount: 7,
      inOtherBaskets: 34,
      shopName: "Samsung Brand Store",
      images: [
        "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1461151304267-38535e780c79?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Kristal tiniqligidagi 4K tasvir, ingichka ramka va Tizen OS orqali barcha ilovalarni oson ishlatish."
    },
    {
      id: 202,
      title: "DeLonghi avtomatik espresso qahva mashinasi",
      category: "maishiy-texnika",
      categoryName: "Maishiy texnika",
      currentPrice: 4200000,
      oldPrice: 5600000,
      discountPercent: 25,
      installmentPrice: "445 000 so'm/oy",
      rating: 4.92,
      reviewsCount: 95,
      stockCount: 4,
      inOtherBaskets: 52,
      shopName: "Barista Pro",
      images: [
        "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1520970014086-2208d157c9e2?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: true,
      quantityInCart: 0,
      description: "Bitta tugma orqali kapuchino va espresso tayyorlash. O'rnatilgan maydalagich va sut ko'pirtirgich."
    },
    {
      id: 203,
      title: "Erkaklar charm krossovkasi, qulay shahar uslubi",
      category: "poyabzallar",
      categoryName: "Poyabzallar",
      currentPrice: 420000,
      oldPrice: 650000,
      discountPercent: 35,
      installmentPrice: "45 000 so'm/oy",
      rating: 4.65,
      reviewsCount: 78,
      stockCount: 16,
      inOtherBaskets: 30,
      shopName: "Urban Step",
      images: [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Tabiiy charmdan tayyorlangan, nafas oluvchi ortopedik taglik va yengil shahar qadamlari uchun."
    },
    {
      id: 204,
      title: "Smart Soat Amazfit GTR 4 Black Leather Band",
      category: "smartfonlar",
      categoryName: "Smartfonlar va gadjetlar",
      currentPrice: 1980000,
      oldPrice: 2450000,
      discountPercent: 19,
      installmentPrice: "210 000 so'm/oy",
      rating: 4.82,
      reviewsCount: 156,
      stockCount: 11,
      inOtherBaskets: 41,
      shopName: "Gadget Hub",
      images: [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "14 kungacha batareya quvvati, 150+ sport rejimlari, yurak urishi va qon bosimi nazorati."
    }
  ],

  // BACKEND: GET /api/v1/product/list?page=1&limit=8 (Asosiy mahsulotlar / Landing)
  landingProducts: [
    {
      id: 301,
      title: "Sony PlayStation 5 Slim 1TB Digital Edition",
      category: "elektronika",
      categoryName: "Elektronika",
      currentPrice: 6490000,
      oldPrice: 7500000,
      discountPercent: 13,
      installmentPrice: "680 000 so'm/oy",
      rating: 4.98,
      reviewsCount: 230,
      stockCount: 6,
      inOtherBaskets: 92,
      shopName: "PlayStore UZ",
      images: [
        "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Next-gen o'yinlar, 120 FPS, ultra-tezkor SSD va DualSense haptik boshqaruv pulti bilan."
    },
    {
      id: 302,
      title: "Dyson V15 Detect Simsiz changyutgich Fluffy",
      category: "maishiy-texnika",
      categoryName: "Maishiy texnika",
      currentPrice: 8900000,
      oldPrice: 10500000,
      discountPercent: 15,
      installmentPrice: "940 000 so'm/oy",
      rating: 4.96,
      reviewsCount: 84,
      stockCount: 3,
      inOtherBaskets: 38,
      shopName: "Dyson Uzbekistan",
      images: [
        "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: true,
      quantityInCart: 0,
      description: "Lazer nuri yordamida ko'rinmas changlarni aniqlash, 60 daqiqalik quvvat va yuqori so'rish quvvati."
    },
    {
      id: 303,
      title: "Erkaklar klassik qora kostyum-shimi (Slim Fit)",
      category: "kiyim-kechak",
      categoryName: "Kiyim-kechak",
      currentPrice: 1250000,
      oldPrice: 1800000,
      discountPercent: 30,
      installmentPrice: "135 000 so'm/oy",
      rating: 4.75,
      reviewsCount: 42,
      stockCount: 15,
      inOtherBaskets: 18,
      shopName: "Gentleman Style",
      images: [
        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Italiya matosidan tayyorlangan zamonaviy qora kostyum, to'y va rasmiy marosimlar uchun."
    },
    {
      id: 304,
      title: "Nike Air Max 270 Black & White Originals",
      category: "poyabzallar",
      categoryName: "Poyabzallar",
      currentPrice: 1450000,
      oldPrice: 1900000,
      discountPercent: 23,
      installmentPrice: "155 000 so'm/oy",
      rating: 4.89,
      reviewsCount: 178,
      stockCount: 9,
      inOtherBaskets: 67,
      shopName: "Nike Sportswear",
      images: [
        "https://images.unsplash.com/photo-1514989940743-4ba01bc0b512?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: true,
      quantityInCart: 0,
      description: "Air Max xavfli yostiqchasi kun bo'yi qulay yurish va amortizatsiyani ta'minlaydi."
    },
    {
      id: 305,
      title: "Keramika choy to'plami 12 kishilik Premium Gold",
      category: "uy-rozgor",
      categoryName: "Uy-ro'zg'or buyumlari",
      currentPrice: 490000,
      oldPrice: 650000,
      discountPercent: 24,
      installmentPrice: "52 000 so'm/oy",
      rating: 4.8,
      reviewsCount: 56,
      stockCount: 14,
      inOtherBaskets: 21,
      shopName: "Chini Uyi",
      images: [
        "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Zarhallangan nafis sharqona naqshlar, sifatli chinni va mustahkam sirlangan qoplama."
    },
    {
      id: 306,
      title: "Parfyum Chanel Bleu de Chanel Eau de Parfum 100ml",
      category: "gozallik",
      categoryName: "Go'zallik va parvarish",
      currentPrice: 1850000,
      oldPrice: 2200000,
      discountPercent: 15,
      installmentPrice: "195 000 so'm/oy",
      rating: 4.97,
      reviewsCount: 204,
      stockCount: 10,
      inOtherBaskets: 73,
      shopName: "Parfum Gallery",
      images: [
        "https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "Erkaklar uchun xushbo'y, sitrus va daraxt iforlari uyg'unlashgan xushbo'y hid."
    },
    {
      id: 307,
      title: "MacBook Air 13' M2 8/256GB Space Gray",
      category: "elektronika",
      categoryName: "Elektronika",
      currentPrice: 11900000,
      oldPrice: 13500000,
      discountPercent: 11,
      installmentPrice: "1 250 000 so'm/oy",
      rating: 4.99,
      reviewsCount: 312,
      stockCount: 5,
      inOtherBaskets: 110,
      shopName: "Apple Authorised",
      images: [
        "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: true,
      quantityInCart: 0,
      description: "Apple M2 chipi, 18 soatgacha avtonom ishlash, Liquid Retina yorqin displey va jim sovutish."
    },
    {
      id: 308,
      title: "Simsiz changyutgich va avtomobil kompressori 2in1",
      category: "avtotovarlar",
      categoryName: "Avtotovarlar",
      currentPrice: 280000,
      oldPrice: 390000,
      discountPercent: 28,
      installmentPrice: "30 000 so'm/oy",
      rating: 4.6,
      reviewsCount: 39,
      stockCount: 22,
      inOtherBaskets: 15,
      shopName: "AutoPro Tools",
      images: [
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&w=600&q=80"
      ],
      isLiked: false,
      quantityInCart: 0,
      description: "G'ildiraklarni tezkor damlash va avtomobil salonini bir zumda tozalash uchun ixcham qurilma."
    }
  ],

  // BACKEND: GET /api/v1/product/{id}/comments
  comments: [
    {
      id: 1,
      productId: 101,
      userName: "Sardorbek Rahimov",
      userAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
      rating: 5,
      createdAt: "2026-10-12 14:20",
      text: "Telefon ajoyib darajada tez ishlayapti! Kamera juda tiniq, 200MP haqiqatan ham seziladi. 1 kunda yetkazib berishdi, qadoqlanishi ham butun keldi. Tavsiya qilaman!",
      images: [
        "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=300&q=80"
      ]
    },
    {
      id: 2,
      productId: 101,
      userName: "Madina Yusupova",
      userAvatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80",
      rating: 5,
      createdAt: "2026-10-10 18:45",
      text: "O'zim uchun oldim, rangi juda yoqdi. Zaryadi 1.5 kunga erkin yetadi. Sovg'asiga chexol ham qo'shib berishdi. Katta rahmat do'kon jamoasiga!",
      images: [
        "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=300&q=80"
      ]
    },
    {
      id: 3,
      productId: 101,
      userName: "Javohir Tursunov",
      userAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80",
      rating: 4,
      createdAt: "2026-10-08 09:15",
      text: "Narxiga nisbatan juda yaxshi variant. O'yinlarda deyarli qizimaydi. Faqat qutisi burchagida ozgina ezilgan edi, lekin apparatga zarar yetmagan.",
      images: []
    },
    {
      id: 4,
      productId: 101,
      userName: "Gulnoza Rahimova",
      userAvatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=150&q=80",
      rating: 5,
      createdAt: "2026-10-05 11:30",
      text: "Ekran ravshanligi quyoshda ham bemalol ko'rinyapti. Ovoz sifati stereo baland va yoqimli. 10/10 ball beraman!",
      images: [
        "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=300&q=80"
      ]
    }
  ],

  // BACKEND: GET /api/v1/order/my-orders
  orders: [
    {
      id: 1001,
      uniqId: "ORD-984321",
      createdAt: "2026-10-14 16:30",
      status: "courier_delivering", // "created" | "processing" | "courier_delivering" | "delivered" | "cancelled"
      statusText: "Kuryer yo'lda",
      statusColor: "warning", // primary | warning | success | danger
      totalPrice: 3299000,
      deliveryMethod: "courier", // "courier" | "drop_off_point"
      deliveryAddress: "Toshkent sh., Chilonzor tumani, 9-mavze, 14-uy, 28-xonadon",
      paymentMethod: "credit_card",
      paymentMethodText: "Bank kartasi orqali to'langan",
      courier: {
        name: "Dilshod Akramov",
        phone: "+998 93 456 78 90",
        vehicle: "Skuter (Elektromoped)"
      },
      items: [
        {
          productId: 101,
          title: "Xiaomi Redmi Note 13 Pro 8/256GB Midnight Black",
          images: [
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=300&q=80"
          ],
          price: 3299000,
          quantity: 1,
          details: "Rangi: Qora, Xotirasi: 256GB, Do'kon: Xiaomi Official Store"
        }
      ]
    },
    {
      id: 1002,
      uniqId: "ORD-984102",
      createdAt: "2026-10-09 11:20",
      status: "delivered",
      statusText: "Yetkazib berildi",
      statusColor: "success",
      totalPrice: 2850000,
      deliveryMethod: "drop_off_point",
      deliveryAddress: "Tarqatish punkti: Chilonzor metro yaqinida, Bunyodkor shoh ko'chasi 12A",
      paymentMethod: "cash",
      paymentMethodText: "Qabul qilib olganda to'langan",
      courier: {
        name: "Uzum PVZ operatori",
        phone: "+998 78 140 00 00",
        vehicle: "PVZ"
      },
      items: [
        {
          productId: 102,
          title: "Apple AirPods Pro 2 MagSafe Case (USB-C)",
          images: [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=300&q=80"
          ],
          price: 2850000,
          quantity: 1,
          details: "Rangi: Oq, Turi: Simsiz garnitura, Do'kon: iStore Tashkent"
        }
      ]
    },
    {
      id: 1003,
      uniqId: "ORD-983890",
      createdAt: "2026-10-01 14:10",
      status: "delivered",
      statusText: "Yetkazib berildi",
      statusColor: "success",
      totalPrice: 920000,
      deliveryMethod: "courier",
      deliveryAddress: "Toshkent sh., Yakkasaroy tumani, Shota Rustaveli ko'chasi, 45-uy",
      paymentMethod: "installment",
      paymentMethodText: "Muddatli to'lov (12 oy)",
      courier: {
        name: "Jamshid Qodirov",
        phone: "+998 97 123 99 88",
        vehicle: "Avtomobil (Cobalt)"
      },
      items: [
        {
          productId: 103,
          title: "Erkaklar issiq kurtkasi, suv o'tkazmaydigan qishki",
          images: [
            "https://images.unsplash.com/photo-1544923246-77307dd654cb?auto=format&fit=crop&w=300&q=80"
          ],
          price: 580000,
          quantity: 1,
          details: "O'lchami: XL, Rangi: To'q ko'k, Do'kon: Nordic Wear"
        },
        {
          productId: 104,
          title: "Aqlli havo namlagich Smart Mist 4L",
          images: [
            "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=300&q=80"
          ],
          price: 340000,
          quantity: 1,
          details: "Hajmi: 4 Litr, Do'kon: EcoHome Tech"
        }
      ]
    }
  ],

  // BACKEND: GET /api/v1/courier/tasks (Kuryer buyurtmalari)
  courierTasks: {
    active: [
      {
        id: "CR-5501",
        orderId: "ORD-984321",
        customerName: "Olimjon Karimov",
        customerPhone: "+998 90 123 45 67",
        fromAddress: "Uzum Markaziy Ombori, Yangi Sergeli 15",
        toAddress: "Chilonzor tumani, 9-mavze, 14-uy, 28-xona",
        distance: "4.2 km",
        estimatedTime: "25 daqiqa",
        fee: 35000,
        status: "delivering", // "accepted" | "picked_up" | "delivering" | "done"
        statusText: "Xaridorga eltib berilmoqda",
        itemsSummary: "Xiaomi Redmi Note 13 Pro (1 dona)"
      }
    ],
    available: [
      {
        id: "CR-5502",
        orderId: "ORD-984405",
        customerName: "Aziza Karimova",
        customerPhone: "+998 91 876 54 32",
        fromAddress: "Uzum PVZ Mirzo Ulug'bek, Mustaqillik 68",
        toAddress: "Mirzo Ulug'bek tumani, Qorasuv-1, 12-uy",
        distance: "2.8 km",
        estimatedTime: "18 daqiqa",
        fee: 28000,
        status: "available",
        itemsSummary: "Dyson changyutgich va parfyum (2 ta paket)"
      },
      {
        id: "CR-5503",
        orderId: "ORD-984419",
        customerName: "Farrux Eshmatov",
        customerPhone: "+998 94 333 22 11",
        fromAddress: "Uzum Hub Yunusobod 19",
        toAddress: "Yunusobod 12-mavze, 3-uy, 15-xonadon",
        distance: "3.5 km",
        estimatedTime: "22 daqiqa",
        fee: 32000,
        status: "available",
        itemsSummary: "Nike Air Max poyabzali (1 ta quti)"
      }
    ],
    history: [
      {
        id: "CR-5490",
        orderId: "ORD-983991",
        completedAt: "Bugun, 14:15",
        customerName: "Bobur Ziyodov",
        toAddress: "Shayxontohur tumani, Navoiy 30",
        fee: 30000,
        ratingGiven: 5
      },
      {
        id: "CR-5489",
        orderId: "ORD-983944",
        completedAt: "Bugun, 12:40",
        customerName: "Nodira Karimova",
        toAddress: "Mirobod tumani, Nukus 18",
        fee: 35000,
        ratingGiven: 5
      }
    ]
  },

  // BACKEND: GET /api/v1/payment/promocodes/validate
  promoCodes: {
    "UZUM2026": { discountPercent: 10, minAmount: 200000, maxDiscount: 100000 },
    "OZONMARKET": { discountAmount: 50000, minAmount: 300000 },
    "YANGI": { discountPercent: 15, minAmount: 150000, maxDiscount: 80000 }
  },

  // BACKEND: GET /api/v1/payment/wallet (Wallet & Transaction_Log model)
  walletData: {
    id: 1,
    balance: 1450000,
    currency: "UZS",
    isBlocked: false,
    cards: [
      { id: 1, pan: "8600 •••• •••• 4219", type: "Uzcard", holder: "OLIMJON KARIMOV", isDefault: true, color: "linear-gradient(135deg, #1e3c72, #2a5298)" },
      { id: 2, pan: "9860 •••• •••• 8831", type: "Humo", holder: "OLIMJON KARIMOV", isDefault: false, color: "linear-gradient(135deg, #f7971e, #ffd200)" },
      { id: 3, pan: "4000 •••• •••• 1092", type: "Visa", holder: "OLIMJON KARIMOV", isDefault: false, color: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)" }
    ],
    transactionLogs: [
      { id: 901, paymentId: 101, amount: 3299000, type: "out", title: "Xiaomi Redmi Note 13 Pro to'lovi", date: "2026-10-14 16:32", status: "success", statusText: "Muvaffaqiyatli" },
      { id: 902, paymentId: 102, amount: 500000, type: "in", title: "Hamyon balansi to'ldirildi (Payme)", date: "2026-10-13 10:15", status: "success", statusText: "Qabul qilindi" },
      { id: 903, paymentId: 103, amount: 2850000, type: "out", title: "AirPods Pro 2 to'lovi", date: "2026-10-09 11:21", status: "success", statusText: "Muvaffaqiyatli" },
      { id: 904, paymentId: 104, amount: 920000, type: "out", title: "Kurtka va Namlagich to'lovi", date: "2026-10-01 14:12", status: "success", statusText: "Muvaffaqiyatli" }
    ]
  },

  // BACKEND: GET /api/v1/product/shop/{id} (Shop, Shop_Rating, Media model)
  shops: [
    {
      id: 1,
      name: "Xiaomi Official Store",
      slug: "xiaomi-store",
      banner: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
      logo: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=200&q=80",
      rating: 4.92,
      reviewsCount: 840,
      productsCount: 64,
      deliverySpeed: "1 kunda yetkazish",
      description: "Xiaomi brendining O'zbekistondagi rasmiy sertifikatlangan do'koni. Barcha smartfonlar, changyutgichlar va aqlli gadjetlar 1 yil rasmiy kafolat bilan taqdim etiladi.",
      phone: "+998 71 200 45 45",
      address: "Toshkent sh., Navoiy ko'chasi, 28-uy",
      workHours: "Har kuni 09:00 - 21:00"
    },
    {
      id: 2,
      name: "iStore Tashkent",
      slug: "istore",
      banner: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80",
      logo: "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=200&q=80",
      rating: 4.96,
      reviewsCount: 1250,
      productsCount: 112,
      deliverySpeed: "1 kunda yetkazish",
      description: "Apple original gadjetlari, MacBook, iPad va rasmiy aksessuarlari. 100% original kafolat va eng yaxshi bozor narxlari.",
      phone: "+998 71 200 99 99",
      address: "Toshkent sh., Amir Temur shoh ko'chasi, 107",
      workHours: "10:00 - 22:00"
    }
  ],

  // BACKEND: GET /api/v1/common/notifications (Notification & User_Notification model)
  notifications: [
    {
      id: 1,
      title: "Buyurtma kuryerga topshirildi 🚚",
      type: "order",
      message: "#ORD-984321 raqamli buyurtmangiz kuryer Dilshod Akramovga topshirildi va manzilingizga yo'l oldi.",
      readAt: null,
      createdAt: "Bugun 16:35",
      link: "order-tracking-page.html?tracking=TRK-984321"
    },
    {
      id: 2,
      title: "Katta bahorgi chegirmalar boshlandi! 🔥",
      type: "promo",
      message: "Barcha maishiy texnika va smartfonlarga 30% gacha keshbek va foizsiz muddatli to'lov e'lon qilindi.",
      readAt: "2026-10-14 10:00",
      createdAt: "Kecha 10:00",
      link: "home-page.html"
    },
    {
      id: 3,
      title: "Hamyoningiz balansi to'ldirildi 💳",
      type: "wallet",
      message: "Payme orqali hisobingizga +500 000 so'm mablag' muvaffaqiyatli qabul qilindi.",
      readAt: "2026-10-13 10:16",
      createdAt: "2026-10-13 10:15",
      link: "wallet-page.html"
    },
    {
      id: 4,
      title: "Kuryerlik arizangiz ma'qullandi! ⚡",
      type: "role",
      message: "Tabriklaymiz! Sizning kuryer bo'lib ishlash arizangiz tasdiqlandi. Kuryer portalidan buyurtmalarni qabul qilishingiz mumkin.",
      readAt: "2026-09-16 12:00",
      createdAt: "2026-09-15 17:30",
      link: "courier-page.html"
    }
  ],

  // BACKEND: GET /api/v1/order/delivery-tracking/{code} (Delivery_Process model)
  deliveryTrackingData: {
    trackingCode: "TRK-984321",
    orderId: "ORD-984321",
    status: "in_transit",
    statusText: "Xaridor manziliga eltib berilmoqda",
    estimatedDelivery: "Bugun, taxminan 25 daqiqa ichida",
    deliveryFee: 0,
    isFree: true,
    courier: {
      name: "Dilshod Akramov",
      phone: "+998 93 456 78 90",
      vehicle: "Skuter (Elektromoped)",
      rating: 4.95,
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
    },
    destination: "Toshkent sh., Chilonzor tumani, 9-mavze, 14-uy, 28-xonadon",
    steps: [
      { id: 1, title: "Buyurtma qabul qilindi", desc: "Buyurtma tizimga muvaffaqiyatli tushdi va to'lov tasdiqlandi", time: "14:10", done: true },
      { id: 2, title: "Omborda yig'ildi va qadoqlandi", desc: "Uzum Markaziy omborida tekshiruvdan o'tkazilib qadoqlandi", time: "15:20", done: true },
      { id: 3, title: "Kuryerga topshirildi", desc: "Kuryer buyurtmani qabul qilib oldi", time: "16:30", done: true },
      { id: 4, title: "Kuryer yo'lda (Yetkazilmoqda)", desc: "Kuryer ko'rsatilgan manzilga qarab harakatlanmoqda", time: "16:45 (Ayni damda)", current: true, done: false },
      { id: 5, title: "Mijozga topshirildi", desc: "Buyurtma qabul qilib olinadi", time: "Kutilmoqda", done: false }
    ]
  },

  // BACKEND: GET /api/v1/user/role-request (Role_Request model)
  roleRequests: [
    {
      id: 101,
      role: "courier",
      roleTitle: "Kuryerlik xizmati",
      application: "Skuter transportim bor, Chilonzor hududida buyurtmalarni o'z vaqtida yetkazib bera olaman.",
      resumeUrl: "https://example.com/resumes/olimjon_resume.pdf",
      checkingStatus: "approved",
      statusText: "Tasdiqlangan",
      appliedAt: "2026-09-15 14:00",
      reviewedAt: "2026-09-15 17:30"
    }
  ]
};

// Global scope ga eksport
window.MOCK_DATA = MOCK_DATA;
