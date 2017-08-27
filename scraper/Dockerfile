FROM python:3.6.2-alpine3.6

WORKDIR /mnt/scraper
RUN apk add --no-cache gcc libffi-dev libressl-dev libxslt-dev musl-dev
RUN apk add --no-cache libxml2-dev \
    && mkdir -p /usr/include/libxml \
    && ln -s /usr/include/libxml2/libxml/xpath.h /usr/include/libxml/xpath.h \
    && ln -s /usr/include/libxml2/libxml/xmlversion.h /usr/include/libxml/xmlversion.h
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
