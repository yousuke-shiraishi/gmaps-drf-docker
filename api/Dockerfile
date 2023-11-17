# Use an official Python runtime with Alpine as a parent image
FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Tokyo
ENV LANG C.UTF-8
ENV PYTHONPATH=/myapp


RUN mkdir /myapp
RUN mkdir /myapp/app
WORKDIR /myapp
# AWS System Manager セッションマネージャ用のエージェントをインストール
# (以下の行はコメントアウトしてありますが、必要に応じてコメントを外して利用できます)
# RUN curl https://s3.ap-northeast-1.amazonaws.com/amazon-ssm-ap-northeast-1/latest/debian_amd64/amazon-ssm-agent.deb -o /tmp/amazon-ssm-agent.deb \
#     && apk add --no-cache dpkg \
#     && dpkg -i /tmp/amazon-ssm-agent.deb \
#     && cp /etc/amazon/ssm/seelog.xml.template /etc/amazon/ssm/seelog.xml

# Install system dependencies
RUN apk add --no-cache \
    bash \
    jpeg-dev \
    zlib-dev \
    libpng-dev \
    libffi-dev \
    build-base \
    postgresql-dev \
    build-base \
    python3-dev \
    curl \
    git \
    sudo \
    vim \
    netcat-openbsd

# Set work directory


# Copy requirements.txt
COPY requirements.txt /myapp/

# Install Python dependencies
RUN pip install --upgrade pip
# RUN pip install --upgrade pip setuptools
# RUN /bin/sh -c pip install -r requirements.txt
RUN pip install -r /myapp/requirements.txt

# Copy project
COPY . /myapp/

# Add a script to be executed every time the container starts.
COPY ./entrypoint.sh /myapp/app/entrypoint.sh
RUN chmod +x /myapp/app/entrypoint.sh
RUN sleep 2
CMD ["/myapp/app/entrypoint.sh"]

EXPOSE 8000
