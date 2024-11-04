FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install && pip install --upgrade pip

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы
COPY . .

# Открываем порт для FastAPI
EXPOSE 8092

CMD ["python", "main.py"]