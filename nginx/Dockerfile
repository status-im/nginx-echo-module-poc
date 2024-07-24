ARG nginx_version=1.23.2

FROM debian:bullseye-slim AS builder

ARG nginx_version

ENV NGINX_VERSION=${nginx_version}

RUN apt update && \
    apt install -y \
    build-essential \
    curl \
    git \
    libpcre++-dev \
    zlib1g-dev

RUN curl http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -o /tmp/nginx-${NGINX_VERSION}.tar.gz && \
    cd /tmp && \
    tar xvzf nginx-${NGINX_VERSION}.tar.gz

RUN git clone https://github.com/openresty/echo-nginx-module.git /tmp/echo-nginx-module && \
    cd /tmp/nginx-${NGINX_VERSION} && \
    ./configure --with-compat --add-dynamic-module=/tmp/echo-nginx-module && \
    make -j2 && \
    make install

FROM nginx:${nginx_version}

COPY --from=builder /tmp/nginx-${NGINX_VERSION}/objs/* /etc/nginx/modules/

COPY --from=builder /usr/local/lib/* /lib/x86_64-linux-gnu/
