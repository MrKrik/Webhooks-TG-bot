# Этап сборки
FROM python:3.13 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.13-slim
WORKDIR /code

# Копируем установленные зависимости из builder
COPY --from=builder /root/.local /root/.local
# Копируем остальные файлы проекта
COPY . .

# Указываем PATH для pip-пакетов
ENV PATH=/root/.local/bin:$PATH
# Переменные окружения
ENV TOKEN=${TOKEN}
ENV URL=${URL} 
ENV DB_URL=${DB_URL}
ENV TEST_SERVER=${TEST_SERVER}
# Оптимизация для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Команда запуска 
CMD sh -c "python init_db.py && python main.py & uvicorn app:app --host 0.0.0.0 --port 5000"