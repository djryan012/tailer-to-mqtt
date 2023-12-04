# Stage 1: Build Stage
FROM alpine:latest AS builder
LABEL org.opencontainers.image.source="https://github.com/djryan012/tailer-to-mqtt"

RUN apk --no-cache add bash grep yq

COPY log_tailing /app
WORKDIR /app

# Stage 2: Final Stage
FROM alpine:latest

COPY --from=builder / /

WORKDIR /app
CMD ["sh", "-c", "while [ ! -f /app/config.yaml ]; do sleep 1; done && tail_logs.sh"]
