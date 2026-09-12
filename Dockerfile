FROM python:3.12-slim

# Ishchi papkani belgilash
WORKDIR /app

# Tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# uv paket menejerini o'rnatish
RUN pip install --no-cache-dir uv

# Bog'liqliklarni o'rnatish (Keshdan unumli foydalanish uchun koddan oldin o'rnatamiz)
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml

# Barcha loyiha kodini konteynerga o'tkazish
COPY . .

# FastAPI'ni ishga tushirish
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

ENV PYTHONUNBUFFERED=1