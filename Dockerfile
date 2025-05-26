# Use a base Python image
FROM python:3.9-slim-buster

# Install Chrome and its dependencies
# These commands are for Debian-based systems (like buster)
# They install necessary libraries and then Google Chrome Stable
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
    libflashplugin \
    libcurl4 \
    libdbus-glib-1-2

# Download and install Google Chrome Stable
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Set the working directory in the container
WORKDIR /app

# Copy your requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Ensure the chromedriver is in PATH and specify Chrome binary location (optional, webdriver_manager might handle it)
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"
ENV GOOGLE_CHROME_BIN="/usr/bin/google-chrome-stable"
ENV PATH="/usr/bin:${PATH}" 
# Add /usr/bin to PATH where Chrome is

# Expose the port your Flask app runs on
ENV PORT 5000
EXPOSE $PORT

# Command to run your Flask application
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"] 
# Use gunicorn for production