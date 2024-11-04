# Start from an Ubuntu base image
FROM ubuntu:latest

# Environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Add Ondrej's PPA for NGINX with Lua support
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:ondrej/nginx && \
    apt-get update

# Install NGINX and Lua dependencies
RUN apt-get install -y \
    nginx \
    curl \
    zip \
    luajit \
    libnginx-mod-http-lua \
    libnginx-mod-http-ndk \
    lua-resty-core \
    lua-resty-lrucache \
    lua-cjson && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Lua directory structure exists for resty
RUN mkdir -p /usr/local/share/lua/5.1/resty

# Download and install lua-resty-string
RUN curl -L -o /tmp/lua-resty-string.zip https://github.com/openresty/lua-resty-string/archive/refs/heads/master.zip && \
    unzip /tmp/lua-resty-string.zip -d /tmp && \
    cp -r /tmp/lua-resty-string-master/lib/resty/* /usr/local/share/lua/5.1/resty/ && \
    rm -rf /tmp/lua-resty-string.zip /tmp/lua-resty-string-master

# Copy Lua resty libraries from GitHub to the correct path
RUN curl -L -o /tmp/lua-resty-http.zip https://github.com/ledgetech/lua-resty-http/archive/refs/heads/master.zip && \
    unzip /tmp/lua-resty-http.zip -d /tmp && \
    cp -r /tmp/lua-resty-http-master/lib/resty/* /usr/local/share/lua/5.1/resty/ && \
    rm -rf /tmp/lua-resty-http.zip /tmp/lua-resty-http-master

# Set up NGINX to run in the foreground
CMD ["nginx", "-g", "daemon off;"]

# Expose HTTP and HTTPS ports
EXPOSE 80 443
