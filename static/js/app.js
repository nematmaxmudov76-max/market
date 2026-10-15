/**
 * Market Frontend Main Application Logic
 * 
 * Ushbu skript barcha sahifalardagi umumiy interaktivlikni,
 * savatcha, sevimlilar, bildirishnomalar va UI animatsiyalarini boshqaradi.
 */

// Narxni chiroyli so'm formatiga o'tkazish
function formatPrice(amount) {
  if (amount === undefined || amount === null) return "0 so'm";
  return new Intl.NumberFormat('uz-UZ').format(amount) + " so'm";
}

// Toast xabarnomasi chiqarish
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  let icon = '🔔';
  if (type === 'success') icon = '✅';
  if (type === 'warning') icon = '⚠️';
  if (type === 'danger') icon = '❌';

  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

// Header dagi Savat va Sevimlilar hisoblagichini yangilash
function updateHeaderCounters() {
  const cartBadge = document.getElementById('header-cart-count');
  const likesBadge = document.getElementById('header-likes-count');

  if (window.marketAPI) {
    const cart = window.marketAPI.getCart();
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (cartBadge) {
      cartBadge.textContent = totalCount;
      cartBadge.style.display = totalCount > 0 ? 'inline-block' : 'none';
    }

    const likes = window.marketAPI.getLikes();
    if (likesBadge) {
      likesBadge.textContent = likes.length;
      likesBadge.style.display = likes.length > 0 ? 'inline-block' : 'none';
    }
  }
}

// Slayderni chapga/o'ngga siljitish
function slideRow(containerId, direction) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const scrollAmount = direction === 'left' ? -320 : 320;
  container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
}

// Mahsulot kartasi HTML shablonini generatsiya qilish
function renderProductCard(p, inCartCount = 0) {
  const isLiked = window.marketAPI ? window.marketAPI.isProductLiked(p.id) : false;
  const currentImg = (p.images && p.images.length > 0) ? p.images[0] : 'https://placehold.co/400';

  return `
    <div class="product-card" id="product-card-${p.id}">
      <div class="card-media">
        <span class="badge-discount">-${p.discountPercent || 15}%</span>
        <button class="btn-like ${isLiked ? 'liked' : ''}" onclick="handleLikeClick(event, ${p.id})" title="Sevimlilarga qo'shish">
          ♥
        </button>
        <button class="card-nav-arrow prev" onclick="handleCardImageNav(event, ${p.id}, -1)">‹</button>
        <img src="${currentImg}" alt="${p.title}" class="card-img" id="card-img-${p.id}" data-current-index="0" data-images='${JSON.stringify(p.images)}'>
        <button class="card-nav-arrow next" onclick="handleCardImageNav(event, ${p.id}, 1)">‹</button>
      </div>

      <div class="card-body">
        <a href="one-product-detail.html?id=${p.id}" class="card-title" title="${p.title}">
          ${p.title}
        </a>

        <div class="card-rating-row">
          <span class="stars">★ ${p.rating}</span>
          <span>(${p.reviewsCount} sharh)</span>
          <span class="badge-stock">Omborda: ${p.stockCount} ta</span>
        </div>

        <div class="card-installment">${p.installmentPrice || "35 000 so'm/oy"}</div>

        <div class="card-prices">
          <span class="current-price">${formatPrice(p.currentPrice)}</span>
          ${p.oldPrice ? `<span class="old-price">${formatPrice(p.oldPrice)}</span>` : ''}
        </div>

        <div class="card-action-bar">
          <div class="qty-stepper">
            <button class="qty-btn" onclick="handleCardQtyChange(event, ${p.id}, -1)">-</button>
            <span class="qty-value" id="card-qty-${p.id}">${inCartCount}</span>
            <button class="qty-btn" onclick="handleCardQtyChange(event, ${p.id}, 1)">+</button>
          </div>
          <button class="btn-to-cart ${inCartCount > 0 ? 'in-cart' : ''}" id="btn-cart-${p.id}" onclick="handleAddToCartClick(event, ${p.id})">
            🛒 ${inCartCount > 0 ? "Savatda" : "Savatga"}
          </button>
        </div>
      </div>
    </div>
  `;
}

