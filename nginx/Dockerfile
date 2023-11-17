FROM nginx:latest

# Install curl
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN rm -f /etc/nginx/conf.d/*

COPY ./nginx.conf /etc/nginx/
ADD nginx.conf /etc/nginx/nginx.conf

CMD ["/entrypoint.sh"]

EXPOSE 80
