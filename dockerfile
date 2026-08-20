FROM python:3.14.4-alpine

RUN apk add --no-cache yt-dlp tini \
    && adduser -D app \
    && mkdir -p /app \
    && chown -R app:app /app

WORKDIR /app

COPY --chown=app:app . .

RUN mkdir -p save au \
    && chown -R app:app save au \
    && pip install --no-cache-dir -r requirements.txt

USER app

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "main.py"]