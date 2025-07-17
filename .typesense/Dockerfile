FROM alpine:latest AS parallel

# install 'parallel' for entrypoint script
RUN apk add --no-cache parallel

FROM caddy:latest AS caddy

# format caddyfile, image contains caddy binary
COPY Caddyfile ./
RUN caddy fmt --overwrite Caddyfile

FROM typesense/typesense:29.0

# copy caddyfile, caddy binary, parallel binary, and scripts from previous layers
COPY --from=caddy /srv/Caddyfile ./
COPY --from=caddy /usr/bin/caddy /usr/bin/caddy
COPY --from=parallel /usr/bin/parallel /usr/bin/parallel
COPY --chmod=755 scripts/* ./

# run start.sh script
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]