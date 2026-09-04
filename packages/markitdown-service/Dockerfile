FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=False
ENV PORT=8000

# The live deb.debian.org bullseye-security pool has moved on and no longer
# serves some package builds this base image pins to, causing 404s on
# `apt-get install`. Pin to the snapshot.debian.org mirror the base image
# already references (commented out) instead, so the exact package versions
# stay available.
RUN sed -i \
    -e 's|^# deb http://snapshot|deb [check-valid-until=no] http://snapshot|' \
    -e '/^deb http:\/\/deb\.debian\.org/d' \
    /etc/apt/sources.list

# Runtime dependency
# NOTE: Add any additional MarkItDown plugins here
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool

# Cleanup
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install /app

# Default USERID and GROUPID
ARG USERID=nobody
ARG GROUPID=nogroup

USER $USERID:$GROUPID

EXPOSE 8000

ENTRYPOINT [ "markitdown-service" ]
