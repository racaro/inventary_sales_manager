# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install all necessary dependencies including Qt libraries
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    python3-dev \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxcb1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgtk-3-0 \
    libdbus-1-3 \
    libegl1-mesa \
    libfontconfig1 \
    libgcc-s1 \
    libgssapi-krb5-2 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb-glx0 \
    libxcb-cursor0 \
    libxi6 \
    libxrender1 \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY main.py .

# Create data directories
RUN mkdir -p /app/data /app/backups

# Environment variables
ENV DISPLAY=:99
ENV QT_X11_NO_MITSHM=1
ENV QT_DEBUG_PLUGINS=1

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Xvfb..."\n\
Xvfb :99 -screen 0 1024x768x16 -ac +extension GLX +render -noreset &\n\
sleep 3\n\
\n\
echo "Starting window manager..."\n\
fluxbox &\n\
sleep 2\n\
\n\
echo "Starting VNC server..."\n\
x11vnc -display :99 -nopw -forever -shared -listen 0.0.0.0 -rfbport 5900 -xkb &\n\
sleep 3\n\
\n\
echo "Testing X server..."\n\
export DISPLAY=:99\n\
xdpyinfo || echo "X server test failed but continuing..."\n\
\n\
echo "Starting Stock Manager application..."\n\
python3 main.py || (echo "Application failed, keeping container alive" && tail -f /dev/null)\n' > start.sh && chmod +x start.sh

# Expose VNC port
EXPOSE 5900

# Run the startup script
CMD ["./start.sh"]
