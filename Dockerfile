# docker build commands
ARG FROM_IMAGE=ubuntu:18.04

FROM ${FROM_IMAGE}

RUN apt update && apt install ca-certificates -y

# change tsinghua mirror
RUN echo \
"deb [trusted=yes] https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse\n\
deb [trusted=yes] https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse\n\
deb [trusted=yes] https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse\n\
deb [trusted=yes] https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse" > /etc/apt/sources.list

RUN apt update && apt install wget \
        python3.7 python3.7-dev \
        g++ build-essential -y

WORKDIR /usr/src/jittor

RUN apt download python3-distutils && dpkg-deb -x ./python3-distutils* / \
    && wget -O - https://bootstrap.pypa.io/get-pip.py | python3.7

ENV PYTHONIOENCODING utf8

# change tsinghua mirror
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip3 install  \
        pybind11 \
        numpy \
        tqdm \
        pillow \
        astunparse \
        notebook

COPY . .

RUN pip3 install . --timeout 100

RUN python3.7 -m jittor.test.test_example

RUN rm -rf ~/.cache/jittor/default

CMD python3.7 -m jittor.notebook --allow-root