/**
 * Market Frontend API Layer
 * 
 * Ushbu modul backend API bilan aloqa qilish uchun xizmat qiladi.
 * Hozirgi bosqichda localStorage va MOCK_DATA asosida ishlaydi.
 * Backend tayyor bo'lgach, har bir metod ichidagi TODO qismini haqiqiy
 * fetch() so'rovi bilan almashtirish kifoya.
 */

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

class MarketAPI {
  constructor() {
    this.initStorage();
  }

  // LocalStorage ni boshlang'ich ma'lumotlar bilan to'ldirish
  initStorage() {
    if (!localStorage.getItem("market_cart")) {
      // Dastlabki savat: 1 ta tovar
      const initialCart = [
        {
          product: MOCK_DATA.seasonalProducts[1], // AirPods Pro 2
          quantity: 1,
          isSelected: true
        }
      ];
      localStorage.setItem("market_cart", JSON.stringify(initialCart));
    }

    if (!localStorage.getItem("market_likes")) {
      const initialLikes = [102, 202, 302, 304, 307];
      localStorage.setItem("market_likes", JSON.stringify(initialLikes));
    }

    if (!localStorage.getItem("market_orders")) {
      localStorage.setItem("market_orders", JSON.stringify(MOCK_DATA.orders));
    }

    if (!localStorage.getItem("market_courier_tasks")) {
      localStorage.setItem("market_courier_tasks", JSON.stringify(MOCK_DATA.courierTasks));
    }
  }

  // --- FOYDALANUVCHI (AUTH & USER) ---
  // BACKEND: GET /api/v1/auth/me
  async getCurrentUser() {
    // REAL BACKEND FETCH:
    // const res = await fetch(`${API_BASE_URL}/auth/me`, { headers: this.getAuthHeaders() });
    // return await res.json();
    return Promise.resolve(MOCK_DATA.currentUser);
  }

  // BACKEND: PUT /api/v1/user/profile
  async updateUserProfile(profileData) {
    // REAL BACKEND:
    // const res = await fetch(`${API_BASE_URL}/user/profile`, { method: 'PUT', body: JSON.stringify(profileData) });
    MOCK_DATA.currentUser = { ...MOCK_DATA.currentUser, ...profileData };
    return Promise.resolve(MOCK_DATA.currentUser);
  }

  // --- KATEGORIYALAR ---
  // BACKEND: GET /api/v1/product/categories
  async getCategories() {
    return Promise.resolve(MOCK_DATA.categories);
  }

  // --- MAHSULOTLAR (PRODUCTS) ---
  // BACKEND: GET /api/v1/product/seasonal/
  async getSeasonalProducts() {
    return Promise.resolve(MOCK_DATA.seasonalProducts);
  }

  // BACKEND: GET /api/v1/product/weekly/
  async getWeeklyProducts() {
    return Promise.resolve(MOCK_DATA.weeklyProducts);
  }

  // BACKEND: GET /api/v1/product/list?page=1&limit=10
  async getLandingProducts(page = 1, limit = 8) {
    // Sahifalash mantiqi
    const all = MOCK_DATA.landingProducts;
    return Promise.resolve({
      page,
      limit,
      total: all.length,
      items: all
    });
  }

  // BACKEND: GET /api/v1/product/{id}
  async getProductById(id) {
    const allProducts = [
      ...MOCK_DATA.seasonalProducts,
      ...MOCK_DATA.weeklyProducts,
      ...MOCK_DATA.landingProducts
    ];
    const found = allProducts.find(p => p.id === Number(id)) || MOCK_DATA.seasonalProducts[0];
    return Promise.resolve(found);
  }

  // BACKEND: GET /api/v1/product/category/{slug}?page=1
  async getProductsByCategory(categorySlug, page = 1) {
    const all = [
      ...MOCK_DATA.seasonalProducts,
      ...MOCK_DATA.weeklyProducts,
      ...MOCK_DATA.landingProducts
    ];
    const filtered = categorySlug && categorySlug !== "all" 
      ? all.filter(p => p.category === categorySlug) 
      : all;
    return Promise.resolve({
      category: categorySlug,
      page,
      total: filtered.length,
      items: filtered
    });
  }

  // BACKEND: GET /api/v1/product/{id}/comments?page=1
  async getProductComments(productId, page = 1) {
    return Promise.resolve({
      page,
      totalPages: 3,
      items: MOCK_DATA.comments
    });
  }

  // --- SAVATCHA (CART / BUCKET) ---
  // BACKEND: GET /api/v1/order/bucket
  getCart() {
    try {
      return JSON.parse(localStorage.getItem("market_cart")) || [];
    } catch {
      return [];
    }
  }

