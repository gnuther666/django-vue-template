FROM centos:centos7
RUN yum update -y
RUN yum install -y openssh-server
WORKDIR /usr/local
RUN yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel unzip
RUN yum install -y wget mesa-libGL
RUN wget http://npm.taobao.org/mirrors/python/3.9.0/Python-3.9.0.tgz
RUN tar -zxvf Python-3.9.0.tgz
WORKDIR /usr/local/Python-3.9.0
RUN ./configure prefix=/usr/local/python3 && make && make install
RUN ln -s /usr/local/python3/bin/python3.9 /usr/bin/python3
WORKDIR /root
COPY ./META/backend/requirements.txt /root
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt --no-cache-dir
RUN mkdir /backend
WORKDIR /backend
