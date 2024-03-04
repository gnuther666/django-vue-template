FROM node:21.6

RUN yarn config set registry http://mirrors.cloud.tencent.com/npm/
RUN yarn global add @tarojs/cli

RUN mkdir /web
WORKDIR /web