  saveCart(cart) {
    localStorage.setItem("market_cart", JSON.stringify(cart));
    window.dispatchEvent(new Event("cartUpdated"));
  }

  addToCart(product, quantity = 1) {
    const cart = this.getCart();
    const existingIndex = cart.findIndex(item => item.product.id === product.id);

    if (existingIndex > -1) {
      cart[existingIndex].quantity += quantity;
      if (cart[existingIndex].quantity <= 0) {
        cart.splice(existingIndex, 1);
      }
    } else if (quantity > 0) {
      cart.push({
        product: product,
        quantity: quantity,
        isSelected: true
      });
    }

    this.saveCart(cart);
    return cart;
  }

  updateCartQuantity(productId, quantity) {
    const cart = this.getCart();
    const item = cart.find(i => i.product.id === Number(productId));
    if (item) {
      item.quantity = quantity;
      if (item.quantity <= 0) {
        const index = cart.indexOf(item);
        cart.splice(index, 1);
      }
      this.saveCart(cart);
    }
    return cart;
  }

  toggleCartSelection(productId, isSelected) {
    const cart = this.getCart();
    const item = cart.find(i => i.product.id === Number(productId));
    if (item) {
      item.isSelected = isSelected;
      this.saveCart(cart);
    }
    return cart;
  }

  // --- SEVIMLILAR (LIKES) ---
  getLikes() {
    try {
      return JSON.parse(localStorage.getItem("market_likes")) || [];
    } catch {
      return [];
    }
  }

  toggleLike(productId) {
    const id = Number(productId);
    let likes = this.getLikes();
    const isLiked = likes.includes(id);

    if (isLiked) {
      likes = likes.filter(x => x !== id);
    } else {
      likes.push(id);
    }

    localStorage.setItem("market_likes", JSON.stringify(likes));
    window.dispatchEvent(new Event("likesUpdated"));
    return !isLiked;
  }

  isProductLiked(productId) {
    return this.getLikes().includes(Number(productId));
  }

  // --- BUYURTMALAR (ORDERS) ---
  // BACKEND: GET /api/v1/order/my-orders
  async getMyOrders() {
    try {
      return JSON.parse(localStorage.getItem("market_orders")) || MOCK_DATA.orders;
    } catch {
      return MOCK_DATA.orders;
    }
  }

  // BACKEND: POST /api/v1/order/create
  async createOrder(orderPayload) {
    const orders = await this.getMyOrders();
    const newOrder = {
      id: Date.now(),
      uniqId: "ORD-" + Math.floor(100000 + Math.random() * 900000),
      createdAt: new Date().toISOString().replace('T', ' ').substring(0, 16),
      status: "processing",
      statusText: "Tayyorlanmoqda",
      statusColor: "warning",
      totalPrice: orderPayload.totalPrice,
      deliveryMethod: orderPayload.deliveryMethod,
      deliveryAddress: orderPayload.deliveryAddress,
      paymentMethod: orderPayload.paymentMethod,
      paymentMethodText: orderPayload.paymentMethodText || "To'lov amalga oshirilgan",
      items: orderPayload.items || []
    };

    orders.unshift(newOrder);
    localStorage.setItem("market_orders", JSON.stringify(orders));

    // Savatdan tanlangan tovarlarni o'chirish
    const remainingCart = this.getCart().filter(item => !item.isSelected);
    this.saveCart(remainingCart);

    return newOrder;
  }

  // --- KURYER FUNKSIYALARI (COURIER) ---
  // BACKEND: GET /api/v1/courier/dashboard
  async getCourierTasks() {
    try {
      return JSON.parse(localStorage.getItem("market_courier_tasks")) || MOCK_DATA.courierTasks;
    } catch {
      return MOCK_DATA.courierTasks;
    }
  }

  // BACKEND: POST /api/v1/courier/order/{id}/accept
  async acceptCourierTask(taskId) {
    const tasks = await this.getCourierTasks();
    const taskIndex = tasks.available.findIndex(t => t.id === taskId);
    if (taskIndex > -1) {
      const task = tasks.available.splice(taskIndex, 1)[0];
      task.status = "delivering";
      task.statusText = "Xaridorga eltib berilmoqda";
      tasks.active.push(task);
      localStorage.setItem("market_courier_tasks", JSON.stringify(tasks));
      return { success: true, task };
    }
    return { success: false, message: "Buyurtma topilmadi" };
  }

