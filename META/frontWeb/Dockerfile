FROM node:21.6

RUN npm install -g pnpm
RUN apt update
RUN mkdir /code-server
WORKDIR /code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN mkdir /web
WORKDIR /web

COPY ./META/frontWeb/run_dev.sh /root/run_dev.sh