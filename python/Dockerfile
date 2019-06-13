FROM python:3.7.3-stretch

RUN apt-get update
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip install virtualenv
RUN apt-get -y install vim wget git