  // BACKEND: POST /api/v1/courier/order/{id}/complete
  async completeCourierTask(taskId) {
    const tasks = await this.getCourierTasks();
    const activeIndex = tasks.active.findIndex(t => t.id === taskId);
    if (activeIndex > -1) {
      const task = tasks.active.splice(activeIndex, 1)[0];
      task.status = "done";
      task.completedAt = "Hozirgina";
      tasks.history.unshift(task);

      // Kuryer balansini oshirish
      MOCK_DATA.currentUser.courierProfile.currentBalance += task.fee;
      MOCK_DATA.currentUser.courierProfile.todayEarnings += task.fee;
      MOCK_DATA.currentUser.courierProfile.completedToday += 1;

      localStorage.setItem("market_courier_tasks", JSON.stringify(tasks));
      return { success: true, task };
    }
    return { success: false, message: "Faol buyurtma topilmadi" };
  }

  // --- HAMYON (WALLET & TRANSACTIONS) ---
  // BACKEND: GET /api/v1/payment/wallet
  async getWalletData() {
    try {
      return JSON.parse(localStorage.getItem("market_wallet")) || MOCK_DATA.walletData;
    } catch {
      return MOCK_DATA.walletData;
    }
  }

  // BACKEND: POST /api/v1/payment/wallet/topup
  async topUpWallet(amount) {
    const wallet = await this.getWalletData();
    wallet.balance += Number(amount);
    wallet.transactionLogs.unshift({
      id: Date.now(),
      paymentId: Math.floor(100 + Math.random() * 900),
      amount: Number(amount),
      type: "in",
      title: "Hamyon to'ldirildi (Onlayn to'lov)",
      date: new Date().toISOString().replace('T', ' ').substring(0, 16),
      status: "success",
      statusText: "Qabul qilindi"
    });
    localStorage.setItem("market_wallet", JSON.stringify(wallet));
    MOCK_DATA.currentUser.balance = wallet.balance;
    return wallet;
  }

  // BACKEND: POST /api/v1/payment/card/add
  async addCard(card) {
    const wallet = await this.getWalletData();
    wallet.cards.push({
      id: Date.now(),
      pan: card.pan,
      type: card.type || "Uzcard",
      holder: card.holder || "OLIMJON KARIMOV",
      isDefault: false,
      color: "linear-gradient(135deg, #434343, #000000)"
    });
    localStorage.setItem("market_wallet", JSON.stringify(wallet));
    return wallet;
  }

  // --- DO'KONLAR (SHOP & SHOP_RATING) ---
  // BACKEND: GET /api/v1/product/shops
  async getShops() {
    return Promise.resolve(MOCK_DATA.shops);
  }

  // BACKEND: GET /api/v1/product/shop/{id}
  async getShopById(id) {
    const shop = MOCK_DATA.shops.find(s => s.id === Number(id)) || MOCK_DATA.shops[0];
    return Promise.resolve(shop);
  }

  // BACKEND: POST /api/v1/product/shop/{id}/rate
  async rateShop(shopId, ball) {
    const shop = await this.getShopById(shopId);
    shop.rating = Number(((shop.rating * shop.reviewsCount + ball) / (shop.reviewsCount + 1)).toFixed(2));
    shop.reviewsCount += 1;
    return { success: true, newRating: shop.rating };
  }

  // --- BILDIRISHNOMALAR (NOTIFICATIONS) ---
  // BACKEND: GET /api/v1/common/notifications
  async getNotifications() {
    try {
      return JSON.parse(localStorage.getItem("market_notifications")) || MOCK_DATA.notifications;
    } catch {
      return MOCK_DATA.notifications;
    }
  }

  // BACKEND: POST /api/v1/common/notifications/{id}/read
  async markNotificationRead(id) {
    const notifs = await this.getNotifications();
    const item = notifs.find(n => n.id === Number(id));
    if (item) {
      item.readAt = new Date().toISOString();
      localStorage.setItem("market_notifications", JSON.stringify(notifs));
    }
    return notifs;
  }

  // --- YETKAZISHNI KUZATISH (DELIVERY TRACKING) ---
  // BACKEND: GET /api/v1/order/delivery-tracking/{code}
  async getDeliveryTracking(code) {
    return Promise.resolve(MOCK_DATA.deliveryTrackingData);
  }

  // --- ROLE REQUEST (ROLE ARIZALARI) ---
  // BACKEND: POST /api/v1/user/role-request
  async submitRoleRequest(role, application, resumeUrl) {
    const newReq = {
      id: Date.now(),
      role: role,
      roleTitle: role === 'courier' ? "Kuryerlik xizmati" : "Sotuvchi (Merchant)",
      application: application,
      resumeUrl: resumeUrl || "ariza.pdf",
      checkingStatus: "pending",
      statusText: "Ko'rib chiqilmoqda",
      appliedAt: new Date().toISOString().replace('T', ' ').substring(0, 16)
    };
    MOCK_DATA.roleRequests.unshift(newReq);
    return newReq;
  }
}

// Global API obyektini yaratish
window.marketAPI = new MarketAPI();
