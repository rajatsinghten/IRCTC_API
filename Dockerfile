FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    unzip \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libnspr4 \
    libnss3 \
    lsb-release \
    xdg-utils \
    libxss1 \
    libgbm1 \
    libu2f-udev \
    libvulkan1 \
    libcurl4 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"
ENV GOOGLE_CHROME_BIN="/usr/bin/google-chrome-stable"
ENV PATH="/usr/bin:${PATH}"
ENV PORT=5000

EXPOSE ${PORT}

CMD sh -c "exec gunicorn -b 0.0.0.0:${PORT:-5000} app:app"
