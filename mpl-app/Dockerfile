FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    libx11-dev \
    libgtk-3-dev \
    libxcb1-dev \
    libxtst-dev \
    libxkbcommon-x11-dev \
    libxslt-dev \
    libxml2-dev \
    libxslt1-dev \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the display environment variable
ENV DISPLAY=:0

# Run a sample matplotlib plot
COPY . .
CMD ["python3", "plot_example.py"]
