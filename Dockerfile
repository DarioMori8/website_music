# Dockerfile

FROM python:3.10.0-slim


RUN sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' /etc/apt/sources.list

# Installa i pacchetti necessari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev

# Pulizia
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Imposta il workdir dell'applicazione
WORKDIR /app

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copia il resto del codice dell'applicazione
COPY . .

# Crea la cartella per i file statici
RUN mkdir -p /app/website_music/static/
RUN mkdir -p /app/website_music/media/


# Raccoglie i file statici di Django
RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

# Imposta le variabili d'ambiente (placeholder)
ENV DJANGO_SETTINGS_MODULE=website_music.settings
ENV PORT=8000

# Comando di avvio dell'applicazione con Gunicorn
CMD gunicorn website_music.wsgi:application --bind 0.0.0.0:$PORT
