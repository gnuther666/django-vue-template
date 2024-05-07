FROM centos:centos7


RUN yum update -y

RUN yum install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN ssh-keygen -A

WORKDIR /usr/local
RUN yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel unzip
RUN yum install -y wget mesa-libGL
# 部分情况无法正常下载，可手动下载
# RUN wget http://npm.taobao.org/mirrors/python/3.9.0/Python-3.9.0.tgz
COPY META/backend/Python-3.9.0.tgz .
RUN tar -zxvf Python-3.9.0.tgz
WORKDIR /usr/local/Python-3.9.0
RUN ./configure prefix=/usr/local/python3 && make && make install
RUN ln -s /usr/local/python3/bin/python3.9 /usr/bin/python3
WORKDIR /root
COPY META/backend/requirements.txt /root
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt --no-cache-dir
RUN mkdir /backend
WORKDIR /backend

# local interpreter install, only use for ide auto prompt
# sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
# wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
# tar -zxvf Python-3.9.0.tgz
# cd Python-3.9.0
# ./configure prefix=/mnt/e/python_interpreter/python3.9 && make 
# sudo make install
# cd python3.9 && ./python3 -m pip install virtualenv
# ./python3 -m virtualenv /mnt/e/workspace/django-vue-template/venv
