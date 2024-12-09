FROM python:3.8-slim

# Clean up unnecessary files before installing packages
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install system packages
RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        nginx supervisor vim build-essential libpq-dev gettext \
        libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
        libjpeg-dev libopenjp2-7-dev libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Copy Nginx config
COPY nginx-config/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Install Python dependencies
COPY requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt

# Install Granian globally
RUN pip install granian

# Setup project directory
RUN mkdir -p /opt/app/web_apps
COPY . /opt/app/web_apps
WORKDIR /opt/app/web_apps

# Copy supervisor config
COPY supervisor-config/task-granian.conf /etc/supervisor/conf.d/task-granian.conf

# Create granian log directory
RUN mkdir -p /var/log/granian && chown -R root:root /var/log/granian

# Copy and make the start script executable
COPY docker-entry-point/start-server.sh /opt/app/start-server.sh
RUN chmod +x /opt/app/start-server.sh

# Expose the port
EXPOSE 8020

# Run supervisord
ENTRYPOINT ["/opt/app/start-server.sh"]
CMD ["supervisord", "-n"]