// Kartadagi rasmlarni chapga/o'ngga almashtirish
function handleCardImageNav(event, productId, step) {
  event.stopPropagation();
  event.preventDefault();
  const imgEl = document.getElementById(`card-img-${productId}`);
  if (!imgEl) return;

  const images = JSON.parse(imgEl.getAttribute('data-images') || '[]');
  if (images.length <= 1) return;

  let currentIndex = parseInt(imgEl.getAttribute('data-current-index') || '0', 10);
  currentIndex = (currentIndex + step + images.length) % images.length;
  imgEl.src = images[currentIndex];
  imgEl.setAttribute('data-current-index', currentIndex);
}

// Like bosish hodisasi
function handleLikeClick(event, productId) {
  event.stopPropagation();
  event.preventDefault();
  const isNowLiked = window.marketAPI.toggleLike(productId);
  const btn = event.currentTarget;
  if (isNowLiked) {
    btn.classList.add('liked');
    showToast("Mahsulot sevimlilarga qo'shildi! ❤️", 'success');
  } else {
    btn.classList.remove('liked');
    showToast("Mahsulot sevimlilardan olib tashlandi", 'info');
  }
  updateHeaderCounters();
}

// Kartadagi miqdorni (- 0 +) o'zgartirish
function handleCardQtyChange(event, productId, change) {
  event.stopPropagation();
  event.preventDefault();

  const qtyEl = document.getElementById(`card-qty-${productId}`);
  let currentQty = parseInt(qtyEl.textContent || '0', 10);
  currentQty = Math.max(0, currentQty + change);
  qtyEl.textContent = currentQty;

  // Agar savatda mavjud bo'lsa yangilaymiz
  const cart = window.marketAPI.getCart();
  const existing = cart.find(i => i.product.id === productId);

  if (existing) {
    window.marketAPI.updateCartQuantity(productId, currentQty);
    const cartBtn = document.getElementById(`btn-cart-${productId}`);
    if (cartBtn) {
      if (currentQty > 0) {
        cartBtn.classList.add('in-cart');
        cartBtn.innerHTML = "🛒 Savatda";
      } else {
        cartBtn.classList.remove('in-cart');
        cartBtn.innerHTML = "🛒 Savatga";
      }
    }
  }
}

// "Savatga" tugmasi bosilganda
async function handleAddToCartClick(event, productId) {
  event.stopPropagation();
  event.preventDefault();

  const product = await window.marketAPI.getProductById(productId);
  const qtyEl = document.getElementById(`card-qty-${productId}`);
  let count = parseInt(qtyEl ? qtyEl.textContent : '1', 10);
  if (count <= 0) count = 1;

  window.marketAPI.addToCart(product, count);
  if (qtyEl) qtyEl.textContent = count;

  const btn = event.currentTarget;
  btn.classList.add('in-cart');
  btn.innerHTML = "🛒 Savatda";

  showToast(`${product.title.substring(0, 24)}... savatga qo'shildi!`, 'success');
  updateHeaderCounters();
}

// Qidiruv shakli hodisasi
function setupSearch() {
  const searchInput = document.getElementById('search-input');
  const searchForm = document.getElementById('search-form');
  if (searchForm && searchInput) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = searchInput.value.trim();
      if (query) {
        window.location.href = `product-by-this-type.html?search=${encodeURIComponent(query)}`;
      }
    });
  }
}

// Sahifa yuklanganda umumiy initsializatsiya
document.addEventListener('DOMContentLoaded', () => {
  updateHeaderCounters();
  setupSearch();

  // Boshqa oynalardan yoki eventlardan savat yangilanganda
  window.addEventListener('cartUpdated', updateHeaderCounters);
  window.addEventListener('likesUpdated', updateHeaderCounters);
});
