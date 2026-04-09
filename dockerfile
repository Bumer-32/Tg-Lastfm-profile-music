FROM python:3.14.4-alpine
COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps build-base python3-dev \
    && apk add --no-cache yt-dlp \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
CMD python3 main.py