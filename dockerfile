FROM python:3.14.4-alpine

RUN apk add --no-cache ffmpeg tini deno \
    && adduser -D app \
    && mkdir -p /app \
    && chown -R app:app /app

WORKDIR /app

COPY --chown=app:app . .

RUN mkdir -p save au \
    && chown -R app:app save au \
    && pip install --no-cache-dir -r requirements.txt \
    && wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    && chmod +x yt-dlp

USER app

ENV YT_DLP_EXEC=/app/yt-dlp

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python", "main.py"]