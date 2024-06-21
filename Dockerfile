# Utilizza un'immagine di base Python slim
FROM python:3.10.0-slim

# Aggiorna i repository e installa le dipendenze di sistema
RUN sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Imposta il workdir dell'applicazione
WORKDIR /app

# Copia il file requirements.txt e installa le dipendenze Python
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copia il resto del codice dell'applicazione
COPY . .

# Crea le cartelle per i file statici e media
RUN mkdir -p /app/staticfiles /app/media

# Raccoglie i file statici di Django
RUN python manage.py collectstatic --noinput

# Applica le migrazioni del database
RUN python manage.py migrate

# Imposta le variabili d'ambiente
ENV DJANGO_SETTINGS_MODULE=website_music.settings
ENV PORT=8000

# Comando di avvio dell'applicazione con Gunicorn
CMD ["gunicorn", "website_music.wsgi:application", "--bind", "0.0.0.0:8000"]
