FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get update
RUN apt-get install -y curl jq python3-pip build-essential php8.1-fpm php8.1-gd php-json php8.1-mysql php8.1-curl php8.1-mbstring php8.1-intl php-imagick php8.1-xml php8.1-zip
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN pip3 install requests numpy

RUN mkdir /app
WORKDIR /app

COPY ./dashboard /app/dashboard
COPY ./progpilot_wp /app/progpilot_wp


EXPOSE 8000
WORKDIR /app/dashboard

RUN rm /app/progpilot_wp/plugins
RUN ln -s /app/pwnlab-wordpress/plugins /app/progpilot_wp/plugins
RUN /app/progpilot_wp/install_progpilot.sh

CMD ["npm", "start"]


