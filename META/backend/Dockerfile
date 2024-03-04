FROM python:3.13.0a4-slim
RUN mkdir /backend
WORKDIR /root
COPY ./META/backend/requirements.txt /root
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt --no-cache-dir
WORKDIR /backend